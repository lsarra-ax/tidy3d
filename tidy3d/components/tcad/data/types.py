from typing import Union

from tidy3d.components.tcad.data.monitor_data.charge import (
    CapacitanceData,
    FreeCarrierData,
    PotentialData,
    VoltageData,
)
from tidy3d.components.tcad.data.monitor_data.heat import TemperatureData

HeatChargeMonitorDataTypes = Union[
    TemperatureData, VoltageData, PotentialData, FreeCarrierData, CapacitanceData
]
