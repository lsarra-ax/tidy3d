"""Tidy3d package imports"""

# grid
# apodization
from tidy3d.components.data.dataset import (
    FieldDataset,
    FieldTimeDataset,
    ModeSolverDataset,
    PermittivityDataset,
    TetrahedralGridDataset,
    TriangularGridDataset,
)
from tidy3d.components.data.monitor_data import (
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
from tidy3d.components.data.sim_data import DATA_TYPE_MAP, SimulationData
from tidy3d.components.eme.data.dataset import (
    EMECoefficientDataset,
    EMEFieldDataset,
    EMEModeSolverDataset,
    EMESMatrixDataset,
)
from tidy3d.components.eme.data.monitor_data import (
    EMECoefficientData,
    EMEFieldData,
    EMEModeSolverData,
)
from tidy3d.components.eme.data.sim_data import EMESimulationData
from tidy3d.components.eme.grid import (
    EMECompositeGrid,
    EMEExplicitGrid,
    EMEGrid,
    EMEModeSpec,
    EMEUniformGrid,
)
from tidy3d.components.eme.monitor import (
    EMECoefficientMonitor,
    EMEFieldMonitor,
    EMEModeSolverMonitor,
    EMEMonitor,
)

# EME
from tidy3d.components.eme.simulation import EMESimulation
from tidy3d.components.eme.sweep import EMEFreqSweep, EMELengthSweep, EMEModeSweep

# field projection
from tidy3d.components.field_projection import FieldProjector

# frequency conversion utilities
from tidy3d.components.frequencies import frequencies, wavelengths

# geometry
from tidy3d.components.geometry.base import Box, ClipOperation, Geometry, GeometryGroup, Transformed
from tidy3d.components.geometry.mesh import TriangleMesh
from tidy3d.components.geometry.polyslab import PolySlab
from tidy3d.components.geometry.primitives import Cylinder, Sphere
from tidy3d.components.grid.grid import Coords, Coords1D, FieldGrid, Grid, YeeGrid
from tidy3d.components.grid.grid_spec import (
    AutoGrid,
    CustomGrid,
    CustomGridBoundaries,
    GridSpec,
    UniformGrid,
)

# lumped elements
from tidy3d.components.lumped_element import (
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
from tidy3d.components.medium import (
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
from tidy3d.components.mode import ModeSpec

# monitors
from tidy3d.components.monitor import (
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
from tidy3d.components.parameter_perturbation import (
    CustomChargePerturbation,
    CustomHeatPerturbation,
    IndexPerturbation,
    LinearChargePerturbation,
    LinearHeatPerturbation,
    ParameterPerturbation,
    PermittivityPerturbation,
)

# run time spec
from tidy3d.components.run_time_spec import RunTimeSpec

# scene
from tidy3d.components.scene import Scene

# simulation
from tidy3d.components.simulation import Simulation

# sources
from tidy3d.components.source import (
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
from tidy3d.components.spice import (
    Capacitor,
    ElectricalAnalysisTypes,
    MultiStaticTransferSourceDC,
    OperatingPointDC,
    StaticTransferSourceDC,
    TransferFunctionDC,
)

# structures
from tidy3d.components.structure import MeshOverrideStructure, Structure

# subpixel
from tidy3d.components.subpixel_spec import (
    HeuristicPECStaircasing,
    PECConformal,
    PolarizedAveraging,
    Staircasing,
    SubpixelSpec,
    SurfaceImpedance,
    VolumetricAveraging,
)

# tcad
from tidy3d.components.tcad.bandgap import SlotboomNarrowingBandGap
from tidy3d.components.tcad.boundary.charge import CurrentBC, InsulatingBC, VoltageBC
from tidy3d.components.tcad.boundary.heat import ConvectionBC, HeatFluxBC, TemperatureBC
from tidy3d.components.tcad.boundary.specification import HeatBoundarySpec, HeatChargeBoundarySpec
from tidy3d.components.tcad.data.monitor_data.abstract import (
    HeatChargeMonitorData,
)
from tidy3d.components.tcad.data.monitor_data.charge import (
    ElectroStaticDataArray,
    StaticCapacitanceData,
    StaticChargeCarrierData,
    # PotentialData,
    StaticVoltageData,
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
    ElectronicSpec,
)
from tidy3d.components.tcad.materials.heat import FluidSpec, SolidSpec, ThermalSpecType
from tidy3d.components.tcad.mobility import CaugheyThomasMobility
from tidy3d.components.tcad.monitors.abstract import HeatChargeMonitor
from tidy3d.components.tcad.monitors.charge import (
    StaticCapacitanceMonitor,
    StaticChargeCarrierMonitor,
    StaticVoltageMonitor,
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

# time modulation
from tidy3d.components.time_modulation import (
    ContinuousWaveTimeModulation,
    ModulationSpec,
    SpaceModulation,
    SpaceTimeModulation,
)
from tidy3d.components.transformation import RotationAroundAxis

# config
from tidy3d.config import config

# constants imported as `C_0 = td.C_0` or `td.constants.C_0`
from tidy3d.constants import C_0, EPSILON_0, ETA_0, HBAR, K_B, MU_0, Q_e, inf
from tidy3d.log import log, set_logging_console, set_logging_file

# material library dict imported as `from tidy3d import material_library`
# get material `mat` and variant `var` as `material_library[mat][var]`
from tidy3d.material_library.material_library import material_library
from tidy3d.material_library.parametric_materials import Graphene

# updater
from tidy3d.updater import Updater

# version
from tidy3d.version import __version__

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
    ChargeCarrierDataArray,
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
    "Capacitor",
    "StaticCapacitanceData",
    "StaticCapacitanceMonitor",
    "CaugheyThomasMobility",
    "CellDataArray",
    "ChargeCarrierDataArray",
    "ChargeSourceTypes",
    "ChargeMonitorTypes",
    "ClipOperation",
    "CoaxialLumpedResistor",
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
    "ElectroStaticDataArray",
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
    "ElectricalAnalysisTypes",
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
    # "EMESweepSpec",
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
    "StaticChargeCarrierData",
    "StaticChargeCarrierMonitor",
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
    "MultiStaticTransferSourceDC",
    "NonlinearModel",
    "NonlinearSpec",
    "NonlinearSusceptibility",
    "OperatingPointDC",
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
    "ScalarModeFieldCylindricalDataArray",
    "Scene",
    "Sellmeier",
    "ElectronicSpec",
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
    "StaticTransferSourceDC",
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
    "TransferFunctionDC",
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
    "StaticVoltageData",
    "StaticVoltageMonitor",
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
