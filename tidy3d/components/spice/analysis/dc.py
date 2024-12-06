"""
This class defines standard SPICE analysis types (electrical simulations configurations).
"""
import pydantic.v1 as pd
from typing import Optional
from tidy3d.components.base import Tidy3dBaseModel
from tidy3d.components.spice.sources.dc import SourceDC, MultiSourceDC


class OperatingPointDC(Tidy3dBaseModel):
    """
    Equivalent to Section 11.1.2 in the ngspice manual.
    """


class TransferFunctionDC(Tidy3dBaseModel):
    """This class sets parameters used in DC simulations.

    Ultimately, equivalent to Section 11.3.2 in the ngspice manual.

    Example
    -------
    TODOUPDATE Example.
    >>> import tidy3d as td
    >>> dc_spec = td.TransferFunctionDC(dv=0.1)
    """
    sources: SourceDC | MultiSourceDC = []
