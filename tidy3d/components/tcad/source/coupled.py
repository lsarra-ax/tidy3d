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


class HeatFromElectricSource(GlobalHeatChargeSource):
    """Volumetric heat source generated from an electric simulation.
    If a `HeatFromElectricSource` is specified as a source, appropriate boundary
    conditions for an electric simulation must be provided, since such a simulation
    will be executed before the heat simulation can run.

    Example
    -------
    >>> heat_source = HeatFromElectricSource()
    """
