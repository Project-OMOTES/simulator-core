Introduction
============

Overview
--------

OMOTES.SIMULATOR_CORE is the simulation package used to evaluate thermo-hydraulic behavior in district
heating systems. It provides the package-level entry point for understanding what the simulator does,
how the main subsystems fit together, and how to interpret the results that come out of a run.

What OMOTES.SIMULATOR_CORE Does
------------------------------

The package turns a time-based system description into simulation results. In practice, it combines the
network structure, asset behavior, control setpoints, and solver execution needed to compute how the
system evolves over time.

This introductory section keeps the focus on the overall package rather than on implementation detail.
Use it to understand the scope of the simulator before moving into the solver, network, physics, and
control sections.

Why It Is Used
--------------

The package is used when you need to study how a district-heating system behaves under changing demand,
network conditions, and control decisions. It supports modelers and integrators who want to compare
scenarios, interpret operational behavior, or connect simulation results to surrounding tooling.

Typical use is to answer questions such as whether a configuration can meet demand, how a control
strategy affects system response, or what thermal and hydraulic trends appear over a simulation period.

Contents
--------

.. toctree::
   :maxdepth: 1

   package_scope
   audience_and_use_cases
   simulation_input_and_output

Related Documentation
---------------------

For the next level of detail, see:

- :doc:`../solver/solver_main` for solver behavior and numerical execution.
- :doc:`../network/network_main` for network representation and connectivity concepts.
- :doc:`../physics/physics_main` for asset-level physical relations.
- :doc:`../controller/controller` for control concepts and setpoint behavior.
- :doc:`../developer/developer_main` for contributor and API-oriented material.
- :doc:`../support/support` for support and issue-reporting guidance.

For project context and standards, see the `NWN website`_ and `ESDL`_.

.. _NWN website: https://www.nwn.nu/
.. _ESDL: https://www.esdl.nl/
