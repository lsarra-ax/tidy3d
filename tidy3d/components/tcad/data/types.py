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
from tidy3d.components.tcad.data.monitor_data.abstract import (
    SpatialDataArray,
)

HeatChargeMonitorDataTypes = Union[
    TemperatureData, VoltageData, PotentialData, FreeCarrierData, CapacitanceData
]

FieldDataset = FieldDatasetTypes = Union[
    SpatialDataArray, annotate_type(Union[TriangularGridDataset, TetrahedralGridDataset])
]
