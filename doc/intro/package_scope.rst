Package scope
=============

OMOTES.SIMULATOR_CORE provides the simulation engine used to evaluate district-heating behavior over
time. It focuses on thermo-hydraulic state evolution in a network of connected assets.

What is in scope
----------------

- Time-stepped simulation of hydraulic and thermal behavior
- Integration of network topology, asset physics, and controller setpoints
- Execution on ESDL-based model definitions

What is out of scope
--------------------

- Interactive visualization dashboards and scenario authoring tools
- Site-specific deployment and operational orchestration
- Generic data platform concerns not required for simulation execution

Package boundaries
------------------

At a high level, simulation behavior is produced by collaboration between:

- Solver: assembles and solves the network equation system
- Network representation: maintains connected nodes and assets
- Physics models: define asset-specific constitutive behavior
- Controller: computes per-step setpoints and dispatch decisions
