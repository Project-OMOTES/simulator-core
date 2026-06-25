.. _Pipe-asset:

Pipe asset
+++++++++++++++++++++++++++++++++++++++++++++

The **Pipe Asset** is the entity-level representation of a network pipe that
transports fluid between connected assets.

It captures the design and operating properties that define hydraulic losses,
thermal exchange, and connectivity before those values are mapped to the solver.

Implemented by
--------------

This reference page documents the ``Pipe`` entity in
``omotes_simulator_core.entities.assets.pipe``.

Related documentation
---------------------

- For pipe behavior during simulation, see :doc:`../physics/pipe_physics`.
- For network connectivity and solved state variables, see :doc:`../network/network_main`.

.. autoclass:: omotes_simulator_core.entities.assets.pipe.Pipe
   :no-index:
   :members: