import pydantic.v1 as pd

from tidy3d.components.base import Tidy3dBaseModel


# Generation-Recombination models
class AugerRecombination(Tidy3dBaseModel):
    # TODO the ideal case here, is if we could use some of Yannick's serializable operations for this model
    #  calculation, but it's priorityt o get this out soon.
    """This class defines the parameters for the Auger recombination model.
    NOTE: default parameters are those appropriate for Silicon."""

    electrons_constant: pd.PositiveFloat = pd.Field(
        2.8e-31, title="Constant for electrons", description="Constant for electrons in cm^6/s"
    )
    c_n = electrons_constant

    holes_constant: pd.PositiveFloat = pd.Field(
        9.9e-32, title="Constant for holes", description="Constant for holes in cm^6/s"
    )
    c_p = holes_constant


class RadiativeRecombination(Tidy3dBaseModel):
    # TODO the ideal case here, is if we could use some of Yannick's serializable operations for this model
    #  calculation, but it's priorityt o get this out soon.
    """This class is used to define the parameters for the radiative recombination model.
    NOTE: default values are those appropriate for Silicon."""

    radiation_constant: float = pd.Field(
        1.6e-14,
        title="Radiation constant in cm^3/s",
        description="Radiation constant in cm^3/s",
    )
    r_const = radiation_constant


class ShockleyReedHallRecombination(Tidy3dBaseModel):
    # TODO the ideal case here, is if we could use some of Yannick's serializable operations for this model
    #  calculation, but it's priorityt o get this out soon.
    """This class defines the parameters for the Shockley-Reed-Hall recombination model.
    NOTE: currently, lifetimes are considered constant (not dependent on temp. nor doping)
    NOTE: default values are those appropriate for Silicon."""

    electron_lifetime: pd.PositiveFloat = pd.Field(
        3.3e-6, title="Electron lifetime.", description="Electron lifetime."
    )
    tau_n = electron_lifetime

    hole_lifetime: pd.PositiveFloat = pd.Field(
        4e-6, title="Hole lifetime.", description="Hole lifetime."
    )
    tau_p = hole_lifetime
