"""Tidy3d package imports"""

# grid
# apodization
# tcad
from tidy3d.components.tcad.bandgap import SlotboomNarrowingBandGap
from tidy3d.components.tcad.boundary.charge import CurrentBC, InsulatingBC, VoltageBC
from tidy3d.components.tcad.boundary.heat import ConvectionBC, HeatFluxBC, TemperatureBC
from tidy3d.components.tcad.boundary.specification import HeatBoundarySpec, HeatChargeBoundarySpec
from tidy3d.components.tcad.data.monitor_data.abstract import (
    HeatChargeMonitorData,
)
from tidy3d.components.tcad.data.monitor_data.charge import (
    CapacitanceData,
    DCCapacitanceDataArray,
    FreeCarrierData,
    PotentialData,
    VoltageData,
)
from tidy3d.components.tcad.data.monitor_data.heat import TemperatureData
from tidy3d.components.tcad.data.sim_data import HeatChargeSimulationData, HeatSimulationData
from tidy3d.components.tcad.generation_recombination import (
    AugerRecombination,
    RadiativeRecombination,
    ShockleyReedHallRecombination,
)
from tidy3d.components.tcad.grid import (
    DistanceUnstructuredGrid,
    UniformUnstructuredGrid,
)
from tidy3d.components.tcad.materials.charge import (
    ElectricSpecType,
    SemiConductorSpec,
)
from tidy3d.components.tcad.materials.heat import FluidSpec, SolidSpec, ThermalSpecType
from tidy3d.components.tcad.mobility import CaugheyThomasMobility
from tidy3d.components.tcad.monitors.abstract import HeatChargeMonitor
from tidy3d.components.tcad.monitors.charge import (
    CapacitanceMonitor,
    FreeCarrierMonitor,
    VoltageMonitor,
)
from tidy3d.components.tcad.monitors.heat import (
    TemperatureMonitor,
)
from tidy3d.components.tcad.simulation.heat import HeatSimulation
from tidy3d.components.tcad.simulation.heat_charge import HeatChargeSimulation
from tidy3d.components.tcad.source.coupled import GlobalHeatChargeSource, HeatFromElectricSource
from tidy3d.components.tcad.source.heat import (
    HeatSource,
    UniformHeatSource,
)
from tidy3d.components.tcad.types import (
    BandGapModelTypes,
    ChargeMonitorTypes,
    ChargeSourceTypes,
    ElectricBCTypes,
    HeatBCTypes,
    HeatChargeBCTypes,
    HeatChargeMonitorTypes,
    HeatChargeSimulationTypes,
    HeatChargeSourceTypes,
    HeatSourceTypes,
    MobilityModelTypes,
    RecombinationModelTypes,
)

from .components.apodization import ApodizationSpec

# boundary placement for other solvers
from .components.bc_placement import (
    MediumMediumInterface,
    SimulationBoundary,
    StructureBoundary,
    StructureSimulationBoundary,
    StructureStructureInterface,
)

# boundary
from .components.boundary import (
    PML,
    Absorber,
    AbsorberParams,
    BlochBoundary,
    Boundary,
    BoundaryEdge,
    BoundaryEdgeType,
    BoundarySpec,
    DefaultAbsorberParameters,
    DefaultPMLParameters,
    DefaultStablePMLParameters,
    PECBoundary,
    Periodic,
    PMCBoundary,
    PMLParams,
    PMLTypes,
    StablePML,
)

# data
from .components.data.data_array import (
    AxialRatioDataArray,
    CellDataArray,
    ChargeDataArray,
    DCIVCurveDataArray,
    DiffractionDataArray,
    DirectivityDataArray,
    EMECoefficientDataArray,
    EMEModeIndexDataArray,
    EMEScalarFieldDataArray,
    EMEScalarModeFieldDataArray,
    EMESMatrixDataArray,
    FieldProjectionAngleDataArray,
    FieldProjectionCartesianDataArray,
    FieldProjectionKSpaceDataArray,
    FluxDataArray,
    FluxTimeDataArray,
    HeatDataArray,
    IndexedDataArray,
    ModeAmpsDataArray,
    ModeIndexDataArray,
    PointDataArray,
    ScalarFieldDataArray,
    ScalarFieldTimeDataArray,
    ScalarModeFieldCylindricalDataArray,
    ScalarModeFieldDataArray,
    SpatialDataArray,
)
from .components.data.dataset import (
    FieldDataset,
    FieldTimeDataset,
    ModeSolverDataset,
    PermittivityDataset,
    TetrahedralGridDataset,
    TriangularGridDataset,
)
from .components.data.monitor_data import (
    AbstractFieldProjectionData,
    DiffractionData,
    DirectivityData,
    FieldData,
    FieldProjectionAngleData,
    FieldProjectionCartesianData,
    FieldProjectionKSpaceData,
    FieldTimeData,
    FluxData,
    FluxTimeData,
    ModeData,
    ModeSolverData,
    PermittivityData,
)
from .components.data.sim_data import DATA_TYPE_MAP, SimulationData
from .components.eme.data.dataset import (
    EMECoefficientDataset,
    EMEFieldDataset,
    EMEModeSolverDataset,
    EMESMatrixDataset,
)
from .components.eme.data.monitor_data import EMECoefficientData, EMEFieldData, EMEModeSolverData
from .components.eme.data.sim_data import EMESimulationData
from .components.eme.grid import (
    EMECompositeGrid,
    EMEExplicitGrid,
    EMEGrid,
    EMEModeSpec,
    EMEUniformGrid,
)
from .components.eme.monitor import (
    EMECoefficientMonitor,
    EMEFieldMonitor,
    EMEModeSolverMonitor,
    EMEMonitor,
)

# EME
from .components.eme.simulation import EMESimulation
from .components.eme.sweep import EMEFreqSweep, EMELengthSweep, EMEModeSweep

# field projection
from .components.field_projection import FieldProjector

# frequency conversion utilities
from .components.frequencies import frequencies, wavelengths

# geometry
from .components.geometry.base import Box, ClipOperation, Geometry, GeometryGroup, Transformed
from .components.geometry.mesh import TriangleMesh
from .components.geometry.polyslab import PolySlab
from .components.geometry.primitives import Cylinder, Sphere
from .components.grid.grid import Coords, Coords1D, FieldGrid, Grid, YeeGrid
from .components.grid.grid_spec import (
    AutoGrid,
    CustomGrid,
    CustomGridBoundaries,
    GridSpec,
    UniformGrid,
)

# lumped elements
from .components.lumped_element import (
    AdmittanceNetwork,
    CoaxialLumpedResistor,
    LinearLumpedElement,
    LumpedElement,
    LumpedResistor,
    RectangularLumpedElement,
    RLCNetwork,
)

# medium
# for docs
from .components.medium import (
    PEC,
    PEC2D,
    AbstractMedium,
    AnisotropicMedium,
    CustomAnisotropicMedium,
    CustomDebye,
    CustomDrude,
    CustomLorentz,
    CustomMedium,
    CustomPoleResidue,
    CustomSellmeier,
    Debye,
    Drude,
    FullyAnisotropicMedium,
    KerrNonlinearity,
    Lorentz,
    LossyMetalMedium,
    Medium,
    Medium2D,
    NonlinearModel,
    NonlinearSpec,
    NonlinearSusceptibility,
    PECMedium,
    PerturbationMedium,
    PerturbationPoleResidue,
    PoleResidue,
    Sellmeier,
    SkinDepthFitterParam,
    TwoPhotonAbsorption,
    medium_from_nk,
)

# modes
from .components.mode import ModeSpec

# monitors
from .components.monitor import (
    DiffractionMonitor,
    DirectivityMonitor,
    FieldMonitor,
    FieldProjectionAngleMonitor,
    FieldProjectionCartesianMonitor,
    FieldProjectionKSpaceMonitor,
    FieldProjectionSurface,
    FieldTimeMonitor,
    FluxMonitor,
    FluxTimeMonitor,
    ModeMonitor,
    ModeSolverMonitor,
    Monitor,
    PermittivityMonitor,
)
from .components.parameter_perturbation import (
    CustomChargePerturbation,
    CustomHeatPerturbation,
    IndexPerturbation,
    LinearChargePerturbation,
    LinearHeatPerturbation,
    ParameterPerturbation,
    PermittivityPerturbation,
)

# run time spec
from .components.run_time_spec import RunTimeSpec

# scene
from .components.scene import Scene

# simulation
from .components.simulation import Simulation

# sources
from .components.source import (
    TFSF,
    AstigmaticGaussianBeam,
    ContinuousWave,
    CustomCurrentSource,
    CustomFieldSource,
    CustomSourceTime,
    GaussianBeam,
    GaussianPulse,
    ModeSource,
    PlaneWave,
    PointDipole,
    Source,
    SourceTime,
    UniformCurrentSource,
)

# structures
from .components.structure import MeshOverrideStructure, Structure

# subpixel
from .components.subpixel_spec import (
    HeuristicPECStaircasing,
    PECConformal,
    PolarizedAveraging,
    Staircasing,
    SubpixelSpec,
    SurfaceImpedance,
    VolumetricAveraging,
)

# time modulation
from .components.time_modulation import (
    ContinuousWaveTimeModulation,
    ModulationSpec,
    SpaceModulation,
    SpaceTimeModulation,
)
from .components.transformation import RotationAroundAxis

# config
from .config import config

# constants imported as `C_0 = td.C_0` or `td.constants.C_0`
from .constants import C_0, EPSILON_0, ETA_0, HBAR, K_B, MU_0, Q_e, inf
from .log import log, set_logging_console, set_logging_file

# material library dict imported as `from tidy3d import material_library`
# get material `mat` and variant `var` as `material_library[mat][var]`
from .material_library.material_library import material_library
from .material_library.parametric_materials import Graphene

# updater
from .updater import Updater

# version
from .version import __version__


def set_logging_level(level: str) -> None:
    """Raise a warning here instead of setting the logging level."""
    raise DeprecationWarning(
        "``set_logging_level`` no longer supported. "
        f"To set the logging level, call ``tidy3d.config.logging_level = {level}``."
    )


log.info(f"Using client version: {__version__}")

Transformed.update_forward_refs()
ClipOperation.update_forward_refs()
GeometryGroup.update_forward_refs()

__all__ = [
# <<<<<<< HEAD
#     "Grid",
#     "Coords",
#     "GridSpec",
#     "UniformGrid",
#     "CustomGrid",
#     "AutoGrid",
#     "CustomGridBoundaries",
#     "Box",
#     "Sphere",
#     "Cylinder",
#     "PolySlab",
#     "GeometryGroup",
#     "ClipOperation",
#     "Transformed",
#     "TriangleMesh",
#     "Medium",
#     "PoleResidue",
#     "AnisotropicMedium",
#     "PEC",
#     "PECMedium",
#     "Medium2D",
#     "PEC2D",
#     "Sellmeier",
#     "Debye",
#     "Drude",
#     "Lorentz",
#     "CustomMedium",
#     "CustomPoleResidue",
#     "CustomSellmeier",
#     "FullyAnisotropicMedium",
#     "CustomLorentz",
#     "CustomDrude",
#     "CustomDebye",
#     "CustomAnisotropicMedium",
#     "LossyMetalMedium",
#     "SkinDepthFitterParam",
#     "RotationAroundAxis",
#     "PerturbationMedium",
#     "PerturbationPoleResidue",
#     "ParameterPerturbation",
#     "LinearHeatPerturbation",
#     "CustomHeatPerturbation",
#     "LinearChargePerturbation",
#     "CustomChargePerturbation",
#     "PermittivityPerturbation",
#     "IndexPerturbation",
#     "NonlinearSpec",
#     "NonlinearModel",
#     "NonlinearSusceptibility",
#     "TwoPhotonAbsorption",
#     "KerrNonlinearity",
#     "Structure",
#     "MeshOverrideStructure",
#     "ModeSpec",
#     "ApodizationSpec",
#     "GaussianPulse",
#     "ContinuousWave",
#     "CustomSourceTime",
#     "UniformCurrentSource",
#     "PlaneWave",
#     "ModeSource",
#     "PointDipole",
#     "GaussianBeam",
#     "AstigmaticGaussianBeam",
#     "CustomFieldSource",
#     "TFSF",
#     "CustomCurrentSource",
#     "FieldMonitor",
#     "FieldTimeMonitor",
#     "FluxMonitor",
#     "FluxTimeMonitor",
#     "ModeMonitor",
#     "ModeSolverMonitor",
#     "PermittivityMonitor",
#     "FieldProjectionAngleMonitor",
#     "FieldProjectionCartesianMonitor",
#     "FieldProjectionKSpaceMonitor",
#     "FieldProjectionSurface",
#     "DiffractionMonitor",
#     "DirectivityMonitor",
#     "RunTimeSpec",
#     "Simulation",
#     "FieldProjector",
#     "ScalarFieldDataArray",
#     "ScalarModeFieldDataArray",
#     "ScalarModeFieldCylindricalDataArray",
#     "ScalarFieldTimeDataArray",
#     "SpatialDataArray",
#     "ModeAmpsDataArray",
#     "ModeIndexDataArray",
#     "FluxDataArray",
#     "FluxTimeDataArray",
#     "FieldProjectionAngleDataArray",
#     "FieldProjectionCartesianDataArray",
#     "FieldProjectionKSpaceDataArray",
#     "DiffractionDataArray",
#     "DirectivityDataArray",
#     "AxialRatioDataArray",
#     "HeatDataArray",
#     "ChargeDataArray",
#     "FieldDataset",
#     "FieldTimeDataset",
#     "PermittivityDataset",
#     "ModeSolverDataset",
#     "FieldData",
#     "FieldTimeData",
#     "PermittivityData",
#     "FluxData",
#     "FluxTimeData",
#     "ModeData",
#     "ModeSolverData",
# =======
    "Absorber",
    "AbsorberParams",
    "AbstractFieldProjectionData",
    "AbstractMedium",
    "AdmittanceNetwork",
    "AnisotropicMedium",
    "ApodizationSpec",
    "AstigmaticGaussianBeam",
    "AugerRecombination",
    "AutoGrid",
    "AxialRatioDataArray",
    "BandGapModelTypes",
    "BlochBoundary",
    "Boundary",
    "BoundaryEdge",
    "BoundaryEdgeType",
    "BoundarySpec",
    "Box",
    "C_0",
    "CapacitanceData",
    "CapacitanceMonitor",
    "CaugheyThomasMobility",
    "CellDataArray",
    "ChargeDataArray",
    "ChargeToleranceSpec",
    "ChargeSourceTypes",
    "ChargeMonitorTypes",
    "ClipOperation",
    "CoaxialLumpedResistor",
    "ConductorSpec",
    "ContinuousWave",
    "ContinuousWaveTimeModulation",
    "ConvectionBC",
    "Coords",
    "Coords1D",
    "CurrentBC",
    "CustomAnisotropicMedium",
    "CustomChargePerturbation",
    "CustomCurrentSource",
    "CustomDebye",
    "CustomDrude",
    "CustomFieldSource",
    "CustomGrid",
    "CustomGridBoundaries",
    "CustomHeatPerturbation",
    "CustomLorentz",
    "CustomMedium",
    "CustomPoleResidue",
    "CustomSellmeier",
    "CustomSourceTime",
    "Cylinder",
    "DATA_TYPE_MAP",
    "DCCapacitanceDataArray",
    "DCIVCurveDataArray",
    "DCSpec",
    "Debye",
    "DefaultAbsorberParameters",
    "DefaultPMLParameters",
    "DefaultStablePMLParameters",
    "DiffractionData",
    "DiffractionDataArray",
    "DiffractionMonitor",
    "DirectivityData",
    "DirectivityDataArray",
    "DirectivityMonitor",
    "DistanceUnstructuredGrid",
    "Drude",
    "ElectricBCTypes",
    "ElectricSpecType",
    "EMECoefficientData",
    "EMECoefficientDataArray",
    "EMECoefficientDataset",
    "EMECoefficientMonitor",
    "EMECompositeGrid",
    "EMEExplicitGrid",
    "EMEFieldData",
    "EMEFieldDataset",
    "EMEFieldMonitor",
    "EMEFreqSweep",
    "EMEGrid",
    "EMELengthSweep",
    "EMEModeIndexDataArray",
    "EMEModeSolverData",
    "EMEModeSolverDataset",
    "EMEModeSolverMonitor",
    "EMEModeSpec",
    "EMEModeSweep",
    "EMEMonitor",
    "EMESMatrixDataArray",
    "EMESMatrixDataset",
    "EMEScalarFieldDataArray",
    "EMEScalarModeFieldDataArray",
    "EMESimulation",
    "EMESimulationData",
    "EMESweepSpec",
    "EMEUniformGrid",
    "EPSILON_0",
    "ETA_0",
    "FieldData",
    "FieldDataset",
    "FieldGrid",
    "FieldMonitor",
    "FieldProjectionAngleData",
    "FieldProjectionAngleDataArray",
    "FieldProjectionAngleMonitor",
    "FieldProjectionCartesianData",
    "FieldProjectionCartesianDataArray",
    "FieldProjectionCartesianMonitor",
    "FieldProjectionKSpaceData",
    "FieldProjectionKSpaceDataArray",
    "FieldProjectionKSpaceMonitor",
    "FieldProjectionSurface",
    "FieldProjector",
    "FieldTimeData",
    "FieldTimeDataset",
    "FieldTimeMonitor",
    "FluidSpec",
    "FluxData",
    "FluxDataArray",
    "FluxMonitor",
    "FluxTimeData",
    "FluxTimeDataArray",
    "FluxTimeMonitor",
    "FreeCarrierData",
    "FreeCarrierMonitor",
    "FullyAnisotropicMedium",
    "GaussianBeam",
    "GaussianPulse",
    "Geometry",
    "GeometryGroup",
    "GlobalHeatChargeSource",
    "Graphene",
    "Grid",
    "GridSpec",
    "HBAR",
    "HeatBoundarySpec",
    "HeatChargeBoundarySpec",
    "HeatChargeMonitor",
    "HeatBCTypes",
    "HeatChargeBCTypes",
    "HeatChargeMonitorData",
    "HeatChargeMonitorTypes",
    "HeatChargeSimulation",
    "HeatChargeSimulationData",
    "HeatChargeSimulationTypes",
    "HeatChargeSourceTypes",
    "HeatDataArray",
    "HeatFluxBC",
    "HeatFromElectricSource",
    "HeatSimulation",
    "HeatSimulationData",
    "HeatSource",
    "HeatSourceTypes",
    "HeuristicPECStaircasing",
    "IndexPerturbation",
    "IndexedDataArray",
    "InsulatingBC",
    "InsulatorSpec",
    "K_B",
    "KerrNonlinearity",
    "LinearChargePerturbation",
    "LinearHeatPerturbation",
    "LinearLumpedElement",
    "Lorentz",
    "LossyMetalMedium",
    "LumpedElement",
    "LumpedResistor",
    "MU_0",
    "Medium",
    "Medium2D",
    "MediumMediumInterface",
    "MeshOverrideStructure",
    "MobilityModelTypes",
    "ModeAmpsDataArray",
    "ModeData",
    "ModeIndexDataArray",
    "ModeMonitor",
    "ModeSolverData",
    "ModeSolverDataset",
    "ModeSolverMonitor",
    "ModeSource",
    "ModeSpec",
    "ModulationSpec",
    "Monitor",
    "NonlinearModel",
    "NonlinearSpec",
    "NonlinearSusceptibility",
    "PEC",
    "PEC2D",
    "PECBoundary",
    "PECConformal",
    "PECMedium",
    "PMCBoundary",
    "PML",
    "PMLParams",
    "PMLTypes",
    "ParameterPerturbation",
    "Periodic",
    "PermittivityData",
    "PermittivityDataset",
    "PermittivityMonitor",
    "PermittivityPerturbation",
    "PerturbationMedium",
    "PerturbationPoleResidue",
    "PlaneWave",
    "PointDataArray",
    "PointDipole",
    "PolarizedAveraging",
    "PoleResidue",
    "PolySlab",
    "PotentialData",
    "Q_e",
    "RLCNetwork",
    "RadiativeRecombination",
    "RectangularLumpedElement",
    "RecombinationModelTypes",
    "RotationAroundAxis",
    "RunTimeSpec",
    "ScalarFieldDataArray",
    "ScalarFieldTimeDataArray",
    "ScalarModeFieldDataArray",
    "Scene",
    "Sellmeier",
    "SemiConductorSpec",
    "ShockleyReedHallRecombination",
    "Simulation",
    "SimulationBoundary",
    "SimulationData",
    "SkinDepthFitterParam",
    "SlotboomNarrowingBandGap",
    "SolidSpec",
    "Source",
    "SourceTime",
    "SpaceModulation",
    "SpaceTimeModulation",
    "SpatialDataArray",
    "Sphere",
    "StablePML",
    "Staircasing",
    "Structure",
    "StructureBoundary",
    "StructureSimulationBoundary",
    "StructureStructureInterface",
    "SubpixelSpec",
    "SurfaceImpedance",
    "TFSF",
    "TemperatureBC",
    "TemperatureData",
    "TemperatureMonitor",
    "TetrahedralGridDataset",
    "ThermalSpecType",
    "Transformed",
    "TriangleMesh",
    "TriangularGridDataset",
    "TwoPhotonAbsorption",
    "UniformCurrentSource",
    "UniformGrid",
    "UniformHeatSource",
    "UniformUnstructuredGrid",
    "Updater",
    "VoltageBC",
    "VoltageData",
    "VoltageMonitor",
    "VolumetricAveraging",
    "YeeGrid",
    "__version__",
    "config",
    "frequencies",
    "inf",
    "log",
    "material_library",
    "medium_from_nk",
    "set_logging_console",
    "set_logging_file",
    "wavelengths",
]
