from typing import Union

import pydantic.v1 as pd

from tidy3d.components.data.data_array import SpatialDataArray
from tidy3d.components.tcad.bandgap import SlotboomNarrowingBandGap
from tidy3d.components.tcad.generation_recombination import (
    AugerRecombination,
    RadiativeRecombination,
    ShockleyReedHallRecombination,
)
from tidy3d.components.tcad.materials.abstract import AbstractHeatChargeSpec
from tidy3d.components.tcad.mobility import CaugheyThomasMobility
from tidy3d.components.tcad.types import (
    BandGapModelTypes,
    MobilityModelTypes,
    RecombinationModelTypes,
)
from tidy3d.constants import ELECTRON_VOLT


class ElectronicSpec(AbstractHeatChargeSpec):
    # TODO does this account for the whole temporal dynamics? If not then it should be called ElectroStatic, which it was called before, but unsure why it got changed?
    """
    This class is used to define electro-static semiconductors.

    Notes
    -----
        Both acceptors and donors can be either a positive number or an 'xarray.DataArray'.
        Default values for parameters and models are those appropriate for Silicon
    """

    electrons_effective_density: pd.PositiveFloat = pd.Field(
        2.86e19,
        title="Effective density of electron states",
        description="Effective density of electron states",
        units="cm^(-3)",
    )
    N_e = electrons_effective_density

    holes_effective_density: pd.PositiveFloat = pd.Field(
        3.1e19,
        title="Effective density of hole states",
        description="Effective density of hole states",
        units="cm^(-3)",
    )
    N_v = holes_effective_density

    bandgap_energy: pd.PositiveFloat = pd.Field(
        1.11,
        title="Band-gap energy",
        description="Band-gap energy",
        units=ELECTRON_VOLT,
    )
    E_g = bandgap_energy

    electron_affinity: float = pd.Field(
        4.05, title="Electron affinity", description="Electron affinity", units=ELECTRON_VOLT
    )

    mobility: MobilityModelTypes = pd.Field(
        CaugheyThomasMobility(),
        title="Mobility model",
        description="Mobility model",
    )

    recombination_generation: tuple[RecombinationModelTypes, ...] = pd.Field(
        (ShockleyReedHallRecombination(), AugerRecombination(), RadiativeRecombination()),
        title="Recombination models",
        description="Array containing the recombination models to be applied to the material.",
    )

    bandgap: BandGapModelTypes = pd.Field(
        SlotboomNarrowingBandGap(),
        title="Bandgap narrowing model.",
        description="Bandgap narrowing model.",
    )

    acceptors: Union[pd.NonNegativeFloat, SpatialDataArray] = pd.Field(
        0,
        title="Doping: Acceptor concentration",
        description="Units of 1/cm^3",
        units="1/cm^3",
    )

    donors: Union[pd.NonNegativeFloat, SpatialDataArray] = pd.Field(
        0,
        title="Doping: Donor concentration",
        description="Units of 1/cm^3",
        units="1/cm^3",
    )
    # TODO add shorthand if desired.


# in the future we have ElectroDynamicSpec

ChargeMaterialTypes = ElectricSpecType = ElectronicSpec
