.. _solver-producer:

Solver HeatBoundary
+++++++++++++++++++
The `HeatBoundary` solver can represent both a producer and a consumer in the network.  
This choice is made because a consumer behaves like a producer, with heat flow in the opposite 
direction.  
This approach enhances network flexibility, allowing users to set parameters such as pressure and  
mass flow rate for both producers and consumers.

.. autoclass:: omotes_simulator_core.solver.network.assets.production_asset.HeatBoundary
    :members:
