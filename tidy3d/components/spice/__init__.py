"""
This directory includes shared component SPICE definitions that could be compiled from a RF lumped element or a TCAD component.
The idea is that, ultimately, each component model can be compiled into an electrical element cleanly and used to create
a SPICE model.

All of the types in this directory should follow the standards defined in this documentation:
https://ngspice.sourceforge.io/docs/ngspice-manual.pdf
"""

from tidy3d.components.spice.analysis.dc import OperatingPointDC, TransferFunctionDC
from tidy3d.components.spice.components.capacitor import Capacitor
from tidy3d.components.spice.sources.dc import MultiStaticTransferSourceDC, StaticTransferSourceDC
from tidy3d.components.spice.types import ElectricalAnalysisTypes

__all__ = [
    "Capacitor",
    "ElectricalAnalysisTypes",
    "OperatingPointDC",
    "MultiStaticTransferSourceDC",
    "StaticTransferSourceDC",
    "TransferFunctionDC",
]
