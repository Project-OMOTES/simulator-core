.. _solver-producer:

Solver producer class
++++++++++++++++++++++++
The Solver producer class can be used to represent a producer or a consumer in the network.
This has been chosen since a consumer is the same as an producer onl the heat flow is in the other
direction. In this way the network is very flexible to solve and the user can chose to set certain
parameters (pressures, mass flow rate) in the producers as well as in the consumers.

.. autoclass:: simulator_core.solver.network.assets.production.ProductionAsset
    :members:
   :members: