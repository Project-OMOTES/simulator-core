Extending control behavior
==========================

Purpose
-------

Use this guide when you change how setpoints are computed: new controller parameters, a
controller for a new asset type, different dispatch rules, or a replacement network
controller. It describes the control code as it is implemented today and the extension
paths that the code supports.

For what the controller does conceptually, see :doc:`../controller/controller`. For the
dispatch rules and their effect on results, see :doc:`../controller/controller_behavior`.

Relevant modules and files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 38 22 40

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``src/omotes_simulator_core/entities/network_controller_abstract.py``
     - Abstract interface
     - ``NetworkControllerAbstract`` declares one abstract method,
       ``update_setpoints(time) -> dict``.
   * - ``src/omotes_simulator_core/entities/network_controller.py``
     - Dispatch logic
     - ``NetworkController`` implements ``update_network_state`` and
       ``update_setpoints``: supply and demand balance, storage use, producer priority,
       consumer capping, heat transfer setpoints, and the pressure-setting asset.
   * - ``src/omotes_simulator_core/entities/assets/controller/controller_network.py``
     - Sub-network
     - ``ControllerNetwork`` holds the controllers of one hydraulically connected part and
       builds setpoint dictionaries with methods such as ``set_supply``,
       ``set_consumer_to_demand``, ``set_storage_charge_power``, and ``set_pressure``.
   * - ``src/omotes_simulator_core/entities/assets/controller/asset_controller_abstract.py``
     - Asset controller base
     - ``AssetControllerAbstract(name, identifier)`` stores ``name`` and ``id`` and has a
       no-op ``set_state``. It is not an ABC and declares no setpoint method.
   * - ``src/omotes_simulator_core/entities/assets/controller/controller_producer.py``,
       ``controller_consumer.py``, ``controller_storage.py``,
       ``controller_heat_transfer.py``
     - Asset controllers
     - Hold profiles, limits, temperatures, and storage state, and expose
       ``get_max_power``, ``get_heat_demand``, effective charge and discharge power, or
       ``set_asset_prim`` and ``set_asset_sec``.
   * - ``src/omotes_simulator_core/adapter/transforms/controller_mapper.py``
     - Controller creation
     - ``EsdlControllerMapper.to_entity`` creates asset controllers per asset label, splits
       them into ``ControllerNetwork`` objects, and returns the ``NetworkController``.
   * - ``src/omotes_simulator_core/adapter/transforms/controller_mappers/``
     - Asset controller mappers
     - ``ControllerProducerMapper``, ``ControllerConsumerMapper``,
       ``ControllerAtesStorageMapper``, ``ControllerIdealHeatStorageMapper``,
       ``ControllerHeatPumpMapper``, and ``ControllerHeatExchangeMapper``.
   * - ``src/omotes_simulator_core/entities/assets/asset_defaults.py``
     - Setpoint keys
     - ``PROPERTY_HEAT_DEMAND``, ``PROPERTY_TEMPERATURE_IN``, ``PROPERTY_TEMPERATURE_OUT``,
       ``PROPERTY_SET_PRESSURE``, ``PROPERTY_BYPASS``, and the ``PRIMARY`` and ``SECONDARY``
       prefixes.
   * - ``unit_test/entities/controller/``
     - Controller unit tests
     - One file per asset controller, ``test_controller_network.py``, and
       ``test_controller_new_class.py`` for ``NetworkController``.
   * - ``unit_test/integration/test_communication_controller_network.py``
     - Coupling test
     - Checks that ``update_network_state`` calls ``set_state`` on every producer, consumer,
       and storage controller.

Execution or extension flow
---------------------------

How setpoints are produced
~~~~~~~~~~~~~~~~~~~~~~~~~~

Every timestep ``NetworkSimulation`` calls:

1. ``NetworkController.update_network_state(heat_network)``. For every producer, consumer,
   and storage controller it calls
   ``controller.set_state(heat_network.get_asset_by_id(controller.id).get_state())``. Only
   ``AtesCluster`` and ``IdealHeatStorage`` return a non-empty state; their controllers
   use it to update the effective charge and discharge power.

2. ``NetworkController.update_setpoints(time)``, which:

   a. Updates ``factor_to_first_network`` of each ``ControllerNetwork`` from the heat
      transfer factors along its ``path``.
   b. Sums consumer demand and producer maximum power over all networks, scaled to the
      first network.
   c. If supply exceeds demand, sets consumers to demand and charges storage with the
      surplus. When storage cannot take the whole surplus, it charges storage at maximum and
      sets producers by ``priority``.
   d. Otherwise sets producers to maximum and discharges storage for the shortfall. When
      supply plus storage cannot meet demand, it logs a warning and scales all consumers
      down by the same factor.
   e. For each network with exactly one heat transfer asset, sums the heat demand setpoints
      of that network and calls ``set_asset_prim`` or ``set_asset_sec`` on the heat
      transfer controller. For a heat pump on the secondary side with
      ``max_electrical_power``, consumer setpoints in that network are scaled down first
      when the requested heat exceeds ``max_electrical_power`` times ``factor``.
   f. Asks each network for its pressure-setting asset with ``set_pressure()`` and sets the
      returned key to ``True``.

The result maps asset IDs to setpoint dictionaries and is passed to
``HeatNetwork.run_time_step``.

Extension paths
~~~~~~~~~~~~~~~

Choose the smallest path that does the job:

- **New parameter for an existing controller type.** Read the ESDL value in the controller
  mapper, store it on the asset controller, and use it in ``ControllerNetwork`` or
  ``NetworkController``. ``ControllerProducer.priority`` is read with
  ``esdl_asset.get_strategy_priority()`` in ``ControllerProducerMapper`` and used in
  ``NetworkController._set_producers_based_on_priority``.
- **Existing controller type for a new asset type.** Add a list comprehension to
  ``EsdlControllerMapper.to_entity`` that calls the existing mapper for the new
  ``OmotesAssetLabels`` value, as is done for ``GAS_HEATER`` and ``ELECTRIC_BOILER`` with
  ``ControllerProducerMapper``. See :doc:`AddEntityLayerAsset`.
- **State-dependent control.** Return the state from the entity asset's ``get_state``,
  override ``set_state`` in the asset controller, and use the derived values in the
  dispatch. The storage controllers follow this pattern. ``update_network_state`` only
  covers producers, consumers, and storages; extend it if another category needs state.
- **New controller category.** Add the controller class, a mapper in
  ``controller_mappers/`` exported from its ``__init__.py``, a list in
  ``ControllerNetwork``, a branch in ``NetworkItems.add`` (which raises ``ValueError`` for
  unknown controller types), creation in ``EsdlControllerMapper.to_entity``, and dispatch
  in ``NetworkController.update_setpoints``.
- **Different dispatch rules.** Change ``NetworkController.update_setpoints`` or the
  ``ControllerNetwork`` helper methods. Keep the setpoint dictionary keys described
  below.
- **Replacement network controller.** Subclass ``NetworkControllerAbstract``. Because
  ``NetworkSimulation`` is typed against ``NetworkController`` and also calls
  ``update_network_state``, the replacement must implement that method too, and either
  ``NetworkSimulation`` must be retyped to the abstract class or the replacement must
  subclass ``NetworkController``. ``SimulationManager`` always builds the controller with
  ``EsdlControllerMapper``, so it must be changed to select another controller.

Implementation notes
--------------------

Setpoint dictionary keys
~~~~~~~~~~~~~~~~~~~~~~~~

Entity assets validate the keys they receive, so the controller must provide:

- **Producers and storages:** ``PROPERTY_HEAT_DEMAND``, ``PROPERTY_TEMPERATURE_IN``,
  ``PROPERTY_TEMPERATURE_OUT``, and ``PROPERTY_SET_PRESSURE``. ``ProductionCluster`` raises
  ``ValueError`` when one is missing.
- **Consumers:** ``PROPERTY_HEAT_DEMAND``, ``PROPERTY_TEMPERATURE_IN``, and
  ``PROPERTY_TEMPERATURE_OUT``.
- **Heat transfer assets:** the keys produced by ``set_asset_prim`` and ``set_asset_sec``:
  the quantities above with the ``PRIMARY`` and ``SECONDARY`` prefixes, plus
  ``PROPERTY_BYPASS``. ``HeatPump`` and ``HeatExchanger`` check them per side and raise
  ``ValueError`` when one is missing.

Heat taken from the network is positive and heat delivered to the network is negative:
consumer demand and storage charging are positive, producer supply and storage discharging
are negative.

Each ``ControllerNetwork`` must contain a producer, a secondary heat transfer asset, or a
storage, checked in that order, to set the pressure; otherwise ``set_pressure`` raises
``ValueError``.

Current limitations
~~~~~~~~~~~~~~~~~~~

- ``AssetControllerAbstract`` does not enforce any interface; ``ControllerNetwork`` and
  ``NetworkController`` call type-specific methods directly.
- Heat transfer setpoints are only produced for networks with exactly one heat transfer
  asset.
- ``ControllerHeatTransferAsset.set_asset_sec`` uses fixed temperatures instead of the
  configured ``primary_temperatures`` and ``secondary_temperatures``.
- ``ControllerNetwork.get_total_supply_priority`` uses ``producer.power``, not
  ``get_max_power(time)``, so profiles are ignored when producers are dispatched by
  priority.
- ``EsdlControllerMapper.to_entity`` raises ``RuntimeError`` when heat transfer assets form
  a loop between networks or when a network is more than two stages away from the
  reference network.

Testing and validation
----------------------

- **Asset controller tests** in ``unit_test/entities/controller/``: construct the
  controller directly and test methods such as ``get_max_power``, ``get_heat_demand``,
  ``set_state``, or ``set_asset_prim`` for representative times and states.
- **Dispatch tests** in ``test_controller_new_class.py``: build ``NetworkController`` from
  ``Mock(spec=ControllerNetwork)`` objects and controllers created with
  ``Mock(spec=ControllerConsumer)`` or ``Mock(spec=ControllerStorageAbstract)``, call
  ``update_setpoints``, and assert on the returned dictionary.
- **Mapper tests** in ``unit_test/adapters/transforms/controller_mappers/``, including
  ``test_esdl_controller_mapper.py`` for network splitting.
- **Coupling test** ``test_communication_controller_network.py`` when you change
  ``get_state``, ``set_state``, or ``update_network_state``.
- **Full runs** ``test_heat_physics.py`` and ``test_pressure_physics.py`` to check that
  physics results still match.

Run the full suite with ``ci/linux/test_unit.sh`` or ``ci\win32\test_unit.cmd``. See
:doc:`testing_strategy` for targeted runs with ``--no-cov``.

Common pitfalls
---------------

- **Missing setpoint keys.** A missing key makes the entity asset raise during
  ``run_time_step``; an asset without any entry silently keeps its previous setpoints.
- **Wrong sign.** Supply as a positive heat demand makes a producer extract heat.
- **No pressure asset.** A sub-network without producer, secondary heat transfer asset, or
  storage makes ``set_pressure`` raise ``ValueError``.
- **Unsorted controller.** A controller type not handled in ``NetworkItems.add`` raises
  ``ValueError`` for systems with heat transfer assets, but works without them; test both.
- **Assuming the abstract interface is enough.** ``NetworkSimulation`` also calls
  ``update_network_state``.
- **Expecting exact setpoints in results.** The solver satisfies setpoints only within the
  limits of the physics and the convergence checks; compare results with tolerances.

Related documentation
---------------------

- :doc:`../controller/controller` — conceptual description of control.
- :doc:`../controller/controller_behavior` — dispatch rules and their effect.
- :doc:`simulation_flow` — where the controller is called in a timestep.
- :doc:`AddEntityLayerAsset` — connecting a new asset to an existing controller type.
- :doc:`testing_strategy` — test levels and commands.
- :doc:`api/omotes_simulator_core` — generated class and module reference.
