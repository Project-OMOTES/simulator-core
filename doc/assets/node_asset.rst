:orphan:

Node (Solver-Side Junction Model)
=================================

The ``Node`` class represents a junction where multiple assets connect in the
solver network.

Role
----

- Collects connected asset ports.
- Builds node continuity (mass-balance) equations.
- Builds node energy equations and pressure constraints where applicable.
- Acts as communication point between connected assets in matrix assembly.

Implemented in
--------------

- ``src/omotes_simulator_core/solver/network/assets/node.py``
