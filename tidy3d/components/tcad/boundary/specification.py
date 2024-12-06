


class HeatChargeBoundarySpec(Tidy3dBaseModel):
    """Heat-Charge boundary conditions specification.

    Example
    -------
    >>> from tidy3d import SimulationBoundary
    >>> bc_spec = HeatBoundarySpec(
    ...     placement=SimulationBoundary(),
    ...     condition=ConvectionBC(ambient_temperature=300, transfer_coeff=1),
    ... )
    """

    placement: BCPlacementType = pd.Field(
        title="Boundary Conditions Placement",
        description="Location to apply boundary conditions.",
        discriminator=TYPE_TAG_STR,
    )

    condition: HeatChargeBoundaryConditionType = pd.Field(
        title="Boundary Conditions",
        description="Boundary conditions to apply at the selected location.",
        discriminator=TYPE_TAG_STR,
    )


class HeatBoundarySpec(HeatChargeBoundarySpec):
    """Heat BC specification
    NOTE: here for backward-compatibility only."""
