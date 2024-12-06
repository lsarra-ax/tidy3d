"""Defines heat material specifications"""

from __future__ import annotations

from abc import ABC
from typing import Tuple

import pydantic.v1 as pd

from tidy3d.constants import (
    CONDUCTIVITY,
    ELECTRON_VOLT,
    PERMITTIVITY,
    SPECIFIC_HEAT_CAPACITY,
    THERMAL_CONDUCTIVITY,
)
from tidy3d.base import Tidy3dBaseModel
from tidy3d.data.data_array import SpatialDataArray
from tidy3d.heat_charge.charge_settings import (
    AugerRecombination,
    BandgapNarrowingModelType,
    CaugheyThomasMobility,
    MobilityModelType,
    RadiativeRecombination,
    RecombinationModelType,
    SlotboomNarrowingModel,
    SRHRecombination,
)
from tidy3d.types import Union


# Liquid class
class AbstractHeatChargeSpec(ABC, Tidy3dBaseModel):
    """Abstract heat material specification."""
