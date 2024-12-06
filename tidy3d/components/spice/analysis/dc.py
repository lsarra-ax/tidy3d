"""
This class defines standard SPICE analysis types (electrical simulations configurations).
"""
import pydantic.v1 as pd
from typing import Optional
from tidy3d.components.base import Tidy3dBaseModel


class OperatingPointDC(Tidy3dBaseModel):
    """
    Equivalent to Section 11.1.2 in the ngspice manual.
    """


class TransferFunctionDC(Tidy3dBaseModel):
    """This class sets parameters used in DC simulations.

    Equivalent to Section 11.3.2 in the ngspice manual.

    Example
    -------
    >>> import tidy3d as td
    >>> dc_spec = td.DCSpec(dv=0.1)
    """

    dv: Optional[pd.PositiveFloat] = pd.Field(
        1.0,
        title="Bias step.",
        description="By default, a solution is computed at 0 bias. "
                    "If a bias different than 0 is requested, DEVSIM will start at 0 and increase bias "
                    "at 'dV' intervals until the required bias is reached. ",
    )
