Introduction
============

OMOTES.SIMULATOR_CORE is a Python package for thermo-hydraulic simulation of district heating systems.
It combines network topology, asset behavior, and controller setpoints to compute mass flow rate,
pressure, and thermal state over time.

This Intro section provides package-level orientation before moving into the domain sections.
Use it to understand what the package does, who it is for, and what inputs and outputs define a
simulation run.

**Contents**

.. toctree::
	:maxdepth: 1

	package_scope
	audience_and_use_cases
	simulation_input_and_output

Section map
-----------

- For solver architecture and numerical flow, see :doc:`../solver/solver_main`.
- For network concepts and topology behavior, see :doc:`../network/network_main`.
- For physical relations and asset equations, see :doc:`../physics/physics_main`.
- For controller behavior and setpoint logic, see :doc:`../controller/controller`.
- For contributor and API guidance, see :doc:`../developer/developer_main`.
- For issue reporting and collaboration support, see :doc:`../support/support`.

External context
----------------

For project context and standards, see the `NWN website`_ and `ESDL`_.

.. _NWN website: https://www.nwn.nu/
.. _ESDL: https://www.esdl.nl/
