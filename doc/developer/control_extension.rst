Extending Control Behavior
==========================

Purpose
-------

Use this guide when you need to add a new controller type, extend an existing controller,
modify dispatch logic, or change how setpoints are propagated to assets. This is
implementation-oriented, contributor-facing documentation — not a user-facing conceptual
overview of control.

This page is for contributors who work at the Python implementation level. For conceptual
explanations of what the control system does, consult :doc:`../controller/controller`. For
physical impact and detailed dispatch mechanics, consult :doc:`../controller/controller_behavior`.

Control Architecture for Contributors
-------------------------------------

The control layer is split into three tiers:

**Asset-level controllers** (``entities/assets/controller/``)
    Per-asset classes such as ``ControllerProducer``, ``ControllerConsumer``,
    ``ControllerAtesStorage``, ``ControllerIdealHeatStorage``, ``ControllerHeatTransferAsset``.
    Each inherits from ``AssetControllerAbstract``. They own asset-specific state
    (profiles, demand, stored energy, COP) and the logic to compute per-asset setpoints.

**Network-level controller** (``entities/network_controller.py``)
    The ``NetworkController`` class. It owns a list of ``ControllerNetwork`` objects
    (one per hydraulically isolated sub-network). Each ``ControllerNetwork`` contains the
    asset-level controllers for its sub-network. ``NetworkController`` orchestrates the
    dispatch: update network state, calculate per-network totals, distribute demand across
    producers, and return the setpoints dict.

**Abstract contract** (``entities/network_controller_abstract.py``)
    The ``NetworkControllerAbstract`` base class defines the minimal interface that
    ``NetworkSimulation`` depends on: one abstract method, ``update_setpoints(time)``.
    ``NetworkSimulation`` calls ``update_network_state`` and ``update_setpoints`` on the
    abstract interface; it does not know about individual asset controllers or the
    ``ControllerNetwork`` grouping logic.

Relevant Modules and Files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 38 22 40

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``src/omotes_simulator_core/entities/network_controller_abstract.py``
     - Abstract interface
     - Defines the contract that ``NetworkSimulation`` depends on. Any custom controller
       must inherit from this and implement ``update_setpoints``.
   * - ``src/omotes_simulator_core/entities/network_controller.py``
     - Concrete implementation
     - Current dispatch logic. Owns update orchestration, network-level balancing,
       and producer priority/curtailment. Study this before modifying dispatch.
   * - ``src/omotes_simulator_core/entities/assets/controller/asset_controller_abstract.py``
     - Asset-level base class
     - Minimal contract for per-asset controllers. Defines ``set_state`` (receive network
       state from entity layer) and ``calculate_setpoints`` (return a dict per timestep).
   * - ``src/omotes_simulator_core/entities/assets/controller/controller_network.py``
     - Network grouping
     - Groups asset controllers by hydraulic connectivity. Holds producer, consumer, storage,
       and heat-transfer asset lists. Study when extending to understand sub-network
       isolation and factor adjustment for multi-network systems.
   * - ``src/omotes_simulator_core/entities/assets/controller/controller_producer.py``
     - Producer logic
     - Example: supply-temperature and demand-based setpoint logic for production assets.
   * - ``src/omotes_simulator_core/entities/assets/controller/controller_consumer.py``
     - Consumer logic
     - Example: demand profile and return temperature logic for demand assets.
   * - ``src/omotes_simulator_core/adapter/transforms/controller_mapper.py``
     - ESDL-to-controller mapper
     - ``EsdlControllerMapper.to_entity`` creates the network controller from the ESDL.
       Contains the instantiation dispatch.
   * - ``src/omotes_simulator_core/adapter/transforms/controller_mappers/``
     - Per-asset controller mappers
     - One mapper per asset-level controller type (``controller_producer_mapper.py``,
       ``controller_consumer_mapper.py``, etc.). Each inherits from ``EsdlMapperAbstract``.
   * - ``unit_test/entities/controller/``
     - Controller unit tests
     - Unit tests for all controller classes. Use ``Mock(spec=ControllerNetwork)`` to
       isolate asset controllers from network-level logic.
   * - ``unit_test/integration/test_communication_controller_network.py``
     - Integration coupling test
     - Verifies that ``update_network_state`` correctly propagates entity-layer asset state
       to per-asset controller objects. This is the most important integration test for
       controller changes.

Step-by-step Workflow
---------------------

1. Create or modify an asset-level controller class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Asset controllers live in ``src/omotes_simulator_core/entities/assets/controller/``.

Inherit from ``AssetControllerAbstract``:

.. code-block:: python

    from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
        AssetControllerAbstract,
    )

    class ControllerMyAsset(AssetControllerAbstract):
        def __init__(self, asset_id: str, time_step: float) -> None:
            super().__init__(asset_id, time_step)
            # Initialize asset-specific state (profiles, COP, storage, etc.)

        def set_state(self, state: dict[str, float]) -> None:
            # Called by NetworkController.update_network_state() before each update_setpoints.
            # Receive state dict from entity-layer asset via get_state().
            # Example: read current supply temperature or storage level.
            pass

        def calculate_setpoints(self, time: datetime.datetime) -> dict[str, float]:
            # Called by ControllerNetwork or NetworkController.update_setpoints().
            # Return a dict mapping property names to setpoint values.
            # Example: return {"heat_demand": 100000, "supply_temperature": 55}
            return {}

The two key methods are:

- ``set_state`` — receive current network state (temperature, flow, pressure) from the
  entity-layer asset.
- ``calculate_setpoints`` — compute and return the setpoints for the next solver call.

2. Wire the new asset controller into ControllerNetwork
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Edit ``src/omotes_simulator_core/entities/assets/controller/controller_network.py``.

In the ``ControllerNetwork.__init__`` constructor or in ``EsdlControllerMapper``, add the new
asset controller to the appropriate list:

- ``self.producers`` — for production assets
- ``self.consumers`` — for demand assets
- ``self.storages`` — for storage assets
- ``self.heat_transfer_assets_prim`` or ``self.heat_transfer_assets_sec`` — for heat exchangers
  or heat pumps

Then update ``calculate_setpoints`` inside ``ControllerNetwork`` (if it exists) or inside
``NetworkController.update_setpoints`` to include logic that consults your new controller.

3. Create the controller mapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new file in ``src/omotes_simulator_core/adapter/transforms/controller_mappers/``,
for example ``controller_my_asset_mapper.py``.

Inherit from ``EsdlMapperAbstract``:

.. code-block:: python

    from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract
    from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
        AssetControllerAbstract,
    )
    from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
    from omotes_simulator_core.entities.assets.controller.controller_my_asset import (
        ControllerMyAsset,
    )

    class EsdlControllerMyAssetMapper(EsdlMapperAbstract):

        def to_esdl(self, entity: ControllerMyAsset) -> EsdlAssetObject:
            raise NotImplementedError("EsdlControllerMyAssetMapper.to_esdl()")

        def to_entity(self, esdl_asset: EsdlAssetObject, timestep: float) -> AssetControllerAbstract:
            return ControllerMyAsset(
                asset_id=esdl_asset.esdl_asset.id,
                time_step=timestep,
                # read additional properties with esdl_asset.get_property(name, default)
            )

4. Register the mapper
~~~~~~~~~~~~~~~~~~~~~~~

Open ``src/omotes_simulator_core/adapter/transforms/controller_mapper.py`` and add two changes.

First, import the new mapper:

.. code-block:: python

    from omotes_simulator_core.adapter.transforms.controller_mappers.controller_my_asset_mapper import (
        EsdlControllerMyAssetMapper,
    )

Second, add an entry to the controller dispatch table (inside ``EsdlControllerMapper.to_entity``
or in a dispatch dict):

.. code-block:: python

    mapper = EsdlControllerMyAssetMapper()
    controller = mapper.to_entity(esdl_asset, timestep=config.timestep)

The exact pattern depends on the current controller mapper implementation. Study the existing
mappers for the current pattern.

5. Add unit and integration tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unit tests for the asset-level controller belong in ``unit_test/entities/controller/``.
Follow the pattern of existing controller tests:

.. code-block:: python

    class ControllerMyAssetTest(unittest.TestCase):
        def setUp(self) -> None:
            self.controller = ControllerMyAsset(asset_id="my_asset_id", time_step=3600)

        def test_calculate_setpoints(self) -> None:
            time = datetime.datetime(2020, 1, 1, 0, 0, 0)
            setpoints = self.controller.calculate_setpoints(time)
            self.assertIn("heat_demand", setpoints)
            self.assertIsInstance(setpoints["heat_demand"], (int, float))

        def test_set_state(self) -> None:
            state = {"supply_temperature": 55, "mass_flow": 100}
            self.controller.set_state(state)  # Should not raise

Use ``Mock(spec=ControllerNetwork)`` when you need to mock the network object passed to your
controller.

Integration tests belong in ``unit_test/integration/``. The most relevant integration test
is ``test_communication_controller_network.py``, which verifies that ``update_network_state``
correctly reads from entity-layer assets and propagates state to your controller. Add a test
there if your controller depends on new state properties.

Testing control changes
~~~~~~~~~~~~~~~~~~~~~~~~

Before submitting:

1. Run unit tests for your new or modified controller class:

   .. code-block:: bash

       python -m pytest unit_test/entities/controller/test_controller_my_asset.py

2. Run the integration test that exercises the entity-controller communication:

   .. code-block:: bash

       python -m pytest unit_test/integration/test_communication_controller_network.py

3. Run a full integration test against a real ESDL file that includes your asset type:

   .. code-block:: bash

       python -m pytest unit_test/integration/test_heat_physics.py

4. Run the full suite:

   .. code-block:: bash

       python -m pytest unit_test/

Common Pitfalls
---------------

- **Forgetting to register the mapper**: new controller types that are not registered in
  ``controller_mapper.py`` will silently produce no controller in the network. Always register
  and always add a unit test for the mapper.
- **Breaking the abstract contract**: ``NetworkSimulation`` calls ``update_setpoints`` only.
  Do not require ``NetworkSimulation`` to call additional methods. If your controller needs
  initialization, do it in the constructor or lazily inside ``update_setpoints``.
- **Circular dependencies**: asset controllers must not import from ``HeatNetwork`` or
  ``Solver``. State flow is unidirectional: entity layer reads state from asset and passes
  it to the controller via ``set_state``.
- **Ignoring network isolation**: heat exchangers and heat pumps connect multiple
  ``ControllerNetwork`` objects. If your controller modifies supply temperature or COP based
  on state, test it with a multi-network ESDL file (e.g. with a heat pump that bridges
  two networks).
- **Confusing controller setpoints with solver unknowns**: the controller returns a setpoint
  dict; the solver then solves a nonlinear system to find the state that satisfies both
  the controller's setpoints and the physical equations. Do not expect the solver to produce
  exactly the setpoint values — it produces the closest solution that respects physics.

Related Documentation
---------------------

- Conceptual overview of control: :doc:`../controller/controller`
- Control behavior and dispatch mechanics: :doc:`../controller/controller_behavior`
- Simulation orchestration and control flow: :doc:`simulation_contributor_flow`
- Test layout and patterns: :doc:`testing`
- Full class and module reference: :doc:`api/omotes_simulator_core`
