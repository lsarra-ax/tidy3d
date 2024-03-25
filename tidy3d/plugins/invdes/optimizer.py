# specification for running the optimizer
import abc
from copy import deepcopy

import pydantic.v1 as pd
import optax
import jax.numpy as jnp
import jax

import tidy3d as td

from .base import InvdesBaseModel
from .design import InverseDesign
from .result import InverseDesignResult

# TODO: beta schedule
# TODO: penalty schedule


class AbstractOptimizer(InvdesBaseModel, abc.ABC):
    """Specification for an optimization."""

    design: InverseDesign = pd.Field(...)

    history_save_fname: str = pd.Field(
        None,
        title="History Storage File",
        description="If specified, will save the optimization state to a local ``.pkl`` file "
        "using ``dill.dump()``.",
    )

    learning_rate: pd.NonNegativeFloat = pd.Field(
        ...,
        title="Learning Rate",
        description="Step size for the gradient descent optimizer.",
    )

    num_steps: pd.PositiveInt = pd.Field(
        ...,
        title="Number of Steps",
        description="Number of steps in the gradient descent optimizer.",
    )

    def display_fn(self, result: InverseDesignResult, loop_index: int) -> None:
        """Default display function while optimizing."""
        print(f"step ({loop_index + 1}/{self.num_steps})")
        print(f"\tobjective_fn_val = {result.objective_fn_val[-1]:.3e}")
        print(f"\tgrad_norm = {jnp.linalg.norm(result.grad[-1]):.3e}")
        print(f"\tpost_process_val = {result.post_process_val[-1]:.3e}")
        print(f"\tpenalty = {result.penalty[-1]:.3e}")

    def initialize_result(self, params0: jnp.ndarray) -> InverseDesignResult:
        """Create an initially empty ``InverseDesignResult`` from the starting parameters."""

        # initialize optimizer
        params0 = jnp.array(params0)
        optax_optimizer = self.optax_optimizer
        opt_state = optax_optimizer.init(params0)

        # initialize empty result
        return InverseDesignResult(design=self.design, opt_state=[opt_state], params=[params0])

    def run(self, params0: jnp.ndarray) -> InverseDesignResult:
        """Run this inverse design problem from an initial set of parameters."""

        starting_result = self.initialize_result(params0)
        return self.continue_run(result=starting_result)

    def continue_run(self, result: InverseDesignResult) -> InverseDesignResult:
        """Run optimizer for a series of steps with an initialized state."""

        # get the last state of the optimizer and the last number of params
        opt_state = result.get_final("opt_state")
        params = result.get_final("params")
        history = deepcopy(result.history)

        # use jax to grad the objective function
        # objective_fn = result.design.make_objective_fn(post_process_fn=post_process_fn)
        objective_fn = self.design.objective_fn
        val_and_grad_fn = jax.value_and_grad(objective_fn, has_aux=True)

        optax_optimizer = self.optax_optimizer

        # main optimization loop
        for loop_index in range(self.num_steps):
            # evaluate gradient
            (val, aux_data), grad = val_and_grad_fn(params)

            # strip out auxiliary data
            penalty = aux_data["penalty"]
            post_process_val = aux_data["post_process_val"]
            simulation = aux_data["simulation"]

            # save history
            history["objective_fn_val"].append(val)
            history["grad"].append(grad)
            history["penalty"].append(penalty)
            history["post_process_val"].append(post_process_val)
            history["simulation"].append(simulation)

            # display information
            result = InverseDesignResult(design=result.design, **history)
            self.display_fn(result, loop_index=loop_index)

            # TODO: need to be able to load this somehow
            if self.history_save_fname:
                result.to_file(self.history_save_fname)

            # update optimizer and parameters
            updates, opt_state = optax_optimizer.update(-grad, opt_state, params)
            params = optax.apply_updates(params, updates)
            history["params"].append(params)
            history["opt_state"].append(opt_state)

        return InverseDesignResult(design=result.design, **history)

    @td.components.base.cached_property
    @abc.abstractmethod
    def optax_optimizer(self) -> optax.GradientTransformationExtraArgs:
        """The optimizer used by ``optax`` corresponding to this spec."""


class AdamOptimizer(AbstractOptimizer):
    """Specification for an optimization."""

    b1: float = pd.Field(
        0.9,
        title="Beta 1",
        description="Beta 1 parameter in the Adam optimization method.",
    )

    b2: float = pd.Field(
        0.999,
        title="Beta 2",
        description="Beta 2 parameter in the Adam optimization method.",
    )

    eps: float = pd.Field(
        1e-8,
        title="Epsilon",
        description="Epsilon parameter in the Adam optimization method.",
    )

    @td.components.base.cached_property
    def optax_optimizer(self) -> optax.GradientTransformationExtraArgs:
        """The optimizer used by ``optax`` corresponding to this spec."""
        return optax.adam(
            learning_rate=self.learning_rate,
            b1=self.b1,
            b2=self.b2,
            eps=self.eps,
        )
