"""Defines heat-charge material specifications for 'HeatChargeSimulation'"""

from __future__ import annotations

from abc import ABC
from typing import Tuple, Union

import pydantic.v1 as pd

from tidy3d.constants import VOLUMETRIC_HEAT_RATE
from tidy3d.exceptions import SetupError
from tidy3d.log import log
from tidy3d.components.base import cached_property
from tidy3d.components.base_sim.source import AbstractSource
from tidy3d.components.viz import PlotParams
from tidy3d.components.tcad.viz import plot_params_heat_source
from tidy3d.components.tcad.source.abstract import StructureBasedHeatChargeSource


class HeatSource(StructureBasedHeatChargeSource):
    """Adds a volumetric heat source (heat sink if negative values
    are provided) to specific structures in the scene.

    Example
    -------
    >>> heat_source = HeatSource(rate=1, structures=["box"])
    """

    rate: Union[float] = pd.Field(
        title="Volumetric Heat Rate",
        description="Volumetric rate of heating or cooling (if negative) in units of "
        f"{VOLUMETRIC_HEAT_RATE}.",
        units=VOLUMETRIC_HEAT_RATE,
    )


class UniformHeatSource(HeatSource):
    """Volumetric heat source. This class is deprecated. You can use
    'HeatSource' instead.

    Example
    -------
    >>> heat_source = UniformHeatSource(rate=1, structures=["box"]) # doctest: +SKIP
    """

    # NOTE: wrapper for backwards compatibility.

    @pd.root_validator(skip_on_failure=True)
    def issue_warning_deprecated(cls, values):
        """Issue warning for 'UniformHeatSource'."""
        log.warning(
            "'UniformHeatSource' is deprecated and will be discontinued. You can use "
            "'HeatSource' instead."
        )
        return values

