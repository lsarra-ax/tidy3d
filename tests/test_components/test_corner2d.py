"""Tests 2d corner finder."""

import numpy as np
import shapely
from tidy3d.components.grid.corner_finder import filter_collinear_vertices

np.random.seed(4)


def test_filter_collinear_vertex():
    # 2nd and 3rd vertices are on a collinear line
    poly = shapely.Polygon([[0, 0], [0.1, 0], [0.5, 0], [1, 0], [1, 1]])
    vertices = list(poly.exterior.coords)
    filtered_v = filter_collinear_vertices(vertices)
    assert len(filtered_v) == 3
