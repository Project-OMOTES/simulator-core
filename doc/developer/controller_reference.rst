Controller reference
====================

Purpose
-------

This page is a curated overview of the controller layer: how the ``NetworkController`` is
built from ESDL, how it is split into sub-networks, which per-asset controller classes it
uses, and how it exchanges data with the ``HeatNetwork``. It is meant for contributors who
change dispatch logic, add a controller type for a new asset, or debug setpoints.

For the conceptual dispatch rules and their physical effect, read
:doc:`../controller/controller_behavior`. For a step-by-step extension guide, read
:doc:`ControlExtension`. For the full list of methods, use the generated API reference
(:doc:`api/omotes_simulator_core`).

Relevant modules and files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``entities/network_controller_abstract.py``
     - ``NetworkControllerAbstract``: abstract base with ``update_setpoints(time)``.
     - The interface a controller must offer.
   * - ``entities/network_controller.py``
     - ``NetworkController``: the current controller implementation.
     - Contains the dispatch algorithm across all sub-networks.
   * - ``entities/assets/controller/controller_network.py``
     - ``ControllerNetwork``: one hydraulically separate sub-network.
     - Holds the producers, consumers, storages and heat transfer assets of one circuit,
       and computes totals and per-asset setpoints for it.
   * - ``entities/assets/controller/``
     - Per-asset controllers: ``ControllerProducer``, ``ControllerConsumer``,
       ``ControllerAtesStorage``, ``ControllerIdealHeatStorage``,
       ``ControllerHeatTransferAsset``, all based on ``AssetControllerAbstract``.
     - Hold the limits, profiles and state that dispatch uses for each asset.
   * - ``entities/assets/controller/profile_interpolation.py``
     - ``ProfileInterpolator``: resamples ESDL profiles to the simulation time step.
     - Used by the consumer, producer and storage controller mappers.
   * - ``adapter/transforms/controller_mapper.py``
     - ``EsdlControllerMapper``: builds the ``NetworkController`` from ESDL.
     - Creates the per-asset controllers and partitions them into sub-networks.
   * - ``adapter/transforms/controller_mappers/``
     - One mapper per controller type.
     - Where ESDL attributes and profiles are read for each controller.

Execution or extension flow
---------------------------

Construction
~~~~~~~~~~~~

1. ``SimulationManager.execute`` calls ``EsdlControllerMapper().to_entity(esdl, timestep)``.
2. The mapper builds a connectivity graph with ``EsdlGraphMapper`` and creates per-asset
   controllers. Heat pumps with four ports become heat transfer controllers. Heat pumps with
   two ports, gas heaters and electric boilers become producer controllers.
3. Without heat transfer assets, every controller goes into one ``ControllerNetwork``.
4. With heat transfer assets, the mapper creates one sub-network per circuit, assigns each
   asset by graph reachability, and builds a graph of sub-networks. It raises
   ``RuntimeError`` if that graph is not a tree, or if a sub-network is more than two
   stages away from the reference sub-network (the first one without storage).
5. Each ``ControllerNetwork`` stores its ``path`` to the reference sub-network, which
   ``update_networks_factor`` uses to convert power between circuits.

Per-timestep interface
~~~~~~~~~~~~~~~~~~~~~~

For each time step, ``NetworkSimulation.run``:

1. Calls ``update_network_state(heat_network)``. This reads ``get_state`` from the entity
   asset of every producer, consumer and storage controller and passes it to
   ``set_state``.
2. Calls ``update_setpoints(time)`` once. The result is a dictionary keyed by asset ID,
   with a dictionary of setpoints per asset.
3. Passes that dictionary to ``HeatNetwork.run_time_step`` in the convergence loop (at most
   20 iterations). Setpoints are not recomputed inside this loop.

``update_setpoints`` first updates the sub-network factors, then balances supply and
demand across all sub-networks, sets the heat transfer setpoints, and finally chooses one
pressure-setting asset per sub-network. The full decision order is described in
:doc:`ControlExtension` and :doc:`../controller/controller_behavior`.

Implementation notes
--------------------

- ``NetworkSimulation`` is typed against the concrete ``NetworkController``, and calls
  ``update_network_state``, which is not part of ``NetworkControllerAbstract``. A new
  controller must offer both methods.
- Setpoint keys must match what each entity asset checks in ``set_setpoints``. For
  example, ``ProductionCluster`` needs heat demand, inlet and outlet temperature, and set
  pressure; ``DemandCluster`` needs the same without set pressure.
- Consumption is positive and supply is negative in the heat demand setpoints.
- ``NetworkItems.add`` raises ``ValueError`` for controller types it does not know. A new
  controller type must be added there and in ``ControllerNetwork``.
- ``get_state`` returns data only for ``AtesCluster`` and ``IdealHeatStorage``; for other
  assets ``set_state`` receives an empty dictionary.
- Priority dispatch uses the installed ``power`` of each producer, not its profile.
- Heat transfer setpoints are only set for sub-networks with exactly one heat transfer
  asset. ``ControllerHeatTransferAsset.set_asset_sec`` uses fixed secondary temperatures.
- ``set_pressure`` tries a producer, then a secondary heat transfer asset, then a storage,
  and raises ``ValueError`` if none is present.

Testing and validation
----------------------

- ``unit_test/entities/controller/test_controller_new_class.py`` covers
  ``NetworkController`` dispatch.
- ``unit_test/entities/controller/test_controller_network.py``, ``test_controller_producer.py``,
  ``test_controller_consumer.py``, ``test_controller_storage.py`` and
  ``test_profile_interpolation.py`` cover the sub-network and per-asset controllers.
- ``unit_test/adapters/transforms/controller_mappers/`` covers the mappers, including
  ``test_esdl_controller_mapper.py`` for sub-network partitioning.
- ``unit_test/integration/test_communication_controller_network.py`` checks that the
  controller output is accepted by the network.
- ``unit_test/simulation/test_networksimulation.py`` checks the call order between
  controller and network.

See :doc:`testing_strategy` for commands and test patterns.

Common pitfalls
---------------

- Changing a setpoint key in the controller without changing the entity asset (or the
  other way round).
- Expecting setpoints to react to solver results within one time step.
- Adding a controller type to ``ControllerNetwork`` but not to ``NetworkItems.add``.
- Creating looped or deeply nested heat transfer configurations; the mapper rejects them.
- Describing planned control strategies as if they exist. Only ``NetworkController`` is
  implemented.

Related documentation
---------------------

- :doc:`ControlExtension` — guide for changing or extending control.
- :doc:`architecture` — control hierarchy in the package.
- :doc:`simulation_flow` — where the controller is called.
- :doc:`network_reference` — the ``HeatNetwork`` the controller talks to.
- :doc:`asset_reference` — the entity assets that receive setpoints.
- :doc:`../controller/controller_behavior` — conceptual dispatch behavior.

API reference
-------------

.. toctree::
   :maxdepth: 1

   ../controller/main_controller_class
   ../controller/sub_network_class
   ../controller/assets/asset_controller_abstract
   ../controller/assets/producer
   ../controller/assets/consumer
   ../controller/assets/controller_storage
   ../controller/assets/ates
   ../controller/assets/controller_heat_transfer
   ../controller/assets/controller_network
   ../controller/assets/profile_interpolation
