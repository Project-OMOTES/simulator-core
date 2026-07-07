Controller Behavior
===================

Description
-----------

This page documents what the network-level controller decides in each simulation timestep and how
those decisions affect the solved thermal and hydraulic state.

The controller groups assets into hydraulically separated controller subnetworks, converts local
demand and capacity to a common basis, applies a system-level dispatch rule, then writes per-asset
setpoints for producers, consumers, storages, and heat-transfer assets.

It does not solve network hydraulics or asset-internal thermodynamics. Instead, it defines thermal
and pressure-related boundary requests that are applied by the network and physics models in the
next solve step.

Control Inputs
--------------

The network-level dispatch reads the following quantities each timestep.

.. list-table::
   :header-rows: 1

   * - Input
     - Description
     - Unit
   * - Consumer heat-demand profile
     - Requested thermal demand from each consumer controller at the current timestep, clipped by
       the consumer ``max_power`` in the consumer controller
     - W
   * - Producer available power
     - Maximum producer thermal output at the current timestep from each producer controller
     - W
   * - Producer priority
     - Integer priority used for surplus producer capping when storage charging is saturated
     - -
   * - Storage effective maximum charge power
     - Current charging capability reported by each storage controller
     - W
   * - Storage effective maximum discharge power
     - Current discharging capability reported by each storage controller
     - W
   * - Heat-transfer conversion factor
     - Asset factor used to convert thermal power between primary and secondary subnetworks
     - -
   * - Water-to-water heat-pump maximum electrical power
     - Optional secondary-side electrical limit used to cap secondary-side thermal request
     - W
   * - Controller temperatures
     - Asset controller supply and return temperature setpoints used when writing setpoints
     - K
   * - Previous solved storage state
     - Fill level, buffer temperatures, and timestep fed back to storage controllers before
       dispatch so effective charge and discharge capability can be updated
     - asset-specific

Decision Logic
--------------

Subnetwork Grouping and Conversion Basis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The controller receives subnetworks from the controller mapper. If no heat-transfer asset is
present, all producers, consumers, and storages are dispatched in one controller network.
If heat-transfer assets are present, each hydraulic side is represented by a separate controller
network, and heat-transfer assets connect those controller networks by primary and secondary sides.

The mapper enforces a tree-shaped interconnection through heat-transfer assets. Looped
interconnections are rejected, and paths longer than two heat-transfer stages are rejected.

Before balancing demand and supply, each network computes a conversion chain to a reference network
through the path of connected heat-transfer assets. The chain product is used to convert local
consumer demand, producer capacity, and storage charge or discharge capability to one common basis.

In simplified form, for network :math:`i`:

.. math::

   F_i = \prod_k f_{i,k}

.. math::

   Q_{demand,i}^{ref} = F_i Q_{demand,i}, \quad
   Q_{supply,i}^{ref} = F_i Q_{supply,i}, \quad
   Q_{storage,i}^{ref} = F_i Q_{storage,i}

where :math:`f_{i,k}` is the factor contributed by each heat-transfer step in the path.

Per-Timestep Dispatch Sequence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each timestep, the network controller applies this sequence:

1. Update network conversion chains.
2. Compute converted totals:

   .. math::

      Q_{demand,tot} = \sum_i Q_{demand,i}^{ref}

   .. math::

      Q_{supply,tot} = \sum_i Q_{supply,i}^{ref}

3. Choose the dispatch branch from the demand-versus-supply comparison.
4. Write producer, consumer, and storage heat-demand setpoints.
5. Derive setpoints for subnetworks with exactly one connected heat-transfer side.
6. Select one pressure-setting asset per subnetwork.

Dispatch Logic for Supply, Demand, and Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first branch condition is:

.. math::

   Q_{supply,tot} > Q_{demand,tot}

If true, all consumers are set to requested demand and the surplus is:

.. math::

   Q_{surplus} = Q_{supply,tot} - Q_{demand,tot}

The controller compares this surplus to total effective storage charge capability:

.. math::

   Q_{ch,tot} = \sum_i Q_{ch,max,i}^{ref}

If :math:`Q_{ch,tot} > Q_{surplus}`, producers are set to maximum and storage charging is
allocated proportionally:

.. math::

   f_{ch} = \frac{Q_{surplus}}{Q_{ch,tot}}, \quad
   Q_{storage,i} = f_{ch} Q_{ch,max,i}

If :math:`Q_{ch,tot} \leq Q_{surplus}`, all storages charge at maximum and producer output is
capped by priority to match demand plus maximum storage charge.

If :math:`Q_{supply,tot} \leq Q_{demand,tot}`, the controller evaluates shortage support from
storage discharge:

.. math::

   Q_{dis,tot} = \sum_i Q_{dis,max,i}^{ref}

If :math:`Q_{supply,tot} + Q_{dis,tot} > Q_{demand,tot}`, all consumers keep requested demand,
all producers are set to maximum, and storage discharge supplies the residual shortage:

.. math::

   Q_{short} = Q_{demand,tot} - Q_{supply,tot}

.. math::

   f_{dis} = \frac{Q_{short}}{Q_{dis,tot}}, \quad
   Q_{storage,i} = - f_{dis} Q_{dis,max,i}

If :math:`Q_{supply,tot} + Q_{dis,tot} \leq Q_{demand,tot}`, all producers and storages are set
to maximum delivery and consumer demand is proportionally curtailed:

.. math::

   f_{curtail} = \frac{Q_{supply,tot} + Q_{dis,tot}}{Q_{demand,tot}}, \quad
   Q_{consumer,i} = f_{curtail} Q_{consumer,i}^{req}

Storage fill-level effect on effective capability
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The dispatch branches above use effective storage capability, not only configured
``max_charge_power`` and ``max_discharge_power``.

For ``ControllerIdealHeatStorage``, effective capability is updated from the solved previous state
before dispatch. In practical terms:

- charge capability decreases as available cold volume shrinks near full fill level,
- discharge capability decreases as available hot volume shrinks near empty fill level,
- both capabilities are also limited by current hot-cold temperature difference and timestep.

This means the controller clips storage participation near empty or full bounds even when nominal
power ratings are high. As a result, producer capping (in surplus) or consumer curtailment
(in shortage) can start earlier than expected from nominal ratings alone.

For storage-internal relations and symbol definitions, see
:doc:`../physics/ideal_heat_storage_physics`.

Heat-Transfer Conversion and Water-to-Water Heat-Pump Limit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After producer, consumer, and storage setpoints are assembled, each subnetwork with exactly one
connected heat-transfer side computes net local request:

.. math::

   Q_{net} = \sum Q_{producer} + \sum Q_{consumer} + \sum Q_{storage}

The sign of :math:`Q_{net}` determines whether conversion is active or bypassed when writing
primary-side and secondary-side setpoints.

With conversion active, the controller writes paired thermal requests using the configured factor
:math:`f`:

.. math::

   Q_{sec} = f Q_{prim}

or, when the request is defined on the secondary side,

.. math::

   Q_{prim} = \frac{Q_{sec}}{f}

For a secondary-side water-to-water heat-pump connection with a configured electrical limit,
the controller applies:

.. math::

   Q_{sec,max} = P_{el,max} f

If :math:`|Q_{net}| > Q_{sec,max}`, consumers in that subnetwork are proportionally scaled:

.. math::

   f_{hp} = \frac{Q_{sec,max}}{|Q_{net}|}, \quad
   Q_{consumer,i,new} = f_{hp} Q_{consumer,i,old}

The heat-transfer setpoints are then recalculated from the rescaled subnetwork request.

Pressure-Setting Asset Selection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each controller subnetwork must provide one pressure-setting boundary. Selection precedence is:

1. first producer in the subnetwork,
2. otherwise first secondary-side heat-transfer asset,
3. otherwise first storage asset.

The controller sets the selected pressure flag key to ``True`` and leaves other pressure flags
``False``.

Setpoints Produced
------------------

The controller returns a dictionary keyed by asset identifier with the following setpoint keys.

.. list-table::
   :header-rows: 1

   * - Setpoint
     - Description
     - Unit
   * - ``heat_demand``
     - Thermal request for producer, consumer, or storage assets
     - W
   * - ``temperature_in``
     - Inlet temperature setpoint for producer, consumer, or storage assets
     - K
   * - ``temperature_out``
     - Outlet temperature setpoint for producer, consumer, or storage assets
     - K
   * - ``set_pressure``
     - Pressure-setting flag for selected producer or storage asset
     - -
   * - ``primary_heat_demand``
     - Primary-side heat-transfer thermal request
     - W
   * - ``primary_temperature_in``
     - Primary-side inlet temperature setpoint for heat-transfer asset
     - K
   * - ``primary_temperature_out``
     - Primary-side outlet temperature setpoint for heat-transfer asset
     - K
   * - ``primary_set_pressure``
     - Primary-side pressure flag on heat-transfer asset setpoint payload
     - -
   * - ``secondary_heat_demand``
     - Secondary-side heat-transfer thermal request
     - W
   * - ``secondary_temperature_in``
     - Secondary-side inlet temperature setpoint for heat-transfer asset
     - K
   * - ``secondary_temperature_out``
     - Secondary-side outlet temperature setpoint for heat-transfer asset
     - K
   * - ``secondary_set_pressure``
     - Secondary-side pressure-setting flag for selected heat-transfer asset
     - -
   * - ``bypass``
     - Flag controlling whether conversion factor is bypassed for the heat-transfer request
     - -

Physical Impact
---------------

Demand Satisfaction and Curtailment Consequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Decision:
When :math:`Q_{supply,tot} + Q_{dis,tot} \leq Q_{demand,tot}`, the controller proportionally
curtails all consumers.

Governing relation:

.. math::

   Q_{consumer,i} = f_{curtail} Q_{consumer,i}^{req}, \quad
   f_{curtail} = \frac{Q_{supply,tot} + Q_{dis,tot}}{Q_{demand,tot}}

Practical consequence:
The requested heat presented to the network is reduced before solving hydraulics. Reported
delivered heat may be lower still if hydraulic or thermal conditions cannot realize the curtailed
request exactly. For consumer asset-level behavior, see :doc:`../physics/consumer_physics`.

Storage Clipping and Dispatch Branch Switching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Decision:
Storage contribution is bounded by effective charge and discharge capability derived from current
state.

Governing relation:

.. math::

   Q_{storage,i} = f Q_{storage,max,i}^{eff}

where :math:`Q_{storage,max,i}^{eff}` is the current effective limit used by dispatch.

Practical consequence:
As storages approach full or empty conditions, effective capability clips and less thermal buffering
is available to balance mismatch. This can trigger producer capping in surplus periods or consumer
curtailment in shortage periods. For storage-internal equations, see
:doc:`../physics/ideal_heat_storage_physics` and :doc:`../physics/ates_cluster_physics`.

Heat-Transfer Setpoints and Inter-Network Balance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Decision:
The controller converts net subnetwork request into paired primary-side and secondary-side
setpoints, optionally with bypass.

Governing relation:

.. math::

   Q_{sec} = f Q_{prim}

Practical consequence:
Thermal request is redistributed between hydraulic subnetworks according to conversion factor, so
the solved mass flow and temperature levels on each side can differ while still satisfying the
controller-level converted balance. For water-to-water heat-pump asset physics, see
:doc:`../physics/heat_pump_physics`.

Pressure Boundary Selection
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Decision:
One asset per subnetwork is marked as pressure-setting by fixed precedence.

Governing relation:
The controller sets one pressure flag key to ``True`` per subnetwork.

Practical consequence:
The selected asset becomes the hydraulic pressure boundary for that subnetwork solve. Changing this
selection changes hydraulic boundary conditions and can alter solved pressure and flow distribution.
For network-level interpretation, see :doc:`../network/network_main`.

Assumptions
-----------

- Controller decisions are instantaneous within a timestep.
- Demand profiles and available producer power are treated as known at dispatch time.
- Dispatch balancing is performed on converted thermal power totals, not on a prior hydraulic
  feasibility optimization.
- Storage participation is allocated proportionally to effective capability.
- Consumer curtailment is proportional across consumers when total supply is insufficient.
- Pressure-setting selection follows fixed precedence, not an optimization criterion.

Limitations
-----------

- Heat-transfer-connected controller networks must form a tree; looped topologies are not
  supported.
- Paths through more than two heat-transfer stages are not supported.
- Heat-transfer setpoints are generated only for subnetworks with exactly one connected
  heat-transfer side.
- Surplus producer capping uses integer priority groups only; no cost or emission optimization is
  performed.
- The secondary-side water-to-water heat-pump electrical constraint is enforced by local consumer
  scaling in that subnetwork.
- Controller setpoints are requests; the solved network may realize different delivered values
  because of hydraulic and thermal constraints.

Related Documentation
---------------------

For the conceptual controller overview and workflow placement, see
:doc:`controller`.

For network-level interpretation of how controller setpoints are realized, see
:doc:`../network/network_main`.

For storage and heat-pump asset physics that constrain effective behavior, see
:doc:`../physics/ideal_heat_storage_physics` and
:doc:`../physics/heat_pump_physics`.

For implementation-oriented controller reference, see
:doc:`../reference/controller_reference`.

- :doc:`controller` for the conceptual control overview.
- :doc:`../physics/ideal_heat_storage_physics` for ideal heat-storage internal clipping behavior.
- :doc:`../physics/ates_cluster_physics` for ATES storage behavior.
- :doc:`../physics/producer_physics` for producer asset physical response.
- :doc:`../physics/consumer_physics` for consumer asset physical response.
- :doc:`../physics/heat_pump_physics` for water-to-water heat-pump internal behavior.
- :doc:`../network/network_main` for network solve interpretation.
- :doc:`../reference/controller_reference` for class-level reference.
