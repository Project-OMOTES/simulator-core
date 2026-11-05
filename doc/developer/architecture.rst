Package architecture
====================

Purpose
-------

This page gives contributors an overview of how OMOTES.SIMULATOR_CORE is layered: which
package owns which responsibility, which way dependencies point, how an asset is split over
an entity class and a solver class, and how the control hierarchy is organized. Read it
before moving code between packages or adding a new kind of component.

For a file-by-file map, see :doc:`developer_navigation`. For the per-timestep call order,
see :doc:`simulation_flow`. For step-by-step extension work, see :doc:`developer_guides`.

Relevant modules and files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``src/omotes_simulator_core/infrastructure/``
     - Outer boundary
     - ``app.py`` and ``SimulationManager`` connect a loaded ``EsdlObject`` and a
       ``SimulationConfiguration`` to the simulation; ``SimulationManager.execute`` logs and
       re-raises any error from a run.
   * - ``src/omotes_simulator_core/adapter/``
     - ESDL translation
     - ``transforms/`` holds all ESDL-to-entity and ESDL-to-controller mappers;
       ``utility/graph.py`` holds the graph used for sub-network detection.
   * - ``src/omotes_simulator_core/entities/``
     - Runtime object model
     - Entity assets, asset controllers, ``HeatNetwork``, ``NetworkController``, and the
       ESDL wrappers ``EsdlObject`` and ``EsdlAssetObject``.
   * - ``src/omotes_simulator_core/simulation/``
     - Time loop
     - ``NetworkSimulation`` and the ``EsdlMapperAbstract`` base class.
   * - ``src/omotes_simulator_core/solver/``
     - Physics solve
     - ``Solver``, the solver ``Network`` graph, solver assets, the ``Matrix``, and
       ``fluid_props``.

Execution or extension flow
---------------------------

A run has two phases that touch different packages.

1. **Build phase** (``SimulationManager.execute``). ``adapter`` reads the ``EsdlObject``
   and produces runtime objects in ``entities`` and ``solver``:

   - ``EsdlEnergySystemMapper.to_entity`` is passed to ``HeatNetwork`` as a factory. For
     each enabled ESDL asset it calls ``EsdlAssetMapper.to_entity`` to create an entity
     asset, then calls ``Network.add_existing_asset`` with that asset's ``solver_asset``.
     Afterwards it connects the solver assets through ``Network.connect_assets``, which
     creates the solver ``Node`` objects wrapped by entity ``Junction`` objects.
   - ``EsdlControllerMapper.to_entity`` creates one asset controller per controllable ESDL
     asset, groups them into ``ControllerNetwork`` objects, and returns a
     ``NetworkController``.

2. **Run phase** (``NetworkSimulation.run``). No ESDL is touched. Each timestep the
   ``NetworkController`` reads entity state and returns setpoints, ``HeatNetwork`` applies
   them to entity assets, and ``Solver.solve`` solves the solver ``Network``.

When you add a component, decide first which phase it belongs to. ESDL parsing belongs in
the build phase and in ``adapter``; per-timestep behavior belongs in ``entities`` or
``solver``.

Implementation notes
--------------------

Dependency direction
~~~~~~~~~~~~~~~~~~~~

Imports point inward: ``infrastructure`` imports ``adapter``, ``entities``, and
``simulation``; ``adapter`` imports ``entities`` and ``solver``; ``entities`` imports
``solver``. The current code has these exceptions, which new code should not extend:

- ``entities/esdl_object.py`` and ``entities/assets/esdl_asset_object.py`` import
  ``OmotesAssetLabels`` and port helpers from ``adapter/transforms``.
- ``solver/network/assets/solver_pipe.py`` imports constants from
  ``entities/assets/asset_defaults.py``.

The ``esdl`` package is imported in ``adapter`` and in the ESDL wrappers
``entities/esdl_object.py``, ``entities/assets/esdl_asset_object.py``, and
``entities/utility/influxdb_reader.py``. Entity asset classes, controllers, ``HeatNetwork``,
and ``solver`` do not import ``esdl``; mappers pass them plain Python values.

Two-layer asset model
~~~~~~~~~~~~~~~~~~~~~

Every thermo-hydraulic asset is split over two classes:

**Entity layer** (``entities/assets/``)
    Classes such as ``ProductionCluster``, ``DemandCluster``, ``Pipe``, and ``HeatPump``,
    all derived from ``AssetAbstract``. They translate controller setpoints into solver
    settings in ``set_setpoints``, report state for the controller in ``get_state``, decide
    convergence in ``is_converged``, update internal state in ``postprocess``, and write
    output in ``write_to_output``.

**Solver layer** (``solver/network/assets/``)
    Classes such as ``HeatBoundary``, ``SolverPipe``, ``HeatTransferAsset``, and
    ``HeatBufferAsset``, derived from ``BaseAsset`` (which derives from ``BaseItem``). They
    return ``EquationObject`` instances from ``get_equations`` and store the latest solution
    in ``prev_sol``. They have no notion of ESDL, profiles, or output tables.

The entity class creates its solver asset in ``__init__`` and stores it as
``self.solver_asset``; the mapper registers it in ``Network``. After ``Solver.solve`` the
entity class reads results through ``self.solver_asset`` accessors such as
``get_mass_flow_rate``, ``get_temperature``, and ``get_pressure``.

Several entity classes can share one solver class. ``GasHeater``, ``ElecBoiler``, and
``AirToWaterHeatPump`` subclass ``ProductionCluster`` and reuse ``HeatBoundary``; only
setpoint handling and output differ.

Control hierarchy
~~~~~~~~~~~~~~~~~

- ``NetworkControllerAbstract`` declares one abstract method,
  ``update_setpoints(time) -> dict``.
- ``NetworkController`` implements it and also provides ``update_network_state``, which
  ``NetworkSimulation`` calls before ``update_setpoints``. ``NetworkSimulation`` is typed
  against ``NetworkController``, not against the abstract class.
- ``NetworkController`` holds a list of ``ControllerNetwork`` objects. Each represents a
  hydraulically connected sub-network bounded by heat pumps or heat exchangers, and holds
  lists of producer, consumer, storage, and primary/secondary heat transfer controllers.
- Asset controllers derive from ``AssetControllerAbstract`` and hold profiles, limits, and
  storage state. They do not compute setpoint dictionaries themselves;
  ``ControllerNetwork`` and ``NetworkController`` build the dictionaries from their
  ``get_heat_demand``, ``get_max_power``, and effective charge and discharge values.

The setpoint dictionary maps asset IDs to ``PROPERTY_*`` keys from ``asset_defaults.py``.
It is the only data passed from control to physics.

Testing and validation
----------------------

Layer boundaries are reflected in the test tree: ``unit_test/solver/`` tests solver assets
without entity classes, ``unit_test/entities/`` tests entity assets and controllers with the
solver patched, and ``unit_test/integration/`` combines layers. After moving code between
packages, run the full suite and the type checker (``ci/linux/typecheck.sh`` or
``ci\win32\typecheck.cmd``), which reports broken imports. See :doc:`testing_strategy`.

Common pitfalls
---------------

- Adding ``esdl`` imports to entity assets, controllers, or ``solver``: read ESDL values in
  a mapper and pass them to the constructor.
- Putting physics in ``set_setpoints``: equations belong in the solver asset's
  ``get_equations``; the entity class only sets solver attributes.
- Extending the ``NetworkControllerAbstract`` interface implicitly: a replacement for
  ``NetworkController`` must also provide ``update_network_state``.
- Adding orchestration to ``NetworkSimulation``: keep run setup in ``SimulationManager`` and
  keep ``NetworkSimulation`` limited to the time loop.

Related documentation
---------------------

- :doc:`developer_navigation` — file-level map of the repository.
- :doc:`network_reference`, :doc:`controller_reference`, :doc:`solver_reference` and
  :doc:`asset_reference` — responsibilities and interfaces per subsystem.
- :doc:`simulation_flow` — per-timestep execution flow.
- :doc:`developer_guides` — extension how-to guides.
- :doc:`testing_strategy` — test layout and commands.
- :doc:`../intro/intro_main` — what the simulator does.
- :doc:`../controller/controller` — conceptual description of control.
- :doc:`api/omotes_simulator_core` — generated class and module reference.
