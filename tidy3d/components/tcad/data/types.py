from typing import Union

from tidy3d.components.tcad.data.monitor_data.charge import (
    StaticCapacitanceData,
    StaticChargeCarrierData,
    # PotentialData,
    StaticVoltageData,
)
from tidy3d.components.tcad.data.monitor_data.heat import TemperatureData

HeatChargeMonitorDataTypes = Union[
    TemperatureData,
    StaticVoltageData,
    StaticChargeCarrierData,
    StaticCapacitanceData,  # PotentialData
]
