"""Tests RF monitors."""

import numpy as np
from tidy3d.components.microwave.monitor import VoltageMonitor


def test_create():
    freqs = np.linspace(1e9, 1e11, 101)
    V_mon = VoltageMonitor(freqs=freqs, name="what")
