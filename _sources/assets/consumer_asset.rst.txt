.. _Consumer-asset:

Consumer asset
+++++++++++++++++++++++++++++++++++++++++++++

The **Consumer Asset** is the entity-level representation of a controllable heat
sink in the simulation input model.

It groups the metadata, ports, and operating parameters needed to represent
heat demand before those values are translated to solver behavior.

Implemented by
--------------

This reference page documents the ``DemandCluster`` entity in
``omotes_simulator_core.entities.assets.demand_cluster``.

Related documentation
---------------------

- For consumer behavior during simulation, see :doc:`../physics/consumer_physics`.
- For network-level interpretation of available flow and inlet state, see :doc:`../network/network_main`.


.. autoclass:: omotes_simulator_core.entities.assets.demand_cluster.DemandCluster
   :no-index:
   :members:

