:orphan:

FallType (Two-Port Flow Asset Base)
===================================

The ``FallType`` class is a base for two-port assets that include a pressure-loss
relationship and internal continuity/energy behavior.

Role
----

- Defines shared structure for inlet-outlet assets.
- Provides reusable internal equations used by concrete flow assets.
- Serves as the parent class for components such as solver pipes and boundaries.

Implemented in
--------------

- ``src/omotes_simulator_core/solver/network/assets/fall_type.py``
