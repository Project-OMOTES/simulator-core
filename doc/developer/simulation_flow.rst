Simulation flow
===============

Purpose
-------

This guide traces a simulation run from the application entrypoint to the solver and back
to the output table. Use it when you need to know where a step happens, in which order calls
are made, or which entry level to use for a test or debugging session.

It is written for contributors. For what the simulator computes, see the Intro, Network,
Solver, and Control sections. For package boundaries and the two-layer asset model, see
:doc:`architecture`. For class-level signatures, use :doc:`api/omotes_simulator_core`.

Relevant modules and files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 38 22 40

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``src/omotes_simulator_core/infrastructure/app.py``
     - Entrypoint
     - ``run(file_path)`` builds a ``SimulationConfiguration``, loads the ESDL file with
       ``pyesdl_from_file`` into an ``EsdlObject``, and calls
       ``SimulationManager.execute(progressLogger)``.
   * - ``src/omotes_simulator_core/infrastructure/simulation_manager.py``
     - Orchestrator
     - Creates ``HeatNetwork`` and ``NetworkController`` from the ESDL object, runs
       ``NetworkSimulation``, and returns ``gather_output()``. Logs and re-raises any
       exception from the run.
   * - ``src/omotes_simulator_core/entities/simulation_configuration.py``
     - Configuration dataclass
     - Holds ``simulation_id``, ``name``, ``timestep``, ``start``, and ``stop``.
       Passed from the entrypoint through to ``NetworkSimulation``.
   * - ``src/omotes_simulator_core/simulation/networksimulation.py``
     - Time-step loop
     - Owns the time loop, the controller call order, the convergence retry loop (at most
       20 passes per timestep), and the progress callback interval.
   * - ``src/omotes_simulator_core/entities/heat_network.py``
     - Runtime network wrapper
     - Holds entity assets, junctions, the solver ``Network``, and the ``Solver``. Applies
       setpoints, solves, checks convergence, post-processes, and stores output.
   * - ``src/omotes_simulator_core/entities/assets/asset_abstract.py``
     - Entity-layer base class
     - Declares the abstract ``set_setpoints``, ``write_to_output``, and ``postprocess``
       methods and implements ``write_standard_output`` and ``get_timeseries``.
   * - ``src/omotes_simulator_core/solver/network/network.py``
     - Solver graph model
     - Holds solver assets and nodes. Assets are added by ``EsdlEnergySystemMapper`` via
       ``add_existing_asset`` and connected via ``connect_assets``.
   * - ``src/omotes_simulator_core/solver/solver.py``
     - Nonlinear solve loop
     - Collects ``get_equations()`` from all solver assets and nodes, solves the matrix,
       and repeats until ``Matrix.is_converged()`` or the iteration limit of 100.
   * - ``src/omotes_simulator_core/entities/network_controller_abstract.py``
     - Control abstraction
     - Declares one abstract method, ``update_setpoints(time)``.
   * - ``src/omotes_simulator_core/entities/network_controller.py``
     - Concrete controller
     - Implements ``update_setpoints`` and ``update_network_state``. Holds one
       ``ControllerNetwork`` per hydraulically separated sub-network.
   * - ``src/omotes_simulator_core/adapter/transforms/mappers.py``
     - ESDL-to-entity mapper
     - ``EsdlEnergySystemMapper.to_entity(network)`` creates the entity assets, registers
       their solver assets in ``network``, connects them, and returns
       ``(list[AssetAbstract], list[Junction])``.
   * - ``src/omotes_simulator_core/adapter/transforms/controller_mapper.py``
     - ESDL-to-controller mapper
     - ``EsdlControllerMapper.to_entity(esdl, timestep)`` creates the asset controllers and
       the ``NetworkController``.
   * - ``src/omotes_simulator_core/adapter/transforms/esdl_asset_mapper.py``
     - Asset dispatch table
     - Maps ESDL asset types to mapper classes via ``conversion_dict_mappers``.
   * - ``unit_test/infrastructure/test_simulationmanager.py``
     - Orchestration test
     - Runs ``SimulationManager.execute`` on ``testdata/test1.esdl`` and checks the shape of
       the result table.
   * - ``unit_test/simulation/test_networksimulation.py``
     - Time-loop test
     - Checks construction with mocks and runs ``NetworkSimulation.run`` on
       ``testdata/test1.esdl``.
   * - ``unit_test/integration/test_heat_physics.py``
     - End-to-end integration test
     - Runs a full simulation through ``SimulationManager`` and asserts physical results
       such as heat power and primary inlet temperature.

Execution or extension flow
---------------------------

High-level run
~~~~~~~~~~~~~~

1. **Entrypoint.** ``app.run()`` creates a ``SimulationConfiguration``, loads the ESDL
   file into an ``EsdlObject``, and calls ``SimulationManager.execute(callback)``.

2. **Build.** ``SimulationManager.execute`` creates two runtime objects:

   - ``HeatNetwork(EsdlEnergySystemMapper(esdl).to_entity)``. ``HeatNetwork`` creates an
     empty solver ``Network`` and passes it to ``to_entity``. For each enabled ESDL asset
     the mapper creates an entity asset through ``EsdlAssetMapper.to_entity`` and calls
     ``network.add_existing_asset(entity.solver_asset)``. Disabled assets are skipped with
     a warning. The mapper then connects the solver assets and wraps the created solver
     nodes in ``Junction`` objects. ``HeatNetwork`` finally creates the ``Solver``.
   - ``EsdlControllerMapper().to_entity(esdl, timestep=config.timestep)``, which returns a
     ``NetworkController``.

3. **Time loop.** ``NetworkSimulation(network, controller).run(config, callback)``
   computes the number of timesteps from ``start``, ``stop``, and ``timestep``. For each
   timestep it:

   a. Sets ``time`` to ``start`` plus the elapsed seconds, with the UTC timezone.

   b. Calls ``controller.update_network_state(heat_network)``. The controller reads
      ``get_state()`` from producer, consumer, and storage entity assets and passes it to
      their asset controllers.

   c. Calls ``controller.update_setpoints(time)``, which returns ``controller_input``: a
      dictionary from asset ID to a dictionary of ``PROPERTY_*`` setpoints.

   d. Calls ``network.network.reset_prev_solution()`` to clear the previous solver
      solution.

   e. Runs up to 20 passes of ``network.run_time_step(time, timestep, controller_input)``
      followed by ``network.check_convergence()``. ``run_time_step`` calls
      ``set_time_step``, ``set_time``, and ``set_setpoints`` only on assets whose ID is a
      key in ``controller_input``, then calls ``Solver.solve()``. ``check_convergence``
      returns ``False`` as soon as one asset's ``is_converged()`` is ``False``.

   f. Calls ``network.post_process_assets()``, which calls ``postprocess()`` on every
      asset, then ``network.store_output()``, which calls ``write_standard_output()`` and
      then ``write_to_output()`` on every asset.

   g. Calls the progress callback every ``progress_interval`` timesteps, which limits the
      number of progress messages to about ``MAX_NUMBER_MESSAGES`` (15).

4. **Solve.** ``Solver.solve()`` resets the matrix solution and the previous solution of
   every solver asset and node, then repeats: collect equations from all assets and nodes,
   solve the matrix, and write the results back to assets and nodes. It stops when the
   matrix has converged or after more than 100 iterations, in which case it logs a
   warning.

5. **Output.** ``SimulationManager`` calls ``worker.gather_output()``, which concatenates
   ``get_timeseries()`` of every asset into a single ``pandas.DataFrame``.

Lower-level entry points
~~~~~~~~~~~~~~~~~~~~~~~~

Tests and debugging sessions often skip part of the stack:

- **Network level.** Build ``HeatNetwork(EsdlEnergySystemMapper(esdl).to_entity)``, write
  a ``controller_input`` dictionary by hand, and call ``run_time_step`` directly. This skips
  the controller. ``unit_test/integration/test_ates_network.py`` uses this pattern.
- **Solver level.** Create a solver ``Network()``, add solver assets with
  ``add_existing_asset``, connect them with ``connect_assets``, set boundary values on the
  solver assets, and call ``Solver(network).solve()``. This skips entities, ESDL, and
  control. ``unit_test/integration/test_zero_flow_physics.py`` and
  ``unit_test/integration/test_heat_transfer_asset.py`` use this pattern.

Implementation notes
--------------------

- ``NetworkSimulation`` is typed against ``NetworkController`` and calls
  ``update_network_state``, which is not part of ``NetworkControllerAbstract``.
- ``NetworkSimulation`` does not raise when the 20 retry passes end without convergence; it
  logs the number of passes at debug level and continues. ``Solver.solve`` also only logs a
  warning when it reaches its iteration limit.
- Setpoints are computed once per timestep, before the retry loop. Retry passes only
  re-run ``set_setpoints`` and the solve with the same ``controller_input``; assets can use
  the previous pass's solver results inside ``set_setpoints`` and ``is_converged``.
- ``postprocess`` runs before ``store_output``, so output written in ``write_to_output``
  reflects state after post-processing.
- The ESDL is read only in the build phase. Nothing in the time loop accesses ESDL objects.

Testing and validation
----------------------

Choose the test level that matches the part of the flow you changed:

- ``unit_test/infrastructure/test_simulationmanager.py`` covers the build and the full run
  through ``SimulationManager``.
- ``unit_test/simulation/test_networksimulation.py`` covers ``NetworkSimulation``
  construction (with ``Mock`` objects) and a real run on ``testdata/test1.esdl``.
- ``unit_test/integration/test_communication_controller_network.py`` wraps assets and
  asset controllers in ``Mock(wraps=...)`` and checks that ``update_network_state`` calls
  ``set_state`` on every producer, consumer, and storage controller.
- ``unit_test/integration/test_heat_physics.py`` and
  ``unit_test/integration/test_pressure_physics.py`` check physical results of full runs.
- The network-level and solver-level tests listed under `Lower-level entry points`_ check
  behavior without the controller or without entities.

Run the full suite with ``ci/linux/test_unit.sh`` or ``ci\win32\test_unit.cmd``. To run a
single file, see :doc:`testing_strategy`; targeted runs need ``--no-cov`` because of the
coverage threshold in ``pyproject.toml``.

Common pitfalls
---------------

- **Missing controller entry.** ``run_time_step`` only updates assets whose ID is in
  ``controller_input``. An asset without a controller keeps its previous setpoints without
  any warning.
- **Unregistered ESDL type.** An ESDL asset type missing from ``conversion_dict_mappers``
  raises ``NotImplementedError`` in ``EsdlAssetMapper.to_entity`` during the build phase.
- **State that accumulates across retry passes.** ``set_setpoints`` and ``Solver.solve`` can
  run up to 20 times per timestep. Update time-integrated state, such as a storage fill
  level, in ``postprocess`` and not in ``set_setpoints``.
- **New controller state.** Asset controllers only receive what
  ``NetworkController.update_network_state`` passes from ``AssetAbstract.get_state()``. To
  give a controller more state, extend both ``get_state`` on the entity asset and
  ``update_network_state``.
- **Two iteration loops.** The retry loop in ``NetworkSimulation.run`` (at most 20 passes)
  couples setpoint handling and physics; the loop in ``Solver.solve`` (at most 100
  iterations) solves the nonlinear equations. Neither raises an error when its limit is
  reached.

Related documentation
---------------------

- :doc:`../intro/intro_main` — what the simulator does.
- :doc:`architecture` — package boundaries and the two-layer asset model.
- :doc:`../solver/solver_main` — solver behavior and equation assembly.
- :doc:`../network/network_main` — network representation.
- :doc:`../controller/controller` — control behavior and setpoint logic.
- :doc:`developer_guides` — how-to guides for extending the simulator.
- :doc:`testing_strategy` — test layout and commands.
- :doc:`api/omotes_simulator_core` — generated class and module reference.
