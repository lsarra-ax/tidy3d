from typing import Union
from tidy3d.components.tcad.source.heat import HeatSource, UniformHeatSource
from tidy3d.components.tcad.source.coupled import HeatFromElectricSource
from tidy3d.components.tcad.monitors.heat import TemperatureMonitor
from tidy3d.components.tcad.monitors.charge import VoltageMonitor, FreeCarrierMonitor, CapacitanceMonitor
from tidy3d.components.tcad.mobility import CaugheyThomasMobility
from tidy3d.components.tcad.generation_recombination import AugerRecombination, RadiativeRecombination, \
    ShockleyReedHallRecombination
from tidy3d.components.tcad.bandgap import SlotboomNarrowingBandGap
from tidy3d.components.tcad.boundary.heat import TemperatureBC, HeatFluxBC, ConvectionBC
from tidy3d.components.tcad.boundary.charge import VoltageBC, CurrentBC, InsulatingBC

# types of monitors that are accepted by heat simulation
HeatChargeMonitorType = Union[
    TemperatureMonitor,
    VoltageMonitor,
    FreeCarrierMonitor,
    CapacitanceMonitor,
]
ChargeMonitorType = (VoltageMonitor, FreeCarrierMonitor, CapacitanceMonitor)
HeatChargeMonitorDataType = Union[
    TemperatureData, VoltageData, PotentialData, FreeCarrierData, CapacitanceData
]

FieldDataset = Union[
    SpatialDataArray, annotate_type(Union[TriangularGridDataset, TetrahedralGridDataset])
]

HeatChargeSourceType = Union[
    HeatSource,
    HeatFromElectricSource,
    UniformHeatSource
]
ChargeSourceTypes = None
HeatSourceTypes = (UniformHeatSource, HeatSource, HeatFromElectricSource)

MobilityModelType = Union[
    CaugheyThomasMobility
]
RecombinationModelType = Union[
    AugerRecombination,
    RadiativeRecombination,
    ShockleyReedHallRecombination
]
BandGapModelType = Union[
    SlotboomNarrowingBandGap
]

HeatBCTypes = (TemperatureBC, HeatFluxBC, ConvectionBC)
ElectricBCTypes = (VoltageBC, CurrentBC, InsulatingBC)


class HeatChargeSimulationType(str, Enum):
    """Enumeration of the types of simulations currently supported"""

    HEAT = "HEAT"
    CONDUCTION = "CONDUCTION"
    CHARGE = "CHARGE"
