Controller
=====================================
This section covers user-facing control behavior in the simulator. It explains how controller logic
produces per-timestep setpoints for assets and how that logic influences network operation.

The controller groups hydraulically connected assets into subnetworks and coordinates demand,
production, storage, and heat-transfer behavior across those subnetworks. During each simulation
step it returns setpoints keyed by asset identifier and controlled property.

How to use this section
-----------------------

- Use this section to understand current control behavior and operating logic during simulation.
- Use Developer Documentation for controller class reference and contributor-facing implementation guidance.
- Use the Network and Physics sections when interpreting how controller decisions affect the solved
    hydraulic and thermal state.

Control behavior in practice
----------------------------

During each timestep, the controller:

- groups hydraulically connected assets into subnetworks,
- evaluates demand, production, storage, and heat-transfer needs within each subnetwork,
- writes per-asset setpoints for temperatures, pressures, mass flows, and thermal power,
- reconciles requested operation with the solved network state.

The resulting setpoints are interpreted by the corresponding asset and network models. This means
control behavior should be read together with the Network and Physics sections when analyzing why a
simulation delivered or curtailed heat, changed flow direction, or clipped storage dispatch.

Implementation reference
------------------------

For controller classes, asset-specific controller components, and lower-level implementation
reference, use :doc:`../reference/controller_reference`.

Control topics
--------------

.. toctree::
    :maxdepth: 1
    :titlesonly:


Related Documentation
---------------------

- For network interaction and topology context, see :doc:`../network/network_main`.
- For asset-level physical interpretation, see :doc:`../physics/physics_main`.
- For developer-facing controller reference material, see :doc:`../reference/controller_reference`.


