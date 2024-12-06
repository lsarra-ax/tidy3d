"""Useful utilities."""

import numpy as np

from ..constants import inf


def increment_float(val: float, sign: float, dtype=np.float32) -> float:
    """Applies a small positive or negative shift as though `val`
    using numpy.nextafter, but additionally handles some corner cases.
    """
    # Infinity is left unchanged
    if val == inf or val == -inf:
        return val

    if sign >= 0:
        sign = 1
    else:
        sign = -1

    # Avoid small increments within subnormal values
    if np.abs(val) <= np.finfo(dtype).tiny:
        return val + sign * np.finfo(dtype).tiny

    # Numpy seems to skip over the increment from -0.0 and +0.0
    # which is different from c++
    return np.nextafter(val, sign * inf, dtype=dtype)
