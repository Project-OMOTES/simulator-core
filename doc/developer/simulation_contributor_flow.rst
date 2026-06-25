Simulation Contributor Flow
===========================

Purpose
-------

This guide helps contributors trace and extend the simulation orchestration path from the
application entrypoint to solver execution.

Use this page when you need to change orchestration behavior, add integration points, or decide
which tests should fail or pass after a change. Use API pages for full class and method details.

Relevant Modules and Files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``src/omotes_simulator_core/infrastructure/app.py``
     - Entrypoint
     - Builds ``SimulationConfiguration``, loads ESDL input, and calls
       ``SimulationManager.execute``.
   * - ``src/omotes_simulator_core/infrastructure/simulation_manager.py``
     - Orchestrator
     - Maps ESDL to ``HeatNetwork`` and ``NetworkController``, runs ``NetworkSimulation``, and
       returns gathered output.
   * - ``src/omotes_simulator_core/simulation/networksimulation.py``
     - Time-step runner
     - Owns the outer simulation loop, controller update order, convergence retries, and
       progress callback cadence.
   * - ``src/omotes_simulator_core/entities/heat_network.py``
     - Runtime network wrapper
     - Applies controller setpoints to assets, calls ``Solver.solve``, and stores/gathers output.
   * - ``src/omotes_simulator_core/solver/solver.py``
     - Nonlinear solve loop
     - Builds matrix equations from network assets/nodes and iterates until convergence or
       iteration limit.
   * - ``src/omotes_simulator_core/solver/network/network.py``
     - Solver graph model
     - Holds solver-side assets/nodes consumed by ``Solver``.
   * - ``src/omotes_simulator_core/entities/network_controller.py``
     - Concrete controller
     - Produces per-asset setpoint dictionaries consumed by ``HeatNetwork.run_time_step``.
   * - ``src/omotes_simulator_core/entities/network_controller_abstract.py``
     - Control abstraction
     - Defines the minimal ``update_setpoints`` contract used by the simulation loop.
   * - ``unit_test/infrastructure/test_simulationmanager.py``
     - High-level unit check
     - Verifies manager execution returns output and triggers progress callback.
   * - ``unit_test/simulation/test_networksimulation.py``
     - Loop-level unit checks
     - Verifies run-path behavior and output collection for one timestep.
   * - ``unit_test/integration/test_communication_controller_network.py``
     - Integration coupling check
     - Verifies controller ``update_network_state`` propagates network asset state to controller
       objects.
   * - ``unit_test/solver/network/test_network.py``
     - Solver-network unit checks
     - Validates network graph behavior used by the solver layer.

Execution or Extension Flow
---------------------------

1. ``app.run`` creates ``SimulationConfiguration``, loads an ESDL file, and constructs
   ``SimulationManager``.
2. ``SimulationManager.execute`` maps ESDL into two runtime objects:

   - ``HeatNetwork`` via ``EsdlEnergySystemMapper(...).to_entity``.
   - ``NetworkController`` via ``EsdlControllerMapper().to_entity(...)``.

3. ``SimulationManager`` creates ``NetworkSimulation(network, controller)`` and calls
   ``run(config, progress_callback)``.
4. ``NetworkSimulation.run`` executes per timestep:

   - ``controller.update_network_state(heat_network=network)``
   - ``controller.update_setpoints(time)``
   - ``network.run_time_step(...)`` in a convergence retry loop (up to 20 iterations)
   - ``network.post_process_assets()`` and ``network.store_output()``
   - progress callback dispatch at configured intervals

5. ``HeatNetwork.run_time_step`` applies setpoints to matching assets and calls
   ``self.solver.solve()``.
6. ``Solver.solve`` resets state, assembles equations from solver assets/nodes, solves the matrix,
   writes results back to assets/nodes, and stops on convergence or iteration limit.
7. ``SimulationManager.execute`` returns ``NetworkSimulation.gather_output()``, which delegates to
   ``HeatNetwork.gather_output()``.

Implementation Notes
--------------------

- Keep orchestration order in ``NetworkSimulation.run`` intact unless intentionally changing
  control semantics. In particular, state synchronization and setpoint calculation happen before
  each solver call.
- Put physical/network equation behavior in solver and asset layers, not in
  ``SimulationManager``. The manager should stay focused on wiring and lifecycle.
- ``NetworkControllerAbstract`` currently standardizes ``update_setpoints`` only. If you add new
  controller capabilities used by orchestration code, update the abstraction and all concrete
  implementations together.
- ``HeatNetwork`` is the boundary between controller output and solver execution. Prefer extending
  setpoint schema handling there rather than leaking controller-specific logic into solver classes.
- ``NetworkSimulation`` has two convergence loops: an outer timestep loop and an inner retry loop
  that reruns ``run_time_step`` until ``HeatNetwork.check_convergence`` or retry limit.

Testing and Validation
----------------------

Use a layered test strategy:

- Orchestration wiring and callback behavior:
  ``unit_test/infrastructure/test_simulationmanager.py``.
- Timestep loop behavior and output collection:
  ``unit_test/simulation/test_networksimulation.py``.
- Controller/network state coupling:
  ``unit_test/integration/test_communication_controller_network.py``.
- Solver graph and asset/network mechanics:
  ``unit_test/solver/network/test_network.py`` and
  ``unit_test/solver/network/assets/`` tests.

For documentation changes, run from repository root:

.. code-block:: bat

   doc\make.bat html

Common Pitfalls
---------------

- Adding orchestration logic to ``SimulationManager`` that belongs in ``NetworkSimulation``.
- Changing controller setpoint schema without updating ``HeatNetwork.run_time_step`` handling.
- Treating generated API pages under ``doc/developer/api/`` as editable source.
- Validating only solver unit tests after orchestration edits; orchestration and integration tests
  should also be exercised.

Related Documentation
---------------------

- Developer landing page: :doc:`developer_main`
- Navigation guide: :doc:`developer_navigation`
- Architecture-oriented reference index: :doc:`../reference/architecture_reference`
- API references for orchestration modules:

  - :doc:`api/omotes_simulator_core.infrastructure.app`
  - :doc:`api/omotes_simulator_core.infrastructure.simulation_manager`
  - :doc:`api/omotes_simulator_core.simulation.networksimulation`
  - :doc:`api/omotes_simulator_core.entities.heat_network`
  - :doc:`api/omotes_simulator_core.entities.network_controller`
  - :doc:`api/omotes_simulator_core.solver.solver`
