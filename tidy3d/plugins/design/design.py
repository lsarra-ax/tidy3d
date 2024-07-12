"""Defines design space specification for tidy3d."""

from __future__ import annotations

import inspect
from typing import Any, Callable, Dict, List, Tuple, Union

import pydantic.v1 as pd

from tidy3d.log import log

from ...components.base import Tidy3dBaseModel, cached_property
from ...components.data.sim_data import SimulationData
from ...components.simulation import Simulation
from ...web.api.container import Batch, BatchData
from .method import MethodType
from .parameter import ParameterType
from .result import Result


class DesignSpace(Tidy3dBaseModel):
    """Specification of a design problem / combination of several parameters + algorithm.

    Example
    -------
    >>> import tidy3d.plugins.design as tdd
    >>> param = tdd.ParameterFloat(name="x", span=(0,1))
    >>> method = tdd.MethodMonteCarlo(num_points=10)
    >>> design_space = tdd.DesignSpace(parameters=[param], method=method)
    >>> fn = lambda x: x**2
    >>> result = design_space.run(fn)
    >>> df = result.to_dataframe()
    >>> im = df.plot()
    """

    parameters: Tuple[ParameterType, ...] = pd.Field(
        (),
        title="Parameters",
        description="Set of parameters defining the dimensions and allowed values for the design space.",
    )

    method: MethodType = pd.Field(
        ...,
        title="Search Type",
        description="Specifications for the procedure used to explore the parameter space.",
    )

    name: str = pd.Field(None, title="Name", description="Optional name for the design space.")

    task_name: str = pd.Field(
        None,
        title="Task Name",
        description="Task name assigned to tasks along with a simulation counter. Only used when pre-post functions are supplied.",
    )

    path_dir: str = pd.Field(
        ".",
        title="Path Directory",
        description="Directory for files to output to. Only used when pre-post functions are supplied.",
    )

    folder_name: str = pd.Field(
        "default",
        title="Folder Name",
        description="Folder path where the simulation will be uploaded in the Tidy3D Workspace. Will use 'default' if no path is set.",
    )

    @cached_property
    def dims(self) -> Tuple[str]:
        """dimensions defined by the design parameter names."""
        return tuple(param.name for param in self.parameters)

    def _package_run_results(
        self,
        fn_args: list[dict[str, Any]],
        fn_values: List[Any],
        fn_source: str,
        task_ids: Tuple[str] = None,
        aux_values: List[Any] = None,
    ) -> Result:
        """How to package results from ``method.run`` and ``method.run_batch``"""

        fn_args_coords = tuple(
            [[arg_dict[key] for arg_dict in fn_args] for key in fn_args[0].keys()]
        )

        fn_args_coords_T = list(map(list, zip(*fn_args_coords)))

        # Format fn_values as appropriate

        return Result(
            dims=self.dims,
            values=fn_values,
            coords=fn_args_coords_T,
            fn_source=fn_source,
            task_ids=task_ids,
            aux_values=aux_values,
        )

    def _create_name_generator(self):
        """Initialise the name generator used for simulation task names"""
        counter = 0

        while True:
            # Check if user has supplied a dict key
            if self._dict_name is not None:
                suffix = f"{self._dict_name}_{counter}"
            else:
                suffix = f"{counter}"

            if self.task_name is not None:
                task_name = f"{self.task_name}_{suffix}"
            else:
                task_name = f"{suffix}"

            yield (task_name)
            counter += 1

    @staticmethod
    def get_fn_source(function: Callable) -> str:
        """Get the function source as a string, return ``None`` if not available."""
        try:
            return inspect.getsource(function)
        except (TypeError, OSError):
            return None

    def run(self, fn: Callable, fn_post: Callable = None, **kwargs) -> Result:
        """Run the design problem on a user defined function of the design parameters.

        Parameters
        ----------
        function : Callable
            Function accepting arguments that correspond to the ``.name`` fields
            of the ``DesignSpace.parameters``.

        Returns
        -------
        :class:`.Result`
            Object containing the results of the design space exploration.
            Can be converted to ``pandas.DataFrame`` with ``.to_dataframe()``.
        """

        # Run based on how many functions the user provides
        if fn_post is None:
            fn_args, fn_values, aux_values = self.run_single(fn)

        else:
            fn_args, fn_values, aux_values = self.run_pre_post(fn_pre=fn, fn_post=fn_post)

        fn_source = self.get_fn_source(fn)

        # Package the result
        return self._package_run_results(
            fn_args=fn_args,
            fn_values=fn_values,
            fn_source=fn_source,
            aux_values=aux_values,
            task_ids=None,
        )

    def run_single(self, fn: Callable) -> Tuple(list[dict], list, list[Any]):
        """Run a single function of parameter inputs."""
        evaluate_fn = self._get_evaluate_fn_single(fn=fn)
        return self.method.run(run_fn=evaluate_fn, parameters=self.parameters)

    def run_pre_post(self, fn_pre: Callable, fn_post: Callable) -> Tuple(
        list[dict], list[dict], list[Any]
    ):
        """Run a function with tidy3d implicitly called in between."""
        evaluate_fn = self._get_evaluate_fn_pre_post(fn_pre=fn_pre, fn_post=fn_post)
        return self.method.run(run_fn=evaluate_fn, parameters=self.parameters)

    """ Helpers """

    def _get_evaluate_fn_single(self, fn: Callable) -> list[Any]:
        """Get function that sequentially evaluates single `fn` for a list of arguments."""

        def evaluate(args_list: list) -> list[Any]:
            """Evaluate a list of arguments passed to ``fn``."""
            return [fn(**args) for args in args_list]

        return evaluate

    def _get_evaluate_fn_pre_post(self, fn_pre: Callable, fn_post: Callable) -> list[Any]:
        """Get function that tries to use batch processing on a set of arguments."""

        def evaluate(args_list: list[tuple[Any, ...]], sim_counter: int = 0) -> list[Any]:
            """Put together into one pipeline."""
            combined_fn = self._stitch_pre_post(fn_pre=fn_pre, fn_post=fn_post)
            out = combined_fn(args_list, sim_counter)
            return out

        return evaluate

    def _stitch_pre_post(self, fn_pre: Callable, fn_post: Callable) -> Callable:
        """Combine pre and post into one big function, stitching tidy3d calls between if needed."""

        def fn_combined(args_list, sim_counter):
            sim_dict = {str(idx): fn_pre(**arg_list) for idx, arg_list in enumerate(args_list)}
            data = self._fn_mid(sim_dict, sim_counter)
            post_out = [fn_post(val[1]) for val in data.items()]
            return post_out

        return fn_combined

    def _fn_mid(
        self, pre_out: dict[int, Any], sim_counter: int
    ) -> Union[dict[int, Any], BatchData]:
        """A function of the output of ``fn_pre`` that gives the input to ``fn_post``."""

        # NOTE: Need to check that pre_out has string keys!

        # Keep copy of original to use if no tidy3d simulation required
        original_pre_out = pre_out.copy()

        # Convert list input to dict of dict before passing through checks
        was_list = False
        if all(isinstance(sim, list) for sim in pre_out.values()):
            pre_out = {
                str(idx): {str(sub_idx): sub_list for sub_idx, sub_list in enumerate(sim_list)}
                for idx, sim_list in enumerate(pre_out.values())
            }
            was_list = True

        simulations = {}
        batches = {}

        def _find_and_map(search_dict: dict, search_type: Any, output_dict: dict, previous_key=""):
            """"""
            current_key = previous_key
            for key, value in search_dict.items():
                if len(previous_key) == 0:
                    latest_key = str(key)
                else:
                    latest_key = f"{current_key}_{key}"

                if isinstance(value, dict):
                    _find_and_map(value, search_type, output_dict, latest_key)
                if isinstance(value, search_type):
                    output_dict[latest_key] = value

        _find_and_map(pre_out, Simulation, simulations)
        _find_and_map(pre_out, Batch, batches)

        if len(simulations) == 0 and len(batches) == 0:
            return original_pre_out

        # Compute sims and batches and return to pre_out
        named_sims = {}
        translate_sims = {}
        for sim_key, sim in simulations.items():
            sim_name = f"{self.task_name}_{sim_counter}"
            named_sims[sim_name] = sim
            translate_sims[sim_name] = sim_key
            sim_counter += 1

        sims_out = Batch(
            simulations=named_sims,
            folder_name=self.folder_name,
            simulation_type="tidy3d_design",
        ).run(path_dir=self.path_dir)

        batch_results = {}
        for batch_key, batch in batches.items():
            batch_out = batch.run(path_dir=self.path_dir)
            batch_results[batch_key] = batch_out

        def _return_to_dict(return_dict, key, return_obj):
            """"""
            split_key = key.split("_", 1)
            if len(split_key) > 1:
                _return_to_dict(return_dict[split_key[0]], split_key[1], return_obj)
            else:
                return_dict[split_key[0]] = return_obj

        for sim_name, sim in sims_out.items():
            translated_name = translate_sims[sim_name]
            _return_to_dict(pre_out, translated_name, sim)

        for batch_name, batch in batch_results.items():
            _return_to_dict(pre_out, batch_name, batch)

        if was_list:
            return {dict_idx: list(sub_dict.values()) for dict_idx, sub_dict in pre_out.items()}

        return pre_out

    def run_batch(
        self,
        fn_pre: Callable[Any, Union[Simulation, List[Simulation], Dict[str, Simulation]]],
        fn_post: Callable[
            Union[SimulationData, List[SimulationData], Dict[str, SimulationData]], Any
        ],
        path_dir: str = None,
        **batch_kwargs,
    ) -> Result:
        """
        This function has been superceded by `run`, please use `run` for batched simulations.
        """
        log.warning(
            "In version 2.8.0, the 'run_batch' method is replaced by 'run'."
            "While the original syntax will still be supported, future functionality will be added to the new method moving forward."
        )

        if len(batch_kwargs) > 0:
            log.warning(
                "Batch_kwargs supplied here will no longer be used for within the simulation."
            )

        new_self = self.updated_copy(path_dir=path_dir)
        result = new_self.run(fn=fn_pre, fn_post=fn_post)

        return result
