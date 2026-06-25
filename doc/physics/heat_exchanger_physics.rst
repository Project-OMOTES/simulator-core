Heat Exchanger
==============

Description
-----------

The ``HeatExchanger`` asset models a four-port water-to-water heat exchanger that transfers heat
from a primary circuit to a secondary circuit. In the thermal network, the primary side acts as
the side that releases heat and the secondary side acts as the side that receives heat. The asset
therefore couples two hydraulic circuits without mixing their water streams.

The asset is mapped from ESDL ``HeatExchange`` objects. The ESDL ``Efficiency`` property is used
to represent how much of the requested primary-side heat transfer appears on the secondary side.
During simulation, the controller provides temperature and heat-demand setpoints for both sides,
plus a signal that selects the hydraulic boundary condition on the secondary side.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 40 20 30

   * - Parameter
     - Description
     - Unit
     - ESDL Asset Property
   * - ``heat_transfer_efficiency``
     - Fraction of requested primary-side heat transfer that is delivered to the secondary side
     - -
     - ``Efficiency``
   * - ``temperature_in_primary``
     - Primary-side inlet temperature
     - K
     - not mapped from ESDL; set by controller
   * - ``temperature_out_primary``
     - Primary-side outlet temperature
     - K
     - not mapped from ESDL; set by controller
   * - ``temperature_in_secondary``
     - Secondary-side inlet temperature
     - K
     - not mapped from ESDL; set by controller
   * - ``temperature_out_secondary``
     - Secondary-side outlet temperature
     - K
     - not mapped from ESDL; set by controller

Controlled Parameters
~~~~~~~~~~~~~~~~~~~~~

The controller provides setpoints for both hydraulic sides of the heat exchanger:

.. list-table::
   :header-rows: 1
   :widths: 28 52 10

   * - Signal
     - Description
     - Unit
   * - ``primary_temperature_in``
     - Primary-side inlet temperature
     - K
   * - ``primary_temperature_out``
     - Primary-side outlet temperature
     - K
   * - ``primary_heat_demand``
     - Requested heat extraction on the primary side
     - W
   * - ``secondary_temperature_in``
     - Secondary-side inlet temperature
     - K
   * - ``secondary_temperature_out``
     - Secondary-side outlet temperature
     - K
   * - ``secondary_heat_demand``
     - Requested heat delivery on the secondary side
     - W
   * - ``set_pressure``
     - Selects whether the secondary side is operated through a prescribed pressure or a prescribed mass flow
     - -

The primary and secondary setpoints should be physically consistent. In particular, the requested
secondary heat transfer should not exceed what the configured heat-transfer efficiency allows.

Additional simulation outputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default per-port outputs for mass flow, pressure, temperature, and volume flow,
the heat exchanger asset provides the following additional outputs:

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - Signal
     - Description
     - Unit
   * - ``heat_power_primary``
     - Heat power transferred from the primary side
     - W
   * - ``heat_power_secondary``
     - Heat power delivered on the secondary side
     - W
   * - ``heat_loss``
     - Difference between reported primary-side and secondary-side heat power
     - W

Physics and Assumptions
-----------------------

The heat exchanger transfers energy between two water circuits while keeping the circuits
hydraulically separated. In simulation, the primary side represents the circuit that gives up heat.
The secondary side represents the circuit that receives that heat. The model is steady-state within
each timestep and uses prescribed inlet and outlet temperatures to translate requested heat transfer
into mass flow and reported heat powers.

Heat transfer efficiency
~~~~~~~~~~~~~~~~~~~~~~~~

The configured heat-transfer efficiency, :math:`\eta`, relates the requested heat transfer on both
sides:

.. math::

   Q_{secondary,set} = - \eta Q_{primary,set}

where:

.. list-table::
   :widths: 30 70
   :stub-columns: 1

   * - :math:`Q_{primary,set}`
     - Requested heat transfer on the primary side [W]
   * - :math:`Q_{secondary,set}`
     - Requested heat transfer on the secondary side [W]
   * - :math:`\eta`
     - Heat-transfer efficiency [-]

The negative sign reflects that heat leaving one side appears on the other side with the opposite
sign. For :math:`\eta = 1`, the asset behaves as an ideal exchanger with equal heat-transfer
magnitudes on both sides. For :math:`\eta < 1`, less heat is delivered to the secondary side than
is removed from the primary side.

Mass flow
~~~~~~~~~

For each side, the requested heat transfer is translated into a mass flow using the prescribed
inlet and outlet temperatures:

.. math::

   \dot{m} = \frac{Q}{c_p (T_{out} - T_{in})}

where:

.. list-table::
   :widths: 25 75
   :stub-columns: 1

   * - :math:`\dot{m}`
     - Mass flow rate on the selected side [kg/s]
   * - :math:`Q`
     - Requested heat transfer on the selected side [W]
   * - :math:`c_p`
     - Specific heat capacity at the mean fluid temperature [J/(kg K)]
   * - :math:`T_{in}`
     - Inlet temperature on the selected side [K]
   * - :math:`T_{out}`
     - Outlet temperature on the selected side [K]

On the primary side, this relation defines the mass flow needed to extract the requested amount of
heat. On the secondary side, the same relation defines the mass flow for heat delivery when the
asset is operated in mass-flow-controlled mode.

Heat powers and losses
~~~~~~~~~~~~~~~~~~~~~~

After solving the network, the reported heat powers are evaluated from solved mass flow and the
internal-energy difference across each side:

.. math::

   Q_{primary} = \dot{m}_{primary} (u_{out,primary} - u_{in,primary})

.. math::

   Q_{secondary} = \dot{m}_{secondary} (u_{out,secondary} - u_{in,secondary})

The reported heat loss is then:

.. math::

   Q_{loss} = Q_{primary} - Q_{secondary}

where:

.. list-table::
   :widths: 25 75
   :stub-columns: 1

   * - :math:`u_{in}` and :math:`u_{out}`
     - Inlet and outlet specific internal energy on the selected side [J/kg]
   * - :math:`Q_{loss}`
     - Reported difference between primary-side and secondary-side heat power [W]

These outputs help users check whether the exchanger is transferring nearly all primary-side heat to
the secondary side or whether a significant difference remains.

Operating modes and sign convention
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The asset can operate with either a prescribed pressure or a prescribed mass flow on the secondary
side. In mass-flow-controlled operation, the secondary-side flow is chosen to match the requested
heat transfer and temperature lift. In pressure-controlled operation, the network hydraulics
determine the resulting secondary-side flow.

Heat transfer on the two sides uses opposite signs. A heat flow reported as leaving the primary
side corresponds to heat entering the secondary side. When interpreting results, compare the
magnitudes of ``heat_power_primary`` and ``heat_power_secondary`` together with ``heat_loss``.

Assumptions
-----------

- The asset is modeled as a steady-state heat transfer element within each timestep.
- The primary and secondary water circuits are hydraulically separated and do not mix.
- The heat-transfer efficiency is constant during a timestep.
- Prescribed inlet and outlet temperatures are applied directly.
- Internal thermal capacity of the exchanger metal and contained fluid is neglected.
- Internal pressure losses inside the exchanger are neglected in the asset model.

Limitations
-----------

- No explicit heat-exchanger geometry, heat-transfer area, or approach-temperature model.
- No temperature-dependent efficiency, fouling, or performance degradation.
- No transient warm-up, cooldown, or thermal storage effects.
- No explicit leakage, bypass flow, or cross-contamination between circuits.
- If exchanger pressure drop is important for the study, a more detailed asset model is needed.

See Also
--------

- :doc:`heat_pump_physics` — Related four-port asset with active heat input
- :doc:`producer_physics` — Simple heat production
- :doc:`consumer_physics` — Heat demand endpoint

References
----------

.. rubric:: References

*(No references listed.)*
