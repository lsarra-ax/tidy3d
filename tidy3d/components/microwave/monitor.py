"""Objects that define how data is recorded from simulation."""

from __future__ import annotations

import math
from typing import Union

import numpy as np
import pydantic.v1 as pd

from ...constants import MICROMETER, fp_eps
from ..base import Tidy3dBaseModel, cached_property
from ..base_sim.monitor import AbstractMonitor
from ..geometry.base import Box, Geometry
from ..geometry.utils import SnapBehavior, SnapLocation, SnappingSpec, snap_box_to_grid
from ..grid.grid import Grid
from ..monitor import (
    BYTES_COMPLEX,
    BYTES_REAL,
    FieldMonitor,
    FieldTimeMonitor,
    FreqMonitor,
    TimeMonitor,
)
from ..types import ArrayFloat1D, ArrayFloat2D, Ax, Axis, Axis2D, Bound, Direction
from ..validators import assert_plane


class Path2D(Tidy3dBaseModel):
    vertices: ArrayFloat2D = pd.Field(
        ...,
        title="Vertices",
        description="List of (d1, d2) defining the 2 dimensional positions of the path. "
        "The index of dimension should be in the ascending order, which means "
        "if the axis corresponds with ``y``, the coordinates of the vertices should be (x, z). "
        "If you wish to indicate a closed contour, the final vertex should be made "
        "equal to the first vertex, i.e., ``vertices[-1] == vertices[0]``",
        units=MICROMETER,
    )

    position: float = pd.Field(
        ...,
        title="Position",
        description="Position of the plane along the ``axis``.",
    )

    axis: Axis = pd.Field(
        2, title="Axis", description="Specifies dimension of the planar axis (0,1,2) -> (x,y,z)."
    )

    @cached_property
    def bounds(self) -> Bound:
        """Helper to get the geometric bounding box of the path."""
        path_min = np.amin(self.vertices, axis=0)
        path_max = np.amax(self.vertices, axis=0)
        min_bound = Geometry.unpop_axis(self.position, path_min, self.axis)
        max_bound = Geometry.unpop_axis(self.position, path_max, self.axis)
        return (min_bound, max_bound)

    @cached_property
    def _is_axis_1D(self) -> Axis2D:
        """Checks if the path is actually 1D. If it is 1D, the axis is returned.
        Otherwise ``None`` is returned.
        """
        vertices = self.path.vertices
        for axis in (0, 1):
            coord = vertices[0][axis]
            if np.allclose(vertices[:, axis], coord, rtol=fp_eps):
                return axis
        return None

    def convert_axis_2d(self, axis_2d: Axis2D) -> Axis:
        """Converts a 2D axis to a full 3D axis."""
        if axis_2d >= self.axis:
            return axis_2d + 1
        return axis_2d

    @staticmethod
    def from_bounds(bounds: Bound) -> Path2D:
        for axis in (0, 1, 2):
            if math.isclose(bounds[1][axis] - bounds[0][axis], 0):
                normal_axis = axis
                break
        # Get 2D versions of vertices
        position, a = Geometry.pop_axis(bounds[0], normal_axis)
        _, b = Geometry.pop_axis(bounds[1], normal_axis)
        vertices = np.array((a, b))
        return Path2D(vertices=vertices, axis=normal_axis, position=position)


class BoxPath2D(Box):
    _plane_validator = assert_plane()

    sign: Direction = pd.Field(
        ...,
        title="Direction of the Path",
        description="Positive indicates a counter-clockwise orientation..",
    )


class AbstractVoltageMonitor(AbstractMonitor):
    path: Path2D = pd.Field(
        ...,
        title="Path",
        description="Computed voltage is :math:`V=V_b-V_a`, where position ``a`` and position ``b`` are "
        "the first and last vertex in the supplied path, respectively. "
        "For most cases, the path will consist of only two points, position ``a`` and position ``b``.",
        units=MICROMETER,
    )

    @cached_property
    def geometry(self) -> Box:
        """:class:`Box` representation of monitor.

        Returns
        -------
        :class:`Box`
            Representation of the monitor geometry as a :class:`Box`.
        """
        return Box.from_bounds(self.path.bounds)

    @cached_property
    def _integration_axes(self) -> list[Axis]:
        if self.path._is_axis_1D:
            return [Path2D.convert_axis_2d(self.path._is_axis_1D)]
        axes = [0, 1, 2]
        axes = Geometry.pop_axis(axes, self.path.axis)
        return axes

    @cached_property
    def _fields(self) -> list[Axis]:
        axes = self._integration_axes
        Efields = ["Ex", "Ey", "Ez"]
        fields = []
        for axis in axes:
            fields.append(Efields[axis])
        return fields

    @property
    def _to_solver_monitor(self):
        """Monitor definition that will be used to define the field recording during the time
        stepping."""
        return self

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

    def _to_field_monitor(self, grid: Grid = None) -> FieldMonitor:
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

    def _to_field_monitor(self, grid: Grid = None) -> FieldTimeMonitor:
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
    path: Union[Box, Path2D] = pd.Field(
        ...,
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
        return Box.from_bounds(self.path.bounds)

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

    @property
    def _to_solver_monitor(self):
        """Monitor definition that will be used to define the field recording during the time
        stepping."""
        return self

    def _to_enclosing_box(self, grid: Grid) -> Box:
        """Slightly expanded :class:`Box` aligned with the locations of the magnetic field.

        Returns
        -------
        :class:`Box`
            :class:`Box` aligned with the locations of the magnetic field.
        """
        box = self.geometry
        behavior = 3 * [SnapBehavior.Expand]
        behavior[self.normal_axis] = SnapBehavior.Off
        location = 3 * [SnapLocation.Center]
        snap_spec = SnappingSpec(location=location, behavior=behavior)
        return snap_box_to_grid(grid, box, snap_spec)

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

    def _to_field_monitor(self, grid: Grid = None) -> FieldMonitor:
        box = self.geometry
        if grid:
            box = self._to_enclosing_box(grid)
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

    def _to_field_monitor(self, grid: Grid = None) -> FieldTimeMonitor:
        box = self.geometry
        if grid:
            box = self._to_enclosing_box(grid)
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
