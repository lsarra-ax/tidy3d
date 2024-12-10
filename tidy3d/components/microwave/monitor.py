"""Objects that define how data is recorded from simulation."""

import math
from typing import Union

import numpy as np
import pydantic.v1 as pd

from ..base import cached_property
from ..base_sim.monitor import AbstractMonitor
from ..geometry.base import Box
from ..monitor import (
    BYTES_COMPLEX,
    BYTES_REAL,
    FieldMonitor,
    FieldTimeMonitor,
    FreqMonitor,
    TimeMonitor,
)
from ..types import ArrayFloat1D, ArrayFloat2D, Ax, Axis, Coordinate, Direction


class AbstractVoltageMonitor(AbstractMonitor):
    r_plus: Coordinate = pd.Field(
        ...,
        title="Positive terminal position.",
        description="Position vector of positive terminal.",
    )

    r_minus: Coordinate = pd.Field(
        ...,
        title="Negative terminal position.",
        description="Position vector of negative terminal.",
    )

    @cached_property
    def geometry(self) -> Box:
        """:class:`Box` representation of monitor.

        Returns
        -------
        :class:`Box`
            Representation of the monitor geometry as a :class:`Box`.
        """
        rmin = tuple(min(x, y) for x, y in zip(self.r_plus, self.r_minus))
        rmax = tuple(max(x, y) for x, y in zip(self.r_plus, self.r_minus))
        return Box.from_bounds(rmin, rmax)

    @cached_property
    def _r_delta(self) -> np.ndarray:
        return np.array(self.r_plus) - np.array(self.r_minus)

    @cached_property
    def _integration_axes(self) -> list[Axis]:
        axes = []
        for delta, axis in zip(self._r_delta, (0, 1, 2)):
            if not math.isclose(delta, 0):
                axes.append(axis)
        return axes

    @cached_property
    def _fields(self) -> list[Axis]:
        axes = self._integration_axes
        Efields = ["Ex", "Ey", "Ez"]
        fields = []
        for axis in axes:
            fields.append(Efields[axis])
        return fields

    def plot(
        self,
        x: float = None,
        y: float = None,
        z: float = None,
        ax: Ax = None,
        **patch_kwargs,
    ) -> Ax:
        """Plot this monitor."""
        box = self.geometry
        ax = box.plot(x=x, y=y, z=z, ax=ax, **patch_kwargs)
        return ax


class VoltageMonitor(FreqMonitor, AbstractVoltageMonitor):
    """:class:`VoltageMonitor` that records the voltage between two points.

    Example
    -------
    >>> monitor = VoltageMonitor(
    ...     r_plus=(0,0,1),
    ...     r_minus=(0,0,0),
    ...     freqs=[10e9, 100e9],
    ...     name='voltage_monitor')

    See Also
    --------

    **Notebooks**

    """

    @cached_property
    def _to_solver_monitor(self) -> FieldMonitor:
        box = self.geometry
        return FieldMonitor(
            name=self.name,
            freqs=self.freqs,
            apodization=self.apodization,
            center=box.center,
            size=box.size,
            interval_space=[1, 1, 1],
            colocate=False,
            fields=self._fields,
        )

    def storage_size(self, num_cells: int, tmesh: ArrayFloat1D) -> int:
        """Size of monitor storage given the number of points after discretization."""
        # stores 1 real number per frequency
        return BYTES_COMPLEX * len(self.freqs)

    def _storage_size_solver(self, num_cells: int, tmesh: ArrayFloat1D) -> int:
        """Size of intermediate data recorded by the monitor during a solver run."""
        final_data_size = self.storage_size(num_cells=num_cells, tmesh=tmesh)

        # internally solver stores all E components
        field_components_factor = 3

        # multiply by field factor
        solver_data_size = final_data_size * field_components_factor
        return solver_data_size


class VoltageTimeMonitor(TimeMonitor, AbstractVoltageMonitor):
    """:class:`Monitor` that records the voltage between two points..

    Example
    -------
    >>> monitor = FluxTimeMonitor(
    ...     center=(1,2,3),
    ...     size=(2,2,0),
    ...     start=1e-13,
    ...     stop=5e-13,
    ...     interval=2,
    ...     name='flux_vs_time')
    """

    @cached_property
    def _to_solver_monitor(self) -> FieldTimeMonitor:
        box = self.geometry
        return FieldTimeMonitor(
            name=self.name,
            start=self.start,
            stop=self.stop,
            interval=self.interval,
            center=box.center,
            size=box.size,
            interval_space=[1, 1, 1],
            colocate=False,
            fields=self._fields,
        )

    def _storage_size_solver(self, num_cells: int, tmesh: ArrayFloat1D) -> int:
        """Size of intermediate data recorded by the monitor during a solver run."""
        final_data_size = self.storage_size(num_cells=num_cells, tmesh=tmesh)

        # internally solver stores all E components
        field_components_factor = 3

        # multiply by field factor
        solver_data_size = final_data_size * field_components_factor
        return solver_data_size

    def storage_size(self, num_cells: int, tmesh: ArrayFloat1D) -> int:
        """Size of monitor storage given the number of points after discretization."""
        # stores 1 real number per time step
        num_steps = self.num_steps(tmesh)
        return BYTES_REAL * num_steps


class AbstractCurrentMonitor(AbstractMonitor):
    path: Union[Box, ArrayFloat2D] = pd.Field(
        ...,
        title="First position of",
        description="Collection of field components to store in the monitor.",
    )

    sign: Direction = pd.Field(
        "+",
        title="First position of",
        description="Collection of field components to store in the monitor.",
    )

    @cached_property
    def geometry(self) -> Box:
        """:class:`Box` representation of monitor.

        Returns
        -------
        :class:`Box`
            Representation of the monitor geometry as a :class:`Box`.
        """
        return self.path

    @cached_property
    def _integration_axes(self) -> list[Axis]:
        axes = [0, 1, 2]
        zero_dim = self.geometry.size.index(0)
        axes.pop(zero_dim)
        return axes

    @cached_property
    def normal_axis(self) -> Axis:
        """Axis normal to the monitor's plane."""
        return self.geometry.size.index(0.0)

    @cached_property
    def _fields(self) -> list[Axis]:
        axes = self._integration_axes
        Hfields = ["Hx", "Hy", "Hz"]
        fields = []
        for axis in axes:
            fields.append(Hfields[axis])
        return fields

    def plot(
        self,
        x: float = None,
        y: float = None,
        z: float = None,
        ax: Ax = None,
        **patch_kwargs,
    ) -> Ax:
        """Plot this monitor."""
        box = self.geometry
        ax = box.plot(x=x, y=y, z=z, ax=ax, **patch_kwargs)
        return ax


class CurrentMonitor(FreqMonitor, AbstractCurrentMonitor):
    """:class:`Monitor` that records the current flowing through a closed path.

    Example
    -------
    >>> monitor = FluxMonitor(
    ...     center=(1,2,3),
    ...     size=(2,2,0),
    ...     freqs=[200e12, 210e12],
    ...     name='flux_monitor')

    See Also
    --------

    **Notebooks**

    """

    @cached_property
    def _to_solver_monitor(self) -> FieldMonitor:
        box = self.geometry
        return FieldMonitor(
            name=self.name,
            freqs=self.freqs,
            apodization=self.apodization,
            center=box.center,
            size=box.size,
            interval_space=[1, 1, 1],
            colocate=False,
            fields=self._fields,
        )

    def storage_size(self, num_cells: int, tmesh: ArrayFloat1D) -> int:
        """Size of monitor storage given the number of points after discretization."""
        # stores 1 real number per frequency
        return BYTES_COMPLEX * len(self.freqs)

    def _storage_size_solver(self, num_cells: int, tmesh: ArrayFloat1D) -> int:
        """Size of intermediate data recorded by the monitor during a solver run."""
        final_data_size = self.storage_size(num_cells=num_cells, tmesh=tmesh)

        # internally solver stores all H components
        field_components_factor = 3

        # take out the stored field components factor and use the solver factor instead
        solver_data_size = final_data_size * field_components_factor
        return solver_data_size


class CurrentTimeMonitor(TimeMonitor, AbstractCurrentMonitor):
    """:class:`Monitor` that records the current flowing through a closed path.

    Example
    -------
    >>> monitor = FluxMonitor(
    ...     center=(1,2,3),
    ...     size=(2,2,0),
    ...     freqs=[200e12, 210e12],
    ...     name='flux_monitor')

    See Also
    --------

    **Notebooks**

    """

    @cached_property
    def _to_solver_monitor(self) -> FieldTimeMonitor:
        box = self.geometry
        return FieldTimeMonitor(
            name=self.name,
            start=self.start,
            stop=self.stop,
            interval=self.interval,
            center=box.center,
            size=box.size,
            interval_space=[1, 1, 1],
            colocate=False,
            fields=self._fields,
        )

    def _storage_size_solver(self, num_cells: int, tmesh: ArrayFloat1D) -> int:
        """Size of intermediate data recorded by the monitor during a solver run."""
        final_data_size = self.storage_size(num_cells=num_cells, tmesh=tmesh)

        # internally solver stores all H components
        field_components_factor = 3

        # multiply by field factor
        solver_data_size = final_data_size * field_components_factor
        return solver_data_size

    def storage_size(self, num_cells: int, tmesh: ArrayFloat1D) -> int:
        """Size of monitor storage given the number of points after discretization."""
        # stores 1 real number per time step
        num_steps = self.num_steps(tmesh)
        return BYTES_REAL * num_steps


# types of monitors that are accepted by simulation
RFMonitorType = Union[
    VoltageMonitor,
    VoltageTimeMonitor,
    CurrentMonitor,
    CurrentTimeMonitor,
]
