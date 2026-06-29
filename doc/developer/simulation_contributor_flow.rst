Simulation Contributor Flow
===========================

Purpose
-------

This guide explains how the OMOTES.SIMULATOR_CORE package is organized, how simulation
executes end-to-end, and where to make changes safely.

Read this page first before modifying any part of the package. It maps the six top-level
packages to their responsibilities, traces the execution path from the application
entrypoint through to the nonlinear solver, and identifies the abstractions that separate
each layer.

This page is for contributors and new developers. For conceptual system-level explanations
consult the Intro, Solver, Network, and Control sections. For class-level detail use the
:doc:`api/omotes_simulator_core` root index.

Relevant Modules and Files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 38 22 40

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``src/omotes_simulator_core/infrastructure/app.py``
     - Entrypoint
     - Builds ``SimulationConfiguration``, loads the ESDL file, and calls
       ``SimulationManager.execute``. The ``run()`` function here is the single
       entry point when the package is invoked from the command line.
   * - ``src/omotes_simulator_core/infrastructure/simulation_manager.py``
     - Orchestrator
     - Creates ``HeatNetwork`` and ``NetworkController`` from the ESDL object, then
       creates ``NetworkSimulation`` and calls ``run``. Owns the error boundary for
       a full simulation run.
   * - ``src/omotes_simulator_core/entities/simulation_configuration.py``
     - Configuration dataclass
     - Holds ``simulation_id``, ``name``, ``timestep``, ``start``, and ``stop``.
       Passed from the entrypoint through to ``NetworkSimulation``.
   * - ``src/omotes_simulator_core/simulation/networksimulation.py``
     - Time-step loop
     - Owns the outer time loop, controller update sequencing, the convergence retry
       loop (up to 20 iterations per timestep), and the progress callback cadence.
   * - ``src/omotes_simulator_core/entities/heat_network.py``
     - Runtime network wrapper
     - Holds the asset list and solver. Applies controller setpoints to assets per
       timestep, calls ``Solver.solve``, checks convergence, post-processes assets,
       and accumulates output.
   * - ``src/omotes_simulator_core/entities/assets/asset_abstract.py``
     - Entity-layer base class
     - Abstract base for all thermo-hydraulic asset entities. Defines
       ``set_setpoints``, ``write_to_output``, and output collection.
   * - ``src/omotes_simulator_core/solver/network/network.py``
     - Solver graph model
     - Holds the dictionary of solver-layer assets and nodes consumed by ``Solver``.
       Assets are added by the mapper, not by ``HeatNetwork`` directly.
   * - ``src/omotes_simulator_core/solver/solver.py``
     - Nonlinear solve loop
     - Builds the global matrix from each asset's ``get_equations()`` return value
       and iterates (up to 100 inner iterations) until convergence.
   * - ``src/omotes_simulator_core/entities/network_controller_abstract.py``
     - Control abstraction
     - Defines the minimal contract used by ``NetworkSimulation``: one abstract
       method, ``update_setpoints(time)``.
   * - ``src/omotes_simulator_core/entities/network_controller.py``
     - Concrete controller
     - Implements ``NetworkControllerAbstract``. Owns a list of ``ControllerNetwork``
       objects (one per hydraulically isolated sub-network) and orchestrates
       per-asset setpoint dispatch across those networks.
   * - ``src/omotes_simulator_core/adapter/transforms/mappers.py``
     - ESDL-to-entity mapper
     - ``EsdlEnergySystemMapper.to_entity`` converts an ``EsdlObject`` into the
       ``(list[AssetAbstract], list[Junction])`` tuple consumed by ``HeatNetwork``.
   * - ``src/omotes_simulator_core/adapter/transforms/controller_mapper.py``
     - ESDL-to-controller mapper
     - ``EsdlControllerMapper.to_entity`` converts an ``EsdlObject`` into a
       ``NetworkController`` containing the correct ``ControllerNetwork`` objects.
   * - ``src/omotes_simulator_core/adapter/transforms/esdl_asset_mapper.py``
     - Asset dispatch table
     - Maps ESDL asset types to per-asset mapper classes via ``conversion_dict_mappers``.
   * - ``unit_test/infrastructure/test_simulationmanager.py``
     - Orchestration unit tests
     - Verifies ``SimulationManager.execute`` returns output and triggers the progress
       callback correctly.
   * - ``unit_test/simulation/test_networksimulation.py``
     - Loop-level unit tests
     - Verifies the time-step loop, controller update order, and output collection.
   * - ``unit_test/integration/test_heat_physics.py``
     - End-to-end integration test
     - Runs a full simulation against ``testdata/test1.esdl`` and asserts physical
       output values. The primary integration test for physics correctness.

Package Layout
--------------

The source tree under ``src/omotes_simulator_core/`` contains six top-level packages:

``infrastructure/``
    Application entrypoint (``app.py``) and ``SimulationManager``. This is the boundary
    between the outside world and the simulation internals. It is also the right place to
    add top-level error handling or result post-processing.

``adapter/``
    Everything related to reading and transforming ESDL input. Contains three sub-packages:

    - ``transforms/`` — mapper classes that convert ESDL objects into internal entities and
      controller objects. ``esdl_asset_mapper.py`` holds the dispatch table; each asset type
      has a dedicated mapper in ``esdl_asset_mappers/``; each controller type has a dedicated
      mapper in ``controller_mappers/``.
    - ``utility/`` — graph utilities used by the ESDL-to-graph conversion step.
    - ``presentation/`` — output presentation layer (currently minimal).

``entities/``
    The runtime object model. Contains:

    - ``assets/`` — entity-layer asset classes (one per physics asset type), the abstract
      base ``AssetAbstract``, and the ``controller/`` sub-package containing per-asset
      controller classes.
    - ``heat_network.py`` — the runtime container that holds all assets and the solver.
    - ``network_controller.py`` and ``network_controller_abstract.py`` — the controller
      and its minimal abstract contract.
    - ``esdl_object.py``, ``simulation_configuration.py``, ``utility/`` — supporting types.

``simulation/``
    The time-step orchestration loop (``networksimulation.py``) and the abstract mapper
    base class (``mappers/mappers.py``).

``solver/``
    The nonlinear physics solver. Contains:

    - ``solver.py`` — the solver entry point: assembles the equation matrix and iterates.
    - ``network/`` — the solver-side graph model (``Network``) and solver-layer asset
      classes under ``network/assets/``.
    - ``matrix/`` — the ``Matrix`` class, ``EquationObject``, and index helpers used to
      assemble and solve the linear system at each iteration.

``entities/assets/controller/``
    Per-asset controller classes (``ControllerProducer``, ``ControllerConsumer``,
    ``ControllerAtesStorage``, ``ControllerIdealHeatStorage``, ``ControllerHeatTransferAsset``)
    and the ``ControllerNetwork`` class that groups hydraulically connected assets.

Execution Flow
--------------

The following numbered steps trace a full simulation run from entrypoint to output:

1. **Entrypoint** — ``app.run()`` creates a ``SimulationConfiguration`` dataclass (timestep,
   start datetime, stop datetime), loads the ESDL file into an ``EsdlObject``, and calls
   ``SimulationManager.execute(progress_callback)``.

2. **ESDL parsing** — ``SimulationManager.execute`` creates two runtime objects from the
   ESDL input in parallel:

   - ``HeatNetwork(EsdlEnergySystemMapper(esdl).to_entity)`` — the mapper callable is passed
     as a factory argument. ``to_entity`` returns ``(list[AssetAbstract], list[Junction])``;
     each asset constructor also creates and registers the corresponding solver-layer asset
     inside the ``Network`` graph object.
   - ``EsdlControllerMapper().to_entity(esdl, timestep=config.timestep)`` — returns a
     ``NetworkController`` containing one ``ControllerNetwork`` per hydraulically isolated
     sub-network.

3. **Simulation loop** — ``SimulationManager`` creates ``NetworkSimulation(network, controller)``
   and calls ``worker.run(config, progress_callback)``. Inside ``run``:

   a. The loop iterates over each timestep from ``config.start`` to ``config.stop`` in
      steps of ``config.timestep`` seconds.

   b. Per timestep:

      - ``controller.update_network_state(heat_network)`` — reads current asset state
        (temperatures, flows) from each entity-layer asset and updates the corresponding
        per-asset controller objects.
      - ``controller.update_setpoints(time)`` — calculates and returns
        ``controller_input``: a ``dict[asset_id, dict[property, value]]`` containing the
        heat demand, supply temperature, return temperature, and pressure setpoints for
        every asset.
      - A convergence retry loop (up to 20 iterations) runs
        ``network.run_time_step(time, timestep, controller_input)`` followed by
        ``network.check_convergence()``.

   c. ``network.run_time_step`` applies the setpoints dict to each asset via
      ``asset.set_setpoints(...)`` and calls ``solver.solve()``.

   d. ``solver.solve()`` calls ``asset.get_equations()`` on every solver-layer asset and
      node in the ``Network`` graph, assembles the global matrix, and runs the linear
      solver. The outer iteration loop in ``Solver.solve()`` repeats up to 100 times.

   e. After convergence (or iteration limit), ``network.post_process_assets()`` and
      ``network.store_output()`` are called.

4. **Output collection** — after the time loop, ``worker.gather_output()`` calls
   ``network.gather_output()``, which collects each asset's output list into a single
   ``pandas.DataFrame`` returned to the caller.

Two-Layer Asset Model
---------------------

Every thermo-hydraulic asset is represented by two classes at different abstraction levels:

**Entity layer** (``entities/assets/``)
    Python classes such as ``ProductionCluster``, ``DemandCluster``, ``Pipe``, ``HeatPump``.
    These hold per-timestep state, apply controller setpoints, collect output, and expose
    ``get_state()`` for the controller. All inherit from ``AssetAbstract``.

**Solver layer** (``solver/network/assets/``)
    Low-level classes such as ``HeatBoundary``, ``SolverPipe``, ``HeatTransferAsset``.
    These implement ``get_equations()`` and supply ``EquationObject`` instances to the
    global matrix. They know about mass flow, pressure drop, and energy balance as
    algebraic constraints — not about time series or ESDL properties.

Each entity-layer asset creates its corresponding solver-layer asset in its constructor and
registers it with the ``Network`` graph. The entity layer accesses solver results through
``self.solver_asset`` after each ``Solver.solve()`` call.

Control Architecture
--------------------

The control layer sits between ``NetworkSimulation`` and ``HeatNetwork``:

- ``NetworkControllerAbstract`` defines the contract: one abstract method,
  ``update_setpoints(time: datetime) -> dict``.
- ``NetworkController`` is the concrete implementation. It holds a list of
  ``ControllerNetwork`` objects — one per hydraulically isolated sub-network. Each
  ``ControllerNetwork`` holds per-asset controller objects
  (``ControllerProducer``, ``ControllerConsumer``, ``ControllerAtesStorage``, etc.)
  that own demand profiles and storage state.
- ``NetworkSimulation`` only calls ``update_network_state`` and ``update_setpoints`` on the
  abstract interface; it does not know about individual asset controllers.

Testing and Validation
----------------------

The most relevant tests for this execution flow are:

- ``unit_test/infrastructure/test_simulationmanager.py`` — verifies the orchestration path:
  checks that ``execute`` returns a non-empty ``DataFrame`` and that the progress callback
  is invoked.
- ``unit_test/simulation/test_networksimulation.py`` — verifies the time-step loop in
  isolation using mocked ``HeatNetwork`` and ``NetworkController`` objects.
- ``unit_test/integration/test_heat_physics.py`` — runs a full simulation against a real
  ESDL file and asserts physical output values. Use this as the reference integration test.
- ``unit_test/integration/test_communication_controller_network.py`` — verifies that
  ``update_network_state`` correctly propagates entity-layer asset state to per-asset
  controller objects.

Run the test suite from the repository root::

    PYTHONPATH='$PYTHONPATH:src/' pytest -p no:faulthandler --junit-xml=test-results.xml unit_test/

Common Pitfalls
---------------

- **Editing the wrong layer**: solver-layer asset classes (``solver/network/assets/``) must
  not import from ``entities/``. Dependency runs upward only: entity layer depends on solver
  layer, never the reverse.
- **Bypassing the mapper registry**: new asset types that are not registered in
  ``esdl_asset_mapper.py``'s ``conversion_dict_mappers`` will silently produce no asset
  in the network. Always register and always add a unit test for the mapper.
- **Skipping ``update_network_state``**: the controller's per-asset controller objects do
  not read from the solver directly. They rely on ``update_network_state`` being called
  before ``update_setpoints`` each timestep. If you add state that the controller needs,
  expose it via ``AssetAbstract.get_state()`` and read it in ``NetworkController.update_network_state``.
- **Convergence retry confusion**: ``network.run_time_step`` is called inside a retry loop
  of up to 20 iterations. Asset state that accumulates side effects across calls within a
  single timestep will produce incorrect results. Use ``store_output`` for committed output
  and ``post_process_assets`` for end-of-timestep finalization only.
- **Confusing the two solver iteration loops**: there is an outer iteration loop in
  ``NetworkSimulation.run`` (convergence retries, max 20) and an inner loop inside
  ``Solver.solve`` (matrix iterations, max 100). They serve different purposes: the outer
  loop handles controller-physics coupling; the inner loop handles the nonlinear equation
  solve.

Related Documentation
---------------------

- Conceptual overview of the system: :doc:`../intro/intro_main`
- Solver behavior and equation assembly: :doc:`../solver/solver_main`
- Network representation: :doc:`../network/network_main`
- Control behavior and setpoint logic: :doc:`../controller/controller`
- Adding a new asset: :doc:`add_new_asset`
- Extending control behavior: :doc:`control_extension`
- Test layout and running tests: :doc:`testing`
- Full class and module reference: :doc:`api/omotes_simulator_core`
