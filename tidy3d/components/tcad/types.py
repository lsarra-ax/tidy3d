from typing import Union
from tidy3d.components.tcad.source.heat import HeatSource,UniformHeatSource
from tidy3d.components.tcad.source.coupled import HeatFromElectricSource

# types of monitors that are accepted by heat simulation
HeatChargeMonitorType = Union[
    TemperatureMonitor,
    VoltageMonitor,
    FreeCarrierMonitor,
    CapacitanceMonitor,
]

HeatChargeSourceType = Union[HeatSource, HeatFromElectricSource, UniformHeatSource]

ChargeRegimeType = Union[DCSpec]
MobilityModelType = Union[CaugheyThomasMobility]
RecombinationModelType = Union[AugerRecombination, RadiativeRecombination, SRHRecombination]
BandgapNarrowingModelType = Union[SlotboomNarrowingModel]

HeatBCTypes = (TemperatureBC, HeatFluxBC, ConvectionBC)
HeatSourceTypes = (UniformHeatSource, HeatSource, HeatFromElectricSource)
ChargeSourceTypes = ()
ElectricBCTypes = (VoltageBC, CurrentBC, InsulatingBC)


class HeatChargeSimulationType(str, Enum):
    """Enumeration of the types of simulations currently supported"""

    HEAT = "HEAT"
    CONDUCTION = "CONDUCTION"
    CHARGE = "CHARGE"
