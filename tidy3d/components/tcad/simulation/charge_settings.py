"""File containing classes required for the setup of a DEVSIM case."""

from abc import ABC
from typing import Optional

import pydantic.v1 as pd

from tidy3d.constants import VOLT
from tidy3d.components.base import Tidy3dBaseModel
from tidy3d.components.types import Union


class AbstractDevsimStruct(ABC, Tidy3dBaseModel):
    """"""


class ChargeToleranceSpec(Tidy3dBaseModel):
    """This class sets some Charge tolerance parameters.

    Example
    -------
    >>> import tidy3d as td
    >>> charge_settings = td.ChargeToleranceSpec(abs_tol=1e8, rel_tol=1e-10, max_iters=30)
    """

    abs_tol: Optional[pd.PositiveFloat] = pd.Field(
        default=1e10,
        title="Absolute tolerance.",
        description="Absolute tolerance used as stop criteria when converging towards a solution.",
    )

    rel_tol: Optional[pd.PositiveFloat] = pd.Field(
        default=1e-10,
        title="Relative tolerance.",
        description="Relative tolerance used as stop criteria when converging towards a solution.",
    )

    max_iters: Optional[pd.PositiveInt] = pd.Field(
        default=30,
        title="Maximum number of iterations.",
        description="Indicates the maximum number of iterations to be run. "
        "The solver will stop either when this maximum of iterations is met "
        "or when the tolerance criteria has been met.",
    )




# TODO: implement future classes for unsteady regimes SmallSignalSpec & NonlinearUnsteadySpec



ChargeToleranceType = Union[ChargeToleranceSpec]
ChargeRegimeType = Union[DCSpec]
MobilityModelType = Union[CaugheyThomasMobility]
RecombinationModelType = Union[AugerRecombination, RadiativeRecombination, SRHRecombination]
BandgapNarrowingModelType = Union[SlotboomNarrowingModel]
