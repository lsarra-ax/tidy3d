from typing import Union
from tidy3d.components.tcad.source.heat import HeatSource,UniformHeatSource
from tidy3d.components.tcad.source.coupled import HeatFromElectricSource

HeatChargeSourceType = Union[HeatSource, HeatFromElectricSource, UniformHeatSource]
