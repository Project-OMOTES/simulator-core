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
- Use Developer Documentation for contributor-facing control extension guidance and API reference.
- Use the Network and Physics sections when interpreting how controller decisions affect the solved
    hydraulic and thermal state.

**Contents**

.. toctree::
    :maxdepth: 1
    :glob:

    main_controller_class
    sub_network_class
    assets/consumer
    assets/producer
    assets/ates


Related Documentation
---------------------

- For network interaction and topology context, see :doc:`../network/network_main`.
- For asset-level physical interpretation, see :doc:`../physics/physics_main`.
- For developer-facing reference material, see :doc:`../developer/developer_main`.


