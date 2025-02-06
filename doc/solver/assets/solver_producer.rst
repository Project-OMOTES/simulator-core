.. _solver-producer:

Solver producer class
++++++++++++++++++++++++
The Solver producer class can be used to represent a producer or a consumer in the network. This has 
been chosen since a consumer is the same as a producer, only the heat flow is in the other 
direction. In this way, the network is very flexible to solve, and the user can choose to set 
certain parameters (pressures, mass flow rate) in the producers as well as in the consumers.

.. autoclass:: omotes_simulator_core.solver.network.assets.production_asset.ProductionAsset
    :members:
