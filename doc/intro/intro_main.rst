Introduction
============

Overview
--------

OMOTES.SIMULATOR_CORE is the simulation engine used to evaluate thermo-hydraulic behavior in
district heating systems. Given a network description in ESDL format, a start/stop time, and a
timestep, it computes how hydraulic and thermal state evolves over the simulation period and
returns the result as a time series.

What It Does
------------

The package combines four things to produce a result: network topology, asset physics, control
setpoints, and solver execution. At each timestep, setpoints are applied, the network equations are
assembled and solved, and the resulting state is recorded.

In scope:

- Time-stepped simulation of hydraulic and thermal behavior
- Integration of network topology, asset physics, and controller setpoints
- Deterministic results for a given model and run configuration

Out of scope:

- Interactive visualization dashboards and scenario authoring tools
- Site-specific deployment and operational orchestration
- Generic data platform concerns not required for simulation execution

Why It Is Used
---------------

The package is used to study how a district-heating system behaves under changing demand, network
conditions, and control decisions:

- **End users and modelers** compare scenarios and interpret operational behavior — whether a
  configuration meets demand, or how a control strategy affects system response.
- **Integrators** connect simulation runs to surrounding tooling and workflows.
- **Contributors** extend package capabilities while preserving simulation correctness.

Example
-------

A run is defined by an ESDL model and a time configuration, and returns a pandas ``DataFrame`` of
results:

.. code-block:: python

   from omotes_simulator_core.entities.esdl_object import EsdlObject
   from omotes_simulator_core.entities.simulation_configuration import SimulationConfiguration
   from omotes_simulator_core.infrastructure.simulation_manager import SimulationManager
   from omotes_simulator_core.infrastructure.utils import pyesdl_from_file

   config = SimulationConfiguration(
       simulation_id=uuid.uuid1(),
       name="test run",
       timestep=3600,
       start=datetime.strptime("2019-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S"),
       stop=datetime.strptime("2019-01-01T01:00:00", "%Y-%m-%dT%H:%M:%S"),
   )

   sim = SimulationManager(EsdlObject(pyesdl_from_file("path/to/file.esdl")), config)
   result = sim.execute(progressLogger)

The ESDL model is loaded and wrapped as an ``EsdlObject``; run parameters (start/stop, timestep)
are captured in a ``SimulationConfiguration``; ``SimulationManager`` ties the two together; and
``execute`` runs the timestep loop and returns the result ``DataFrame``. See ``README.md`` for the
full runnable example, including progress reporting.

Related Documentation
----------------------

- :doc:`../solver/solver_main` for solver behavior and numerical execution.
- :doc:`../network/network_main` for network representation and connectivity concepts.
- :doc:`../physics/physics_main` for asset-level physical relations.
- :doc:`../controller/controller` for control concepts and setpoint behavior.
- :doc:`../developer/developer_main` for contributor and API-oriented material.
- :doc:`../support/support` for support and issue-reporting guidance.

For project context and standards, see the `NWN website`_ and `ESDL`_.

.. _NWN website: https://www.nwn.nu/
.. _ESDL: https://www.esdl.nl/
