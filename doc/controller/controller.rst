Control
=======

Overview
--------

The controller translates user demand and operating limits into per-timestep setpoints for the
simulated heat network. It does not solve the hydraulic or thermal state itself. Instead, it
decides how much heat should be requested, supplied, stored, or transferred so that the network and
physics models can evaluate whether that requested operation is feasible.

For users and modelers, the controller is the bridge between scenario input and simulated network
behavior. It determines how demand profiles are propagated to assets, how available production and
storage are allocated, and how coupled networks exchange heat through heat pumps or heat exchangers.

Role in the Simulation Workflow
-------------------------------

At each simulation step, the controller evaluates the current system state and prepares setpoints
for the next network solve. In practice, this means that it:

#. groups hydraulically connected assets into controller-side subnetworks,
#. reads consumer demand and available producer or storage capacity,
#. distributes heat demand across producers, storages, and heat-transfer assets,
#. assigns one pressure-setting location per hydraulically separated part of the system, and
#. passes the resulting setpoints to the network and physics models.

The network model then applies those setpoints when assembling and solving the timestep equations.
The solved pressures, flows, and thermal states determine whether the requested control action can
actually be realized in the system.

Key Concepts
------------

Network controller
    The top-level control component that coordinates all controller-side subnetworks and produces
    the setpoint dictionary used by the simulation step.

Subnetworks
    Hydraulically connected groups of assets. The controller treats each such group as a local
    balancing problem while still coordinating heat exchange between subnetworks.

Consumers
    Demand-side control components that request heat according to their time-dependent demand
    profiles.

Producers
    Supply-side control components that provide heat up to their available capacity and priority.

Storages
    Flexible control components that can absorb or release heat. In the current model this includes
    ideal heat storage and ATES-based storage.

Heat-transfer assets
    Coupling components, such as heat exchangers and heat pumps, that transfer heat between
    subnetworks and introduce conversion or capacity constraints between the connected sides.

Setpoints
    Asset-level control targets passed into the timestep solve. These include requested heat demand
    or supply, temperature targets, and the selected location where pressure is imposed for a
    hydraulic part of the system.

Behavior and Interpretation
---------------------------

What the controller does
~~~~~~~~~~~~~~~~~~~~~~~~

At a high level, the controller tries to satisfy consumer demand with available production first and
then uses storage flexibility when supply and demand do not match exactly. When coupled networks are
present, it also determines how much heat should pass through each heat-transfer asset so that the
connected subnetworks remain consistent.

Setpoint propagation
~~~~~~~~~~~~~~~~~~~~

Setpoints propagate from system demand to individual assets in stages. Consumer demand profiles are
first converted into requested heat offtake. The controller then compares total demand with the
available producer capacity and storage charge or discharge capacity across the relevant
subnetworks. Based on that comparison, it assigns asset-level setpoints for consumers, producers,
storages, and heat-transfer assets.

This means the controller output should be read as a requested operating state, not as a guarantee.
The final delivered heat, temperatures, and flows still depend on the solved network and asset
physics.

Control building blocks
~~~~~~~~~~~~~~~~~~~~~~~

The current control layer is organized around a small number of asset categories:

- the network controller that coordinates the full system,
- subnetworks that represent hydraulically connected parts of the model,
- consumers that request heat,
- producers that inject heat,
- storages, including ideal heat storage and ATES, that shift heat over time,
- heat-transfer assets that connect subnetworks through heat exchangers or heat pumps.

These building blocks matter because each category contributes a different kind of limit or
flexibility to the timestep balance.

Control interaction with network and physics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The controller defines intent, while the network and physics sections determine realization. A
producer setpoint may request heat injection, a consumer setpoint may request offtake, and a
storage setpoint may request charging or discharging, but the solved hydraulic and thermal state
still depends on connectivity, pressure conditions, transport losses, and asset-specific physical
constraints.

Heat-transfer assets are especially important in this interaction. They couple subnetworks and can
limit how much heat is effectively exchanged between the connected sides. As a result, a shortage,
curtailment, or change in dispatch may be caused either by controller allocation or by network and
physics constraints that prevent the requested operating point from being fully realized.

Practical simulation consequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For users and modelers, the most important consequence is that controller results should be
interpreted together with solved network outcomes.

- If total demand exceeds available production and dischargeable storage, consumer delivery may be
  reduced.
- If total supply exceeds demand, storage may absorb surplus heat until its effective charge limit
  is reached.
- If a heat pump or heat exchanger couples subnetworks, the achievable transfer can constrain both
  sides of the system.
- If pressure is imposed at a different asset than expected, flow patterns can still remain valid
  as long as the hydraulic part of the network is properly anchored.

Assumptions
-----------

- Control is evaluated per timestep and produces asset-level setpoints for that timestep.
- Subnetworks are based on hydraulic connectivity and coordinated through heat-transfer assets.
- Storage is represented through effective charge and discharge capability, not through a detailed
  control optimization problem.
- The controller allocates requested operation before the network and physics solve determines the
  final realized state.

Limitations
-----------

- This page gives a conceptual overview only and does not describe detailed timestep dispatch logic.
- It does not replace the asset-level physics interpretation in :doc:`../physics/physics_main`.
- It does not document class internals or contributor-oriented implementation details.
- Detailed controller behavior belongs on the dedicated behavior page.

Implementation Reference
------------------------

For controller classes, controller-side subnetworks, and implementation-oriented reference, see
:doc:`../reference/controller_reference`.

Related Documentation
---------------------

Use :doc:`controller_behavior` for the detailed user-facing explanation of controller behavior
during a timestep.

For network-level interaction and topology context, see :doc:`../network/network_main`.

For asset-level physical interpretation of the resulting operating state, see
:doc:`../physics/physics_main`.

For implementation-oriented controller reference material, see
:doc:`../reference/controller_reference`.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   controller_behavior


