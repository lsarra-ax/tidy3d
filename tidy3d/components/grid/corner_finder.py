"""Find corners of structures on a 2D plane."""

from typing import List, Literal

import numpy as np

from ...constants import inf
from ..geometry.base import Box, ClipOperation
from ..geometry.utils import merging_geometries_on_plane
from ..medium import PEC, LossyMetalMedium
from ..structure import StructureType
from ..types import ArrayFloat2D, Axis


def filter_collinear_vertices(vertices: ArrayFloat2D, angle_threshold) -> ArrayFloat2D:
    """Filter collinear vertices of a polygon, and return corners.

    Parameters
    ----------
    vertices : ArrayFloat2D
        Polygon vertices from shapely.Polygon. The last vertex is identical to the 1st
        vertex to make a valid polygon.
    angle_threshold : float
        Consider the vertex and its two neighboring two vertices collinear, and the convention that
        the angle is in [0, pi], if the angle formed between them is larger than `pi - angle_threshold`,
        regard them as collinear.

    Returns
    -------
    ArrayFloat2D
        Corner coordinates.
    """

    def normalize(v):
        return v / np.linalg.norm(v, axis=-1)[:, np.newaxis]

    # drop the last vertex, which is identical to the 1st one.
    vs_orig = np.array(vertices[:-1])
    # compute unit vector to next and previous vertex
    vs_next = np.roll(vs_orig, axis=0, shift=-1)
    vs_previous = np.roll(vs_orig, axis=0, shift=+1)
    unit_next = normalize(vs_next - vs_orig)
    unit_previous = normalize(vs_previous - vs_orig)
    # angle
    angle = np.arccos(np.sum(unit_next * unit_previous, axis=-1))
    ind_filter = angle <= np.pi - angle_threshold
    return vs_orig[ind_filter]


def corner_finder(
    normal_axis: Axis,
    coord: float,
    structure_list: List[StructureType],
    mat_type: Literal["metal", "dielectric", "all"],
    angle_threshold: float = 0.1 * np.pi,
) -> ArrayFloat2D:
    """On a 2D plane specified by axis = `normal_axis` and coordinate at `coord`, find out corners of merged
    geometries made of `mat_type`.


    Parameters
    ----------
    normal_axis : Axis
            Axis normal to the 2D plane
        coord : float
                Position of plane along the normal axis.
        structure_list : List[StructureType]
                List of structures present in simulation.
    angle_threshold : float
        Consider the vertex and its two neighboring two vertices collinear, and the convention that
        the angle is in [0, pi], if the angle formed between them is larger than `pi - angle_threshold`,
        regard them as collinear.

    Returns
    -------
    ArrayFloat2D
        Corner coordinates.
    """

    # Construct plane
    center = [0, 0, 0]
    size = [inf, inf, inf]
    center[normal_axis] = coord
    size[normal_axis] = 0
    plane = Box(center=center, size=size)

    geometry_list = [structure.geometry for structure in structure_list]
    # For metal, we don't distinguish between LossyMetal and PEC,
    # so they'll be merged to PEC. Other materials are considered as dielectric.
    medium_list = (structure.medium for structure in structure_list)
    medium_list = [
        PEC if (mat.is_pec or isinstance(mat, LossyMetalMedium)) else mat for mat in medium_list
    ]
    # merge geometries
    merged_geos = merging_geometries_on_plane(geometry_list, plane, medium_list)

    # corner finder here
    corner_list = []
    for mat, shapes in merged_geos:
        if mat_type != "all" and mat.is_pec != (mat_type == "metal"):
            continue
        polygon_list = ClipOperation.to_polygon_list(shapes)
        for poly in polygon_list:
            poly = poly.normalize().buffer(0)
            corner_list.append(
                filter_collinear_vertices(list(poly.exterior.coords), angle_threshold)
            )
            # in case the polygon has holes
            for poly_inner in poly.interiors:
                corner_list.append(
                    filter_collinear_vertices(list(poly_inner.coords), angle_threshold)
                )
    return np.concatenate(corner_list)
