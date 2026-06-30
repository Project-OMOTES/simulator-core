Controller Behavior
===================

Overview
--------

This page describes the network-level controller behavior that runs once per simulation timestep.
It explains how the controller groups assets into controllable subnetworks, balances consumer
requests against producer and storage capability, and writes per-asset setpoints that the network
solver then applies.

The controller does not solve hydraulics or asset-internal thermodynamics itself. Instead, it
decides target heat transfer, temperatures, bypass use for heat-transfer assets, and which asset in
each hydraulic part of the system becomes the pressure-setting boundary. The solved network state
then determines the resulting mass flows, pressures, temperatures, and any difference between
requested and delivered heat.

The timestep control path is centered on ``NetworkController.update_setpoints()``. It converts all
local subnetwork demand and capacity to a common basis, performs a system-level heat balance, then
projects the resulting dispatch back onto producers, consumers, storages, and heat-transfer assets.
The controller therefore decides requested operation, while the network and physics models decide
the physically realized state.

Control Inputs
--------------

The network-level controller reads the following inputs each timestep.

.. list-table::
   :header-rows: 1

   * - Input
     - Description
     - Unit
   * - Consumer heat demand profile
     - Requested consumer heat demand from each consumer controller at the current timestep
     - W
   * - Producer maximum power
     - Available thermal output from each producer at the current timestep
     - W
   * - Producer priority
     - Integer dispatch priority used when supply must be capped under surplus conditions
     - -
   * - Storage effective maximum charge power
     - Available storage charging capability used for surplus allocation
     - W
   * - Storage effective maximum discharge power
     - Available storage discharging capability used for shortage allocation
     - W
   * - Heat-transfer conversion factor
     - Factor used to translate heat between subnetworks across a heat exchanger or heat pump
     - -
   * - Heat-pump maximum electrical power
     - Optional electrical input limit on a secondary-side heat-pump network
     - W
   * - Controller temperatures
     - Fixed inlet and outlet temperature setpoints carried by producer, consumer, storage, and heat-transfer controllers
     - K
   * - Previous solved asset state
     - State fed back from the solved heat network into producers, consumers, and storages before the next dispatch update
     - asset-specific

Decision Logic
--------------

Control Decomposition Into Subnetworks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The controller is built from hydraulically separated subnetworks created by the ESDL controller
mapper. If the model contains no heat-transfer assets, all consumers, producers, and storages are
placed in one controller network. If heat exchangers or four-port heat pumps are present, the
mapper splits the system into one controller network for each connected hydraulic side and places
the heat-transfer asset on both sides.

.. list-table::
   :header-rows: 1

   * - Subnetwork element
     - Mapping rule
     - Consequence for control
   * - Consumer, producer, storage
     - Assigned to the hydraulic side to which its asset id is connected in the ESDL graph
     - Demand, supply, and storage capability are first evaluated locally per hydraulic part
   * - Heat exchanger or four-port heat pump, primary side
     - Added to the controller network connected to ``<asset>_primary``
     - This side can import or export heat depending on the net dispatch direction
   * - Heat exchanger or four-port heat pump, secondary side
     - Added to the controller network connected to ``<asset>_secondary``
     - This side can import or export heat with the configured conversion factor

The mapper then connects these subnetworks into a tree through shared heat-transfer assets. Looped
connections through heat exchangers or heat pumps are rejected, and connections through more than
two heat-transfer stages are not supported.

Each subnetwork stores a path to a reference network and a conversion chain
``factor_to_first_network``. The controller multiplies the heat demand, producer capacity, and
storage charge or discharge capacity of that subnetwork by the product of that chain before forming
the system-wide energy balance. For a heat exchanger this factor is the configured efficiency-like
conversion factor; for a heat pump it is the configured COP-like factor on the secondary side and
its inverse when converting back toward the primary side.

Per-Timestep Control Sequence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The network-level control path follows a fixed sequence:

1. Update each subnetwork conversion chain from its path through heat-transfer assets.
2. Convert each subnetwork's consumer demand, producer capacity, and storage charge or discharge
   capability to the reference-network basis.
3. Form system totals:

   .. math::

      Q_{demand,tot} = \sum_i Q_{demand,i}

   .. math::

      Q_{supply,tot} = \sum_i Q_{supply,i}

4. Choose one of four dispatch branches: direct surplus, surplus with producer capping, shortage
   covered by storage discharge, or shortage with proportional consumer curtailment.
5. Write producer, storage, and consumer setpoints.
6. For subnetworks that contain exactly one heat-transfer connection, derive the corresponding
   primary-side and secondary-side setpoints for that heat-transfer asset.
7. Choose one pressure-setting asset per subnetwork and set its pressure flag.

Dispatch Logic for Supply, Demand, and Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The controller first compares converted total producer capability with converted total consumer
demand.

If

.. math::

   Q_{supply,tot} > Q_{demand,tot}

the system has surplus producer capability. All consumers are assigned their requested demand. The
remaining surplus

.. math::

   Q_{surplus} = Q_{supply,tot} - Q_{demand,tot}

is then compared with total effective storage charge capability.

If storage can absorb the full surplus, all producers are set to maximum output and the controller
allocates storage charging proportionally to available charge power:

.. math::

   f_{charge} = \frac{Q_{surplus}}{\sum_i Q_{charge,max,i}}

.. math::

   Q_{storage,i} = f_{charge} Q_{charge,max,i}

with positive heat demand, meaning heat is taken from the network and stored.

If storage cannot absorb the full surplus, all storages are charged at maximum and producers are
capped by priority. The controller fills producer groups in ascending priority order until the
required supply is reached. If the last active priority group would overshoot the required supply,
that entire group is scaled by a common factor while higher-priority groups are set to zero.

If

.. math::

   Q_{supply,tot} \leq Q_{demand,tot}

the system is short of direct producer capability. The controller compares total producer capability
plus total effective storage discharge capability against demand.

If

.. math::

   Q_{supply,tot} + Q_{discharge,tot} > Q_{demand,tot}

all consumers keep their requested demand, all producers are set to maximum, and storage discharge
supplies the residual shortage:

.. math::

   Q_{shortage} = Q_{demand,tot} - Q_{supply,tot}

.. math::

   f_{discharge} = \frac{Q_{shortage}}{\sum_i Q_{discharge,max,i}}

.. math::

   Q_{storage,i} = -f_{discharge} Q_{discharge,max,i}

with negative heat demand, meaning heat is injected from storage into the network.

If

.. math::

   Q_{supply,tot} + Q_{discharge,tot} \leq Q_{demand,tot}

the controller cannot meet total demand even with full storage discharge. It therefore sets all
producers and storages to maximum delivery and scales every consumer by the same curtailment factor:

.. math::

   f_{curtail} = \frac{Q_{supply,tot} + Q_{discharge,tot}}{Q_{demand,tot}}

.. math::

   Q_{consumer,i} = f_{curtail} Q_{consumer,requested,i}

This is a system-wide proportional curtailment rule on the converted-demand basis.

The controller uses the asset sign convention implemented by ``ControllerNetwork``:

- Consumer heat demand is positive, representing heat extraction from the network.
- Storage charging is positive, representing heat moving from the network into storage.
- Producer dispatch is negative, representing heat injected from the producer into the network.
- Storage discharge is negative, representing heat injected from storage into the network.

Heat-Transfer Asset Handling Across Primary and Secondary Networks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After producer, consumer, and storage setpoints are assembled, the controller derives setpoints for
heat exchangers and four-port heat pumps on subnetworks that have exactly one heat-transfer asset
connected on either the primary or secondary side. For such a subnetwork it forms the algebraic sum
of all already assigned producer, consumer, and storage heat-demand setpoints:

.. math::

   Q_{net} = \sum Q_{producer} + \sum Q_{consumer} + \sum Q_{storage}

The sign of ``Q_net`` determines the direction of transfer.

For a network that sees the heat-transfer asset on its primary side:

- If ``Q_net < 0``, the primary side must deliver heat into that subnetwork. The controller calls
  ``set_asset_prim(Q_net, bypass=False)``.
- If ``Q_net >= 0``, the primary side does not need conversion-assisted delivery into that
  subnetwork. The controller calls ``set_asset_prim(Q_net, bypass=True)``.

For a network that sees the heat-transfer asset on its secondary side:

- If ``Q_net < 0``, the secondary side must deliver heat into that subnetwork. The controller calls
  ``set_asset_sec(Q_net, bypass=True)``.
- If ``Q_net >= 0``, the secondary side must absorb heat and the controller calls
  ``set_asset_sec(Q_net, bypass=False)``.

With conversion active, the heat-transfer asset writes paired primary-side and secondary-side heat
demands using its configured factor. In simplified form:

.. math::

   Q_{sec} = f Q_{prim}

or, when dispatch is defined from the secondary side,

.. math::

   Q_{prim} = \frac{Q_{sec}}{f}

where ``f`` is the exchanger efficiency-like factor or the heat-pump COP-like factor used by the
controller.

Heat-Pump Electrical Power Constraint on a Secondary Network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The controller includes one additional rule for a subnetwork that contains exactly one
secondary-side heat-pump connection with a configured maximum electrical power. Before writing the
heat-transfer setpoints, it checks whether the requested thermal exchange on that secondary network
would exceed the electrical limit:

.. math::

   Q_{sec,max} = P_{el,max} f

If

.. math::

   |Q_{net}| > Q_{sec,max}

the controller proportionally scales only the consumers in that subnetwork:

.. math::

   f_{hp} = \frac{Q_{sec,max}}{|Q_{net}|}

.. math::

   Q_{consumer,i,new} = f_{hp} Q_{consumer,i,old}

After this rescaling it recomputes the network heat balance and only then generates the heat-pump
primary-side and secondary-side setpoints. This means the electrical limit is enforced on the
secondary-network thermal request before the asset-level heat-pump physics is solved.

Pressure-Setting Behavior
~~~~~~~~~~~~~~~~~~~~~~~~~

Each subnetwork must contribute one pressure-setting boundary. ``ControllerNetwork.set_pressure()``
selects that asset by fixed precedence:

1. First producer in the subnetwork, if any.
2. Otherwise the first secondary-side heat-transfer asset in the subnetwork.
3. Otherwise the first storage in the subnetwork.

The selected setpoint key is ``set_pressure`` for producers and storages, or
``secondary_set_pressure`` for a secondary-side heat-transfer asset. No primary-side heat-transfer
asset is selected directly by this rule.

Setpoints Produced
------------------

The network-level controller returns a per-asset dictionary keyed by asset id and controlled
property.

.. list-table::
   :header-rows: 1

   * - Setpoint
     - Description
     - Unit
   * - ``heat_demand``
     - Producer, consumer, or storage thermal setpoint on a single hydraulic network
     - W
   * - ``temperature_in``
     - Asset inlet temperature setpoint used by the receiving asset model
     - K
   * - ``temperature_out``
     - Asset outlet temperature setpoint used by the receiving asset model
     - K
   * - ``set_pressure``
     - Pressure-setting flag for a producer or storage selected as the hydraulic reference
     - -
   * - ``primary_heat_demand``
     - Heat-transfer asset primary-side thermal setpoint
     - W
   * - ``primary_temperature_in``
     - Heat-transfer asset primary-side inlet temperature setpoint
     - K
   * - ``primary_temperature_out``
     - Heat-transfer asset primary-side outlet temperature setpoint
     - K
   * - ``secondary_heat_demand``
     - Heat-transfer asset secondary-side thermal setpoint
     - W
   * - ``secondary_temperature_in``
     - Heat-transfer asset secondary-side inlet temperature setpoint
     - K
   * - ``secondary_temperature_out``
     - Heat-transfer asset secondary-side outlet temperature setpoint
     - K
   * - ``secondary_set_pressure``
     - Pressure-setting flag when the hydraulic reference is a secondary-side heat-transfer asset
     - -
   * - ``bypass``
     - Flag indicating whether the heat-transfer asset should bypass conversion and pass the request through directly
     - -

Physical Impact
---------------

Practical Effects on the Solved Hydraulic and Thermal State
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The controller writes requested thermal operation, but the solved network determines the resulting
mass flows, temperatures, and pressures. The physical impact of the controller is therefore best
read as a change in boundary conditions for the next network solve.

Consumer Delivery Under Shortage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When the system enters the shortage branch, every consumer request is reduced by the same scalar
factor. The practical consequence is that unmet demand is distributed proportionally across all
consumers rather than by location, priority, or hydraulic accessibility.

For interpreting results this means:

- a consumer can receive less heat because of explicit controller curtailment before the network is solved,
- and the solved delivery can differ further from the curtailed request if hydraulics or available temperatures prevent exact realization.

For the asset-level heat-to-mass-flow relation and reported delivered heat, see
:doc:`../physics/consumer_physics`.

Producer Dispatch and Capping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Producer dispatch controls how much thermal power is made available to the network and whether a
producer participates at all in a surplus case. When producer priorities are used to cap supply,
lower-priority groups can remain fully loaded while the marginal priority group is uniformly scaled
and higher-priority groups are forced to zero.

This affects the solved hydraulic state because the active set of pressure-driven or
mass-flow-imposing producers changes between timesteps. As a result, flow magnitudes and pressure
distribution can shift even when total delivered demand is unchanged. For the producer-side physics
of heat injection and pressure-controlled operation, see :doc:`../physics/producer_physics`.

Storage Charge and Discharge Allocation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Storage participation is limited by the effective maximum charge and discharge powers provided by
the storage controllers. The network-level controller allocates surplus charging or shortage
discharge in proportion to these effective powers:

.. math::

   Q_{storage,i} = f Q_{storage,max,i}

This means storage is not dispatched by cost, state-of-charge optimization, or location-specific
hydraulic advantage. It is clipped only by available effective charge or discharge power and then
shared proportionally across all participating storages.

The practical consequence is that storage can absorb or release only as much heat as its current
controller state allows. Once that capability is exhausted, additional surplus forces producer
capping and additional shortage forces consumer curtailment. For ATES-side physical interpretation,
see :doc:`../physics/ates_cluster_physics`.

Heat-Transfer Conversion Between Networks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Heat-transfer assets connect hydraulic subnetworks while changing the thermal power seen on each
side according to the configured conversion factor. The controller first balances the system on a
common reference basis and then writes paired primary-side and secondary-side requests. A secondary
network can therefore show larger thermal throughput than its connected primary network when a heat
pump COP greater than one is active.

The direction of the net subnetwork demand also determines whether conversion is active or a bypass
flag is written. That choice changes whether the solved model interprets the coupling as factor-
based transfer between networks or as a direct pass-through request on both sides. For the four-
port heat-pump asset physics, see :doc:`../physics/heat_pump_physics`. For two-port heat pumps
modeled as producers, see :doc:`../physics/air_to_water_heat_pump_physics`.

Pressure-Setting Choice
~~~~~~~~~~~~~~~~~~~~~~~

The pressure flag selects which asset anchors each hydraulic subnetwork. This is the controller's
only direct pressure decision. All other pressures arise from the network solve. Changing which
asset carries the pressure flag changes the boundary condition used by the hydraulic model and can
therefore alter solved flow distribution and pressure levels throughout that subnetwork, even if the
same total heat setpoints are requested.

For broader network interpretation, see :doc:`../network/network_main`.

.. _controller-behavior-assumptions:

Assumptions
-----------

- Control decisions are instantaneous within a timestep; the controller has no internal ramping, startup, or shutdown dynamics.
- Consumer demand profiles and producer maximum powers are treated as known for the current timestep.
- System-wide balancing is performed on converted thermal power totals, not on a hydraulic feasibility check before dispatch.
- Storage allocation is proportional to effective charge or discharge capability.
- Consumer curtailment under shortage is proportional across all consumers.
- Pressure selection uses a fixed precedence rule rather than an optimization or hydraulic-quality criterion.

.. _controller-behavior-limitations:

Limitations
-----------

- The network grouping built by the controller mapper must form a tree through heat-transfer assets; looped heat-transfer topologies are not supported.
- Connections through more than two heat-transfer stages are rejected.
- Heat-transfer setpoints are only derived for subnetworks that contain exactly one connected heat-transfer asset side.
- The producer-capping rule uses integer priorities only and does not include cost, emissions, or efficiency optimization.
- The secondary-side heat-pump electrical constraint is enforced by scaling consumers in that subnetwork; it does not re-optimize the rest of the system dispatch.
- The network-level controller does not guarantee that the solved hydraulic or thermal state can realize every requested setpoint exactly.

Related Documentation
---------------------

- :doc:`../controller/controller` for the conceptual control overview.
- :doc:`../network/network_main` for how controller setpoints become solved network states.
- :doc:`../physics/producer_physics` for producer-side heat injection behavior.
- :doc:`../physics/consumer_physics` for consumer-side heat extraction behavior.
- :doc:`../physics/ates_cluster_physics` for ATES storage physics.
- :doc:`../physics/heat_pump_physics` for four-port heat-pump behavior across primary and secondary networks.
- :doc:`../physics/air_to_water_heat_pump_physics` for two-port heat pumps mapped as producers.
- :doc:`../reference/controller_reference` for controller implementation reference.