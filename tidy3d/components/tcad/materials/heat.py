from typing import Union
import pydantic.v1 as pd
from tidy3d.constants import SPECIFIC_HEAT_CAPACITY, THERMAL_CONDUCTIVITY
from tidy3d.components.tcad.materials.abstract import AbstractHeatChargeSpec


class FluidSpec(AbstractHeatChargeSpec):
    """Fluid medium. Heat simulations will not solve for temperature
    in a structure that has a medium with this 'heat_spec'.

    Example
    -------
    >>> solid = FluidSpec()
    """


class SolidSpec(AbstractHeatChargeSpec):
    """Solid medium for heat simulations.

    Example
    -------
    >>> solid = SolidSpec(
    ...     capacity=2,
    ...     conductivity=3,
    ... )
    """

    capacity: pd.PositiveFloat = pd.Field(
        title="Heat capacity",
        description=f"Volumetric heat capacity in unit of {SPECIFIC_HEAT_CAPACITY}.",
        units=SPECIFIC_HEAT_CAPACITY,
    )

    conductivity: pd.PositiveFloat = pd.Field(
        title="Thermal conductivity",
        description=f"Thermal conductivity of material in units of {THERMAL_CONDUCTIVITY}.",
        units=THERMAL_CONDUCTIVITY,
    )


HeatMaterialTypes = ThermalSpecType = Union[FluidSpec, SolidSpec]
