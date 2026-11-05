Developer documentation
=======================

This section contains contributor-facing guides for OMOTES.SIMULATOR_CORE. Use it when you
need implementation-oriented guidance: where code lives in ``src/omotes_simulator_core``,
how a simulation run flows from ``app.py`` to the ``Solver``, how to extend assets, control,
or output, and how to test and document your changes.

For system-level behavior and governing relations, consult the Intro, Solver, Network,
Physics, and Control sections instead. For exhaustive class and module lookup, use the
generated API root index listed last in the toctree below.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   developer_navigation
   architecture
   network_reference
   controller_reference
   solver_reference
   asset_reference
   simulation_flow
   testing_strategy
   developer_guides
   documentation_with_ai_agents
   api/omotes_simulator_core


Start here
----------

New contributors can follow this reading order:

1. :doc:`developer_navigation` — map of the packages under ``src/omotes_simulator_core``
   and ``unit_test``, and a task-to-file routing table.
2. :doc:`architecture` — the layering between ``infrastructure``, ``adapter``,
   ``entities``, ``simulation``, and ``solver``, the two-layer asset model, and the
   control hierarchy.
3. :doc:`simulation_flow` — the per-timestep call sequence through ``SimulationManager``,
   ``NetworkSimulation``, ``HeatNetwork``, and ``Solver``, plus the lower-level manual
   path used by solver integration tests.
4. The curated reference pages — responsibilities, interfaces and implementation notes
   per subsystem, each with links to the class-level reference pages:

   - :doc:`network_reference` — ``HeatNetwork``, the solver ``Network`` and node
     construction from ESDL.
   - :doc:`controller_reference` — ``NetworkController``, sub-networks and per-asset
     controllers.
   - :doc:`solver_reference` — the ``Solver`` iteration loop, ``Matrix`` and solver asset
     base classes.
   - :doc:`asset_reference` — the ``AssetAbstract`` interface and entity-to-solver asset
     pairing.

5. :doc:`testing_strategy` — test layout, convenience scripts, and the three integration
   test patterns.
6. :doc:`developer_guides` — step-by-step guides for adding assets, extending control,
   and adding output columns.

Use :doc:`documentation_with_ai_agents` when you add or update pages under ``doc/``.
Use :doc:`api/omotes_simulator_core` only once you know which class or module you need.

