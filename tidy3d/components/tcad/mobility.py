import pydantic.v1 as pd

from tidy3d.components.base import Tidy3dBaseModel


# Mobility models
class CaugheyThomasMobility(Tidy3dBaseModel):
    # TODO the ideal case here, is if we could use some of Yannick's serializable operations for this model
    #  calculation, but it's priorityt o get this out soon.
    """
    This class defines the parameters for the mobility model of Caughey and Thomas.
    NOTE: high electric field effects not yet supported.
    NOTE: Default values are those appropriate for Silicon.
    """

    # mobilities
    minimum_electron_mobility: pd.PositiveFloat = pd.Field(
        52.2,
        title="Minimum electron mobility",
        description="Minimum electron mobility at reference temperature (300K) in cm^2/V-s. ",
    )
    mu_n_min = minimum_electron_mobility

    reference_electron_mobility: pd.PositiveFloat = pd.Field(
        1471.0,
        title="Electron reference mobility",
        description="Reference electron mobility at reference temperature (300K) in cm^2/V-s",
    )
    mu_n = reference_electron_mobility

    minimum_hole_mobility: pd.PositiveFloat = pd.Field(
        44.9,
        title="Minimum hole mobility",
        description="Minimum hole mobility at reference temperature (300K) in cm^2/V-s. ",
    )
    mu_p_min = minimum_hole_mobility

    reference_hole_mobility: pd.PositiveFloat = pd.Field(
        470.5,
        title="Hole reference mobility",
        description="Reference hole mobility at reference temperature (300K) in cm^2/V-s",
    )
    mu_p = reference_hole_mobility

    # thermal exponent for reference mobility
    exp_t_mu: float = pd.Field(
        -2.33, title="Exponent for temperature dependent behavior of reference mobility"
    )

    # doping exponent
    exponent_doping_electron_mobility: pd.PositiveFloat = pd.Field(
        0.68,
        title="Exponent for doping dependence of electron mobility.",
        description="Exponent for doping dependence of electron mobility at reference temperature (300K).",
    )
    exp_d_n = exponent_doping_electron_mobility

    exponent_doping_hole_mobility: pd.PositiveFloat = pd.Field(
        0.719,
        title="Exponent for doping dependence of hole mobility.",
        description="Exponent for doping dependence of hole mobility at reference temperature (300K).",
    )
    exp_d_p = exponent_doping_hole_mobility

    # reference doping
    reference_doping_273K: pd.PositiveFloat = pd.Field(
        2.23e17,
        title="Reference doping",
        description="Reference doping at reference temperature (300K) in #/cm^3.",
    )
    N_ref = reference_doping_273K

    # temperature exponent
    exponent_temperature_minimum_mobility: float = pd.Field(
        -0.57,
        title="Exponent of thermal dependence of minimum mobility.",
        description="Exponent of thermal dependence of minimum mobility.",
    )
    exp_t_mu_min = exponent_temperature_minimum_mobility

    exponent_temperature_reference_doping: float = pd.Field(
        2.4,
        title="Exponent of thermal dependence of reference doping.",
        description="Exponent of thermal dependence of reference doping.",
    )
    exp_t_d = exponent_temperature_reference_doping

    exponent_temperature_doping_effect: float = pd.Field(
        -0.146,
        title="Exponent of thermal dependence of the doping exponent effect.",
        description="Exponent of thermal dependence of the doping exponent effect.",
    )
    exp_t_d_exp = exponent_temperature_doping_effect
