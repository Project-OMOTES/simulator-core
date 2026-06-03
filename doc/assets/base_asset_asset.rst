:orphan:

BaseAsset (Solver Asset Base Class)
===================================

The ``BaseAsset`` class extends ``BaseItem`` with connection and equation helpers
for solver-side assets.

Role
----

- Manages connection points and linked nodes.
- Validates connection points and connectivity state.
- Provides shared equations for pressure and internal-energy coupling between
  asset ports and connected nodes.
- Exposes helpers used by concrete assets to build their equation sets.

Implemented in
--------------

- ``src/omotes_simulator_core/solver/network/assets/base_asset.py``
