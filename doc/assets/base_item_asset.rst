:orphan:

BaseItem (Solver Asset Base)
============================

The ``BaseItem`` class is the abstract foundation for solver-side network items.
It provides shared bookkeeping used by both assets and nodes.

Role
----

- Stores common identity and sizing fields (name, id, number of unknowns, number of ports).
- Stores and resets previous solution values used between solver iterations.
- Provides index mapping into the global matrix via core quantities and connection points.
- Defines abstract interfaces that subclasses must implement (equation generation and disconnection).

Implemented in
--------------

- ``src/omotes_simulator_core/solver/network/assets/base_item.py``
