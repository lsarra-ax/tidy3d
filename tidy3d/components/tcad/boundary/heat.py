"""Defines heat material specifications"""

from __future__ import annotations

from abc import ABC
from typing import Tuple, Union

import pydantic.v1 as pd

from tidy3d.constants import CURRENT_DENSITY, HEAT_FLUX, HEAT_TRANSFER_COEFF, KELVIN, VOLT
from tidy3d.components.base import Tidy3dBaseModel
from tidy3d.components.bc_placement import BCPlacementType
from tidy3d.components.types import TYPE_TAG_STR


class TemperatureBC(HeatChargeBC):
    """Constant temperature thermal boundary conditions.

    Example
    -------
    >>> bc = TemperatureBC(temperature=300)
    """

    temperature: pd.PositiveFloat = pd.Field(
        title="Temperature",
        description=f"Temperature value in units of {KELVIN}.",
        units=KELVIN,
    )


class HeatFluxBC(HeatChargeBC):
    """Constant flux thermal boundary conditions.

    Example
    -------
    >>> bc = HeatFluxBC(flux=1)
    """

    flux: float = pd.Field(
        title="Heat Flux",
        description=f"Heat flux value in units of {HEAT_FLUX}.",
        units=HEAT_FLUX,
    )


class ConvectionBC(HeatChargeBC):
    """Convective thermal boundary conditions.

    Example
    -------
    >>> bc = ConvectionBC(ambient_temperature=300, transfer_coeff=1)
    """

    ambient_temperature: pd.PositiveFloat = pd.Field(
        title="Ambient Temperature",
        description=f"Ambient temperature value in units of {KELVIN}.",
        units=KELVIN,
    )

    transfer_coeff: pd.NonNegativeFloat = pd.Field(
        title="Heat Transfer Coefficient",
        description=f"Heat flux value in units of {HEAT_TRANSFER_COEFF}.",
        units=HEAT_TRANSFER_COEFF,
    )
