import numpy as np

from .base import Tidy3dBaseModel
from .data.dataset import TriangleMeshDataset
from .simulation import Simulation
from .types import ArrayFloat2D


class BaseModel(Tidy3dBaseModel):
    class Config:
        frozen = False
        allow_mutation = True


class SourceMetadata(BaseModel):
    source_type: str
    num_cells: int  # total number of cells inside the simulation grid
    center: tuple[float, float, float]
    size: tuple[float, float, float]
    num_freqs: int


class MonitorMetadata(BaseModel):
    monitor_type: str
    num_cells: int  # total number of cells inside the simulation grid
    center: tuple[float, float, float]
    size: tuple[float, float, float]
    num_freqs: int
    num_time_steps: int


class GeometryMetadata(BaseModel):
    geometry_type: str
    bounds: tuple[float, float, float, float, float, float]
    radius: float = None
    vertices: ArrayFloat2D = None
    mesh_dataset: TriangleMeshDataset = None
    dilation: float = None
    slant_angle: float = None


class StructureMetadata(BaseModel):
    medium_type: str
    num_poles: int
    geometry: GeometryMetadata


class BoundaryConditionMetadata(BaseModel):
    bc_type: str
    num_layers: int


class SimulationMetadata(BaseModel):
    """Metadata dataclass container."""

    grid_num_cells: tuple[float, float, float]
    num_time_steps: int
    symmetry_present: tuple[int, int, int]
    bounds: tuple[float, float, float, float, float, float]  # including PML

    sources: tuple[SourceMetadata, ...] = tuple()
    monitors: tuple[MonitorMetadata, ...] = tuple()
    structures: tuple[StructureMetadata, ...] = tuple()
    boundaries: tuple[BoundaryConditionMetadata, ...] = tuple()


def simulation_metadata(simulation: Simulation):
    """Create a simulation metadata model."""

    metadata = SimulationMetadata(
        grid_num_cells=tuple(simulation.grid.num_cells),
        num_time_steps=len(simulation.tmesh),
        symmetry_present=tuple(sym != 0 for sym in simulation.symmetry),
        bounds=np.array(simulation.simulation_bounds).ravel().tolist(),
    )

    structures_list = []
    for struct in simulation.structures:
        struct_geom = struct.geometry.to_static()
        bounds = struct_geom.bounds_intersection(struct_geom.bounds, simulation.simulation_bounds)
        geometry = GeometryMetadata(
            geometry_type=struct_geom.type,
            bounds=np.array(bounds).ravel().tolist(),
        )
        for key, val in iter(geometry):
            if val is None:
                setattr(geometry, key, getattr(struct_geom, key, None))

        try:
            num_poles = len(struct.medium.pole_residue.num_poles)
        except AttributeError:
            num_poles = 0
        struct_meta = StructureMetadata(
            geometry=geometry,
            medium_type=struct.medium.type,
            num_poles=num_poles,
        )
        structures_list.append(struct_meta)

    monitors_list = []
    for mnt in simulation.monitors:
        try:
            num_time_steps = len(mnt.time_inds(simulation.tmesh))
        except AttributeError:
            num_time_steps = 0

        monitor = MonitorMetadata(
            monitor_type=mnt.type,
            num_cells=simulation._monitor_num_cells(mnt),
            center=mnt.center,
            size=mnt.size,
            num_freqs=len(getattr(mnt, "freqs", [])),
            num_time_steps=num_time_steps,
        )
        monitors_list.append(monitor)

    sources_list = []
    for src in simulation.sources:
        source = SourceMetadata(
            source_type=src.type,
            num_cells=np.prod(simulation.discretize(src).num_cells),
            center=src.center,
            size=src.size,
            num_freqs=getattr(src, "num_freqs", 1),
        )
        sources_list.append(source)

    bcs_list = []
    for boundary1d in simulation.boundary_spec.to_list:
        for bc in boundary1d:
            boundary = BoundaryConditionMetadata(
                bc_type=bc.type,
                num_layers=getattr(bc, "num_layers", 1),
            )
            bcs_list.append(boundary)

    metadata.structures = structures_list
    metadata.monitors = monitors_list
    metadata.sources = sources_list
    metadata.boundaries = bcs_list

    return metadata
