"""
This directory corresponds to the standard electronic interfaces that should be shared across multiple solvers.

The aim is to provide a standard translation interface between SPICE solvers and our own solvers.
Note: the API definitions in this section correspond to electronic frequencies (ie sub terahertz and that
can be represented by standard electronic circuit elements (including RF lumped elements).

In order to have the option to eventually break off the packages into more maintainable subpackages, all the relevant
types will be contained within this sublevel __init__.py
"""
from tidy3d.components.tcad.bandgap import SlotboomNarrowingBandGap
from tidy3d.components.tcad.boundary.heat import (
    ConvectionBC,
    HeatFluxBC,
    TemperatureBC
)
from tidy3d.components.tcad.boundary.specification import (
    HeatBoundarySpec,
    HeatChargeBoundarySpec
)
from tidy3d.components.tcad.boundary.charge import (
    CurrentBC,
    VoltageBC,
    InsulatingBC
)
from tidy3d.components.tcad.data.monitor_data.heat import (
    TemperatureData
)
from tidy3d.components.tcad.data.monitor_data.charge import (
    CapacitanceData,
    FreeCarrierData,
    DCCapacitanceDataArray,
    VoltageData,
    PotentialData
)
from tidy3d.components.tcad.data.monitor_data.abstract import (
    HeatChargeMonitorData,
)
from tidy3d.components.tcad.data.sim_data import (
    HeatChargeSimulationData,
    HeatSimulationData
)
from tidy3d.components.tcad.generation_recombination import (
    AugerRecombination,
    RadiativeRecombination,
    ShockleyReedHallRecombination
)
from tidy3d.components.tcad.grid import (
    DistanceUnstructuredGrid,
    UniformUnstructuredGrid,
)
from tidy3d.components.tcad.mobility import (
    CaugheyThomasMobility
)
from tidy3d.components.tcad.monitors.heat import (
    TemperatureMonitor,
)
from tidy3d.components.tcad.monitors.abstract import (
    HeatChargeMonitor
)
from tidy3d.components.tcad.monitors.charge import (
    CapacitanceMonitor,
    VoltageMonitor,
    FreeCarrierMonitor
)
from tidy3d.components.tcad.grid import (
    UniformUnstructuredGrid,
    DistanceUnstructuredGrid
)
from tidy3d.components.tcad.simulation.heat_charge import (
    HeatChargeSimulation
)
from tidy3d.components.tcad.simulation.heat import (
    HeatSimulation
)
from tidy3d.components.tcad.source.heat import (
    HeatSource,
    UniformHeatSource,
)
from tidy3d.components.tcad.source.coupled import (
    HeatFromElectricSource,
    GlobalHeatChargeSource
)

# tcad
# from tidy3d.components.tcad import (
#     DCSpec,
# )