# utilities for autograd derivative passing
from __future__ import annotations

import numpy as np
import pydantic.v1 as pd
import xarray as xr

from ..base import Tidy3dBaseModel
from ..data.data_array import ScalarFieldDataArray
from ..types import ArrayLike, Bound, tidycomplex
from .types import PathType
from .utils import get_static

# we do this because importing these creates circular imports
FieldData = dict[str, ScalarFieldDataArray]
PermittivityData = dict[str, ScalarFieldDataArray]


class DerivativeSurfaceMesh(Tidy3dBaseModel):
    """Stores information about the surfaces of an object to be used for derivative calculation."""

    centers: ArrayLike = pd.Field(
        ...,
        title="Centers",
        description="(N, 3) array storing the centers of each surface element.",
    )

    areas: ArrayLike = pd.Field(
        ...,
        title="Area Elements",
        description="(N,) array storing the first perpendicular vectors of each surface element.",
    )

    normals: ArrayLike = pd.Field(
        ...,
        title="Normals",
        description="(N, 3) array storing the normal vectors of each surface element.",
    )

    perps1: ArrayLike = pd.Field(
        ...,
        title="Perpendiculars 1",
        description="(N, 3) array storing the first perpendicular vectors of each surface element.",
    )

    perps2: ArrayLike = pd.Field(
        ...,
        title="Perpendiculars 1",
        description="(N, 3) array storing the first perpendicular vectors of each surface element.",
    )


class DerivativeInfo(Tidy3dBaseModel):
    """Stores derivative information passed to the ``.compute_derivatives`` methods."""

    paths: list[PathType] = pd.Field(
        ...,
        title="Paths to Traced Fields",
        description="List of paths to the traced fields that need derivatives calculated.",
    )

    E_der_map: FieldData = pd.Field(
        ...,
        title="Electric Field Gradient Map",
        description='Dataset where the field components ``("Ex", "Ey", "Ez")`` store the '
        "multiplication of the forward and adjoint electric fields. The tangential components "
        "of this dataset is used when computing adjoint gradients for shifting boundaries. "
        "All components are used when computing volume-based gradients.",
    )

    D_der_map: FieldData = pd.Field(
        ...,
        title="Displacement Field Gradient Map",
        description='Dataset where the field components ``("Ex", "Ey", "Ez")`` store the '
        "multiplication of the forward and adjoint displacement fields. The normal component "
        "of this dataset is used when computing adjoint gradients for shifting boundaries.",
    )

    E_fwd: FieldData = pd.Field(
        ...,
        title="Forward Electric Fields",
        description='Dataset where the field components ``("Ex", "Ey", "Ez")`` represent the '
        "forward electric fields used for computing gradients for a given structure.",
    )

    E_adj: FieldData = pd.Field(
        ...,
        title="Adjoint Electric Fields",
        description='Dataset where the field components ``("Ex", "Ey", "Ez")`` represent the '
        "adjoint electric fields used for computing gradients for a given structure.",
    )

    D_fwd: FieldData = pd.Field(
        ...,
        title="Forward Displacement Fields",
        description='Dataset where the field components ``("Ex", "Ey", "Ez")`` represent the '
        "forward displacement fields used for computing gradients for a given structure.",
    )

    D_adj: FieldData = pd.Field(
        ...,
        title="Adjoint Displacement Fields",
        description='Dataset where the field components ``("Ex", "Ey", "Ez")`` represent the '
        "adjoint displacement fields used for computing gradients for a given structure.",
    )

    eps_data: PermittivityData = pd.Field(
        ...,
        title="Permittivity Dataset",
        description="Dataset of relative permittivity values along all three dimensions. "
        "Used for automatically computing permittivity inside or outside of a simple geometry.",
    )

    eps_in: tidycomplex = pd.Field(
        title="Permittivity Inside",
        description="Permittivity inside of the ``Structure``. "
        "Typically computed from ``Structure.medium.eps_model``."
        "Used when it can not be computed from ``eps_data`` or when ``eps_approx==True``.",
    )

    eps_out: tidycomplex = pd.Field(
        ...,
        title="Permittivity Outside",
        description="Permittivity outside of the ``Structure``. "
        "Typically computed from ``Simulation.medium.eps_model``."
        "Used when it can not be computed from ``eps_data`` or when ``eps_approx==True``.",
    )

    bounds: Bound = pd.Field(
        ...,
        title="Geometry Bounds",
        description="Bounds corresponding to the structure, used in ``Medium`` calculations.",
    )

    bounds_intersect: Bound = pd.Field(
        ...,
        title="Geometry and Simulation Intersections Bounds",
        description="Bounds corresponding to the minimum intersection between the "
        "structure and the simulation it is contained in."
        "",
    )

    frequency: float = pd.Field(
        ...,
        title="Frequency of adjoint simulation",
        description="Frequency at which the adjoint gradient is computed.",
    )

    eps_approx: bool = pd.Field(
        False,
        title="Use Permittivity Approximation",
        description="If ``True``, approximates outside permittivity using ``Simulation.medium``"
        "and the inside permittivity using ``Structure.medium``. "
        "Only set ``True`` for ``GeometryGroup`` handling where it is difficult to automatically "
        "evaluate the inside and outside relative permittivity for each geometry.",
    )

    def updated_paths(self, paths: list[PathType]) -> DerivativeInfo:
        """Update this ``DerivativeInfo`` with new set of paths."""
        return self.updated_copy(paths=paths)

    @property
    def delta_eps(self) -> complex:
        return self.eps_in - self.eps_out

    @property
    def delta_eps_inv(self) -> complex:
        return 1.0 / self.eps_in - 1.0 / self.eps_out

    def grad_surfaces(self, surface_mesh: DerivativeSurfaceMesh) -> dict:
        """Derivative with respect to the surface mesh elements, given the derivative fields."""

        # strip out relevant info from `surface_mesh`
        spatial_coords = surface_mesh.centers
        normals = surface_mesh.normals
        perps1 = surface_mesh.perps1
        perps2 = surface_mesh.perps2

        # unpack electric and displacement fields
        E_fwd = self.E_fwd
        E_adj = self.E_adj
        D_fwd = self.D_fwd
        D_adj = self.D_adj

        # compute the E and D fields at the edge centers
        E_fwd_at_coords = self.evaluate_flds_at(fld_dataset=E_fwd, spatial_coords=spatial_coords)
        E_adj_at_coords = self.evaluate_flds_at(fld_dataset=E_adj, spatial_coords=spatial_coords)
        D_fwd_at_coords = self.evaluate_flds_at(fld_dataset=D_fwd, spatial_coords=spatial_coords)
        D_adj_at_coords = self.evaluate_flds_at(fld_dataset=D_adj, spatial_coords=spatial_coords)

        # project the relevant field quantities into their respective basis for gradient calculation
        D_fwd_norm = self.project_in_basis(D_fwd_at_coords, basis_vector=normals)
        D_adj_norm = self.project_in_basis(D_adj_at_coords, basis_vector=normals)

        E_fwd_perp1 = self.project_in_basis(E_fwd_at_coords, basis_vector=perps1)
        E_adj_perp1 = self.project_in_basis(E_adj_at_coords, basis_vector=perps1)

        E_fwd_perp2 = self.project_in_basis(E_fwd_at_coords, basis_vector=perps2)
        E_adj_perp2 = self.project_in_basis(E_adj_at_coords, basis_vector=perps2)

        # multiply forward and adjoint
        D_der_norm = D_fwd_norm * D_adj_norm
        E_der_perp1 = E_fwd_perp1 * E_adj_perp1
        E_der_perp2 = E_fwd_perp2 * E_adj_perp2

        # approximate permittivity in and out
        delta_eps_inv = self.delta_eps_inv
        delta_eps = self.delta_eps

        # put together VJP using D_normal and E_perp integration
        vjps = 0.0

        # perform D-normal integral
        contrib_D = -delta_eps_inv * D_der_norm
        vjps += contrib_D

        # import pdb; pdb.set_trace()

        # perform E-perpendicular integrals
        for E_der in (E_der_perp1, E_der_perp2):
            contrib_E = E_der * delta_eps
            vjps += contrib_E

        return surface_mesh.areas * vjps

    @staticmethod
    def evaluate_flds_at(
        fld_dataset: dict[str, ScalarFieldDataArray],
        spatial_coords: np.ndarray,  # (N, 3)
    ) -> dict[str, ScalarFieldDataArray]:
        """Compute the value of an dict with keys Ex, Ey, Ez at a set of spatial locations."""

        xs, ys, zs = spatial_coords.T
        edge_index_dim = "edge_index"

        sum_dims = []
        interp_kwargs = {}
        for dim, locations_dim in zip("xyz", (xs, ys, zs)):
            # only include dims where the data has more than 1 coord, to avoid warnings and errors
            if False and any(np.array(fld.coords[dim]).size == 1 for fld in fld_dataset.values()):
                sum_dims.append(dim)
            else:
                interp_kwargs[dim] = xr.DataArray(locations_dim, dims=edge_index_dim)

        components = {}
        for fld_name, arr in fld_dataset.items():
            components[fld_name] = (
                arr.interp(**interp_kwargs, assume_sorted=True, kwargs=dict(fill_value=None))
                .sum("f")
                .sum(sum_dims)
            )

        # import pdb; pdb.set_trace()

        return components

    @staticmethod
    def project_in_basis(
        der_dataset: xr.Dataset,
        basis_vector: np.ndarray,
    ) -> xr.DataArray:
        """Project a derivative dataset along a supplied basis vector."""

        value = 0.0
        for coeffs, dim in zip(basis_vector.T, "xyz"):
            value += coeffs * der_dataset[f"E{dim}"]
        return value


# TODO: could we move this into a DataArray method?
def integrate_within_bounds(arr: xr.DataArray, dims: list[str], bounds: Bound) -> xr.DataArray:
    """integrate a data array within bounds, assumes bounds are [2, N] for N dims."""

    # order bounds with dimension first (N, 2)
    bounds = np.asarray(bounds).T
    all_coords = {}

    # loop over all dimensions
    for dim, (bmin, bmax) in zip(dims, bounds):
        bmin = get_static(bmin)
        bmax = get_static(bmax)

        coord_values = np.copy(arr.coords[dim].data)

        # reset all coordinates outside of bounds to the bounds, so that dL = 0 in integral
        np.clip(coord_values, bmin, bmax, out=coord_values)

        all_coords[dim] = coord_values

    _arr = arr.assign_coords(**all_coords)

    # uses trapezoidal rule
    # https://docs.xarray.dev/en/stable/generated/xarray.DataArray.integrate.html
    dims_integrate = [dim for dim in dims if len(_arr.coords[dim]) > 1]
    return _arr.integrate(coord=dims_integrate)


__all__ = [
    "integrate_within_bounds",
    "DerivativeInfo",
]
