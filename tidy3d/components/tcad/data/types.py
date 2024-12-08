from typing import Union
from tidy3d.components.tcad.data.monitor_data.heat import (
    TemperatureData
)
from tidy3d.components.tcad.data.monitor_data.charge import (
    VoltageData,
    PotentialData,
    FreeCarrierData,
    CapacitanceData
)

HeatChargeMonitorDataTypes = Union[
    TemperatureData, VoltageData, PotentialData, FreeCarrierData, CapacitanceData
]
