from typing import Union

ChargeRegimeType = Union[DCSpec]
MobilityModelType = Union[CaugheyThomasMobility]
RecombinationModelType = Union[AugerRecombination, RadiativeRecombination, SRHRecombination]
BandgapNarrowingModelType = Union[SlotboomNarrowingModel]

HeatBCTypes = (TemperatureBC, HeatFluxBC, ConvectionBC)
HeatSourceTypes = (UniformHeatSource, HeatSource, HeatFromElectricSource)
ChargeSourceTypes = ()
ElectricBCTypes = (VoltageBC, CurrentBC, InsulatingBC)
