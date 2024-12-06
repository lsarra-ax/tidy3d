"""Defines heat material specifications"""

from __future__ import annotations

from abc import ABC
from typing import Tuple, Union

import pydantic.v1 as pd

from tidy3d.constants import CURRENT_DENSITY, HEAT_FLUX, HEAT_TRANSFER_COEFF, KELVIN, VOLT
from tidy3d.components.base import Tidy3dBaseModel
from tidy3d.components.bc_placement import BCPlacementType
from tidy3d.components.types import TYPE_TAG_STR


class HeatChargeBC(ABC, Tidy3dBaseModel):
    """Abstract heat-charge boundary conditions."""