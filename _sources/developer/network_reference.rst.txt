Network reference
=================

Purpose
-------

This page is a curated overview of the network layer: how an ESDL energy system becomes a
connected set of solver assets and nodes, which classes own that structure, and how other
parts of the code talk to it. It is meant for contributors who change network construction,
asset connectivity, or the per-timestep interface between the controller and the solver.

For the physical meaning of nodes and network partitioning, read
:doc:`../network/network_main` and :doc:`../physics/junction_physics`. For the full list of
methods, use the generated API reference (:doc:`api/omotes_simulator_core`).

Relevant modules and files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``entities/heat_network.py``
     - ``HeatNetwork``: entity-level container for entity assets, junctions, the solver
       ``Network`` and the ``Solver``.
     - The only network object that ``NetworkSimulation`` and ``NetworkController`` use.
   * - ``solver/network/network.py``
     - ``Network``: solver-level registry of assets and nodes, and the connection logic.
     - Owns node creation and merging, connectivity checks, and the mapping from the
       solution vector back to assets and nodes.
   * - ``solver/network/assets/node.py``
     - ``Node``: shared hydraulic and thermal state point between asset connection points.
     - Contributes the continuity, energy and pressure equations at every connection.
   * - ``adapter/transforms/mappers.py``
     - ``EsdlEnergySystemMapper``: converts ESDL assets and connections into the network.
     - Passed to ``HeatNetwork`` as the conversion factory; resolves ESDL joints.
   * - ``entities/assets/junction.py``
     - ``Junction``: entity wrapper around a solver ``Node``.
     - Entity-level handle for each node created during construction.
   * - ``unit_test/solver/network/test_network.py``
     - Unit tests for ``Network``.
     - Reference for asset registration, connection and merge behavior.

Execution or extension flow
---------------------------

Construction
~~~~~~~~~~~~

1. ``SimulationManager.execute`` creates
   ``HeatNetwork(EsdlEnergySystemMapper(esdl).to_entity)``.
2. ``HeatNetwork.__init__`` creates an empty solver ``Network`` and calls the conversion
   factory with it. The factory returns the list of entity assets and the list of
   ``Junction`` objects.
3. ``EsdlEnergySystemMapper`` converts every ``ENABLED`` ESDL asset (joints excluded) with
   ``EsdlAssetMapper`` and registers its solver asset with ``Network.add_existing_asset``.
   Assets in other states are skipped with a warning.
4. For every connection point that is not yet connected, the mapper looks up the
   neighbouring ESDL asset. ESDL joints are replaced by the assets behind them (with an
   iteration limit of 10; a ``RuntimeError`` is raised if it is exceeded). The mapper then
   calls ``Network.connect_assets``.
5. ``connect_assets`` creates a new node, attaches the second asset to an existing node,
   or merges two existing nodes and removes the second one. The returned node ID is
   wrapped in a ``Junction``.
6. ``HeatNetwork`` creates the ``Solver`` for the network and builds a lookup from asset ID
   to entity asset.

Per-timestep interface
~~~~~~~~~~~~~~~~~~~~~~

``NetworkSimulation`` and ``NetworkController`` interact only with ``HeatNetwork``:

- ``run_time_step(time, time_step, controller_input)`` sets the time step, time and
  setpoints of each asset whose ID is a key in ``controller_input``, then calls
  ``Solver.solve``.
- ``check_convergence`` returns ``True`` only when every entity asset reports convergence.
- ``post_process_assets`` and then ``store_output`` call ``postprocess`` and
  ``write_to_output`` on every asset, once per time step after the convergence loop.
- ``gather_output`` concatenates the time series of all assets into one data frame.
- ``get_asset_by_id`` is used by ``NetworkController.update_network_state`` to read asset
  state before computing setpoints.

The full per-timestep order is described in :doc:`simulation_flow`.

Implementation notes
--------------------

- ``HeatNetwork`` does not know about ESDL. All ESDL handling lives in the conversion
  factory, so a different source format needs a new factory, not changes in
  ``HeatNetwork``.
- The solver ``Network`` stores assets in a dictionary keyed by **name**, while
  ``HeatNetwork`` looks up entity assets by **ID**. Keep both values unique.
- ``Network.add_asset`` only knows the type strings in ``Network.str_to_class_dict``
  (``Boundary``, ``Asset``, ``Fall``, ``Production``, ``Pipe``, ``HeatTransferAsset``). The
  ESDL path uses ``add_existing_asset`` instead, so new solver asset classes do not need to
  be added to this dictionary unless tests or manual networks create them by type string.
- ``connect_assets`` and ``add_existing_asset`` raise ``ValueError`` for unknown or
  duplicate assets. ``get_asset_by_id`` raises ``KeyError`` for unknown IDs.
- ``Junction`` objects can repeat when several connections resolve to the same node.
- ``Network.remove_asset``, ``Network.disconnect_asset`` and ``HeatNetwork.plot_network``
  are empty stubs. Do not rely on them.
- Node merging rewires all connections of the removed node, so node IDs seen during
  construction are not stable. Use the IDs returned at the end of construction.

Testing and validation
----------------------

- ``unit_test/solver/network/test_network.py`` covers asset registration, connections and
  node merging on the solver ``Network``.
- ``unit_test/solver/network/assets/test_node.py`` covers node equations and connection
  validation.
- ``unit_test/entities/test_entities.py`` builds a ``HeatNetwork`` from an ESDL file.
- ``unit_test/adapters/transforms/test_esdl_graph_mapper.py`` covers the graph mapping
  used for controller sub-networks.
- The integration tests in ``unit_test/integration`` (for example
  ``test_heat_physics.py`` and ``test_pressure_physics.py``) build small networks by hand
  with ``Network`` and ``Solver``. Use them as templates for low-level validation.

See :doc:`testing_strategy` for commands and test patterns.

Common pitfalls
---------------

- Adding ESDL-specific logic to ``HeatNetwork`` instead of the mapper.
- Forgetting that an asset only gets setpoints when its ID is a key in the controller
  output.
- Assuming a ``Junction`` is created for every ESDL joint; joints are absorbed.
- Calling the stub methods ``remove_asset``, ``disconnect_asset`` or ``plot_network`` and
  expecting them to work.
- Reusing an asset name for two assets. Entity assets pass their ESDL name to the solver
  asset, and ``add_existing_asset`` raises ``ValueError`` when that name is already
  registered.

Related documentation
---------------------

- :doc:`architecture` — package layering and the two-layer asset model.
- :doc:`simulation_flow` — per-timestep call order.
- :doc:`solver_reference` — the ``Solver`` and ``Matrix`` that solve the network.
- :doc:`asset_reference` — entity and solver asset classes.
- :doc:`controller_reference` — how controller sub-networks relate to the network.
- :doc:`../network/network_main` — conceptual network description.
- :doc:`../physics/junction_physics` — node equations.

API reference
-------------

.. toctree::
   :maxdepth: 1

   ../solver/network
