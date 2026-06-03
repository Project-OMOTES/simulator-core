.. _Producer-asset:

Producer asset
+++++++++++++++++++++++++++++++++++++++++++++

The **Producer Asset** is the entity-level representation of a controllable heat
source in the simulation input model.

It groups the metadata, ports, and operating parameters needed to represent heat
production before those values are translated to solver behavior.

Implemented by
--------------

This reference page documents the ``ProductionCluster`` entity in
``omotes_simulator_core.entities.assets.production_cluster``.

Related documentation
---------------------

- For producer behavior during simulation, see :doc:`../physics/producer_physics`.
- For network-level interpretation of pressure and flow, see :doc:`../network/network_main`.


.. autoclass:: omotes_simulator_core.entities.assets.production_cluster.ProductionCluster
   :no-index:
   :members: