Package Architecture
====================

Purpose
-------

This page provides a contributor-oriented overview of how the OMOTES.SIMULATOR_CORE package
is structured: what each top-level package is responsible for, how the two-layer asset model
works, and how the control layer fits in. Read this page before making structural changes to
the package.

For the detailed execution flow (which class calls which, in what order), see
:doc:`simulation_flow`. For adding assets or extending control, see :doc:`developer_guides`.

Package Layout
--------------

The source tree under ``src/omotes_simulator_core/`` contains six top-level packages:

``infrastructure/``
    Application entrypoint (``app.py``) and ``SimulationManager``. This is the boundary
    between the outside world and the simulation internals. It is the right place to add
    top-level error handling or result post-processing. Contributors should not add domain
    logic here.

``adapter/``
    Everything related to reading and transforming ESDL input. Contains three sub-packages:

    - ``transforms/`` — mapper classes that convert ESDL objects into internal entities and
      controller objects. ``esdl_asset_mapper.py`` holds the dispatch table; each asset type
      has a dedicated mapper in ``esdl_asset_mappers/``; each controller type has a dedicated
      mapper in ``controller_mappers/``.
    - ``utility/`` — graph utilities used by the ESDL-to-graph conversion step.
    - ``presentation/`` — output presentation layer.

``entities/``
    The runtime object model. Contains:

    - ``assets/`` — entity-layer asset classes (one per physics asset type), the abstract
      base ``AssetAbstract``, and the ``controller/`` sub-package with per-asset controller
      classes.
    - ``heat_network.py`` — the runtime container that holds all assets and the solver.
    - ``network_controller.py`` and ``network_controller_abstract.py`` — the network
      controller and its abstract contract.
    - ``esdl_object.py``, ``simulation_configuration.py``, ``utility/`` — supporting types.

``simulation/``
    The time-step orchestration loop (``networksimulation.py``) and the abstract mapper
    base class (``mappers/mappers.py``).

``solver/``
    The nonlinear physics solver. Contains:

    - ``solver.py`` — assembles the equation matrix and iterates.
    - ``network/`` — the solver-side graph model (``Network``) and solver-layer asset
      classes under ``network/assets/``.
    - ``matrix/`` — the ``Matrix`` class, ``EquationObject``, and index helpers used to
      assemble and solve the linear system at each iteration.

``entities/assets/controller/``
    Per-asset controller classes (``ControllerProducer``, ``ControllerConsumer``,
    ``ControllerAtesStorage``, ``ControllerIdealHeatStorage``, ``ControllerHeatTransferAsset``)
    and ``ControllerNetwork`` which groups hydraulically connected assets.

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
    global matrix. They represent mass flow, pressure drop, and energy balance as algebraic
    constraints — they do not know about time series or ESDL properties.

Each entity-layer asset creates its corresponding solver-layer asset in its constructor and
registers it with the ``Network`` graph object. The entity layer reads solver results through
``self.solver_asset`` after each ``Solver.solve()`` call.

The dependency direction is one-way: the entity layer depends on the solver layer. Solver-layer
classes must never import from ``entities/``.

Control Architecture
--------------------

The control layer sits between ``NetworkSimulation`` and ``HeatNetwork``:

- ``NetworkControllerAbstract`` defines the contract: one abstract method,
  ``update_setpoints(time: datetime) -> dict``.
- ``NetworkController`` is the concrete implementation. It holds a list of
  ``ControllerNetwork`` objects — one per hydraulically isolated sub-network. Each
  ``ControllerNetwork`` contains per-asset controller objects
  (``ControllerProducer``, ``ControllerConsumer``, ``ControllerAtesStorage``, etc.) that own
  demand profiles and storage state.
- ``NetworkSimulation`` only calls ``update_network_state`` and ``update_setpoints`` on the
  abstract interface; it does not know about individual asset controllers.

This separation means that the controller can be replaced or mocked without changing
``NetworkSimulation``. The ``NetworkControllerAbstract`` contract is the extension point.

Implementation Notes
--------------------

- The adapter layer (``adapter/``) is the only package that knows about ESDL. Do not add
  ESDL imports to ``entities/`` or ``solver/``.
- ``SimulationManager`` owns the error boundary for a complete run. Keep orchestration logic
  there, not in ``NetworkSimulation``.
- The ``simulation/`` package is intentionally thin. Its only runtime class,
  ``NetworkSimulation``, delegates all physics to ``HeatNetwork`` and all control decisions
  to ``NetworkController``.
- Adding a new asset type requires changes in both ``entities/`` (entity layer) and
  ``solver/`` (solver layer) plus a new mapper in ``adapter/``. See :doc:`developer_guides`
  for step-by-step guidance.

Related Documentation
---------------------

- :doc:`simulation_flow` — detailed execution flow from entrypoint to solver.
- :doc:`developer_guides` — how-to guides for adding assets, output formats, and
  controller extensions.
- :doc:`testing_strategy` — test layout and patterns for each package layer.
- :doc:`../intro/intro_main` — user-facing overview of what the simulator does.
- :doc:`api/omotes_simulator_core` — generated API reference for class and module details.
