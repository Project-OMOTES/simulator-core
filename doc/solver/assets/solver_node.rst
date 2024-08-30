.. _solver-node:

Solver node class
++++++++++++++++++++++++
The node class is split into two to avoid circular import errors. The node is the item conected
different assets. The node has no physical meaning, but is a pure modelling aspect to make it more
easy to connect different assets together. The node is responsible for adding equations for the
mass and energy continuity.

.. autoclass:: omotes_simulator_core.solver.network.assets.base_node_item.BaseNodeItem
    :members:
.. autoclass:: omotes_simulator_core.solver.network.assets.node.Node
    :members:
