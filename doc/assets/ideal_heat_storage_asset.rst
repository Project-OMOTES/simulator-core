.. _ideal-heat-storage-asset:

Ideal heat storage asset
++++++++++++++++++++++++

The **Ideal Heat Storage Asset** is the entity-level representation of a
thermal storage component with charge and discharge operation.

It captures the storage configuration and ports that define how the component
is represented before timestep-by-timestep behavior is solved.

Implemented by
--------------

This reference page documents the ``IdealHeatStorage`` entity in
``omotes_simulator_core.entities.assets.ideal_heat_storage``.

Related documentation
---------------------

- For storage behavior during simulation, see :doc:`../physics/ideal_heat_storage_physics`.
- For control behavior that coordinates storage dispatch, see :doc:`../controller/controller`.

.. autoclass:: omotes_simulator_core.entities.assets.ideal_heat_storage.IdealHeatStorage
   :no-index:
   :members:
