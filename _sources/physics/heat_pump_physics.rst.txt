Heat Pump
=========

Description
-----------

The ``HeatPump`` asset models a four-port water-to-water heat pump that extracts heat from a
primary circuit and delivers it to a secondary circuit. In the thermal network, the primary side
acts as a heat sink and the secondary side acts as a heat source. The asset therefore couples two
hydraulic circuits through an energy balance, while electrical power provides the difference between
heat extracted on the primary side and heat delivered on the secondary side.

The asset is mapped from ESDL ``HeatPump`` objects. The coefficient of performance is read from the
ESDL ``COP`` property, and an optional electrical power limit is read from the ESDL ``power``
property. During simulation, the controller provides temperatures and heat-demand setpoints for both
sides of the asset.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 40 20 30

   * - Parameter
     - Description
     - Unit
     - ESDL Asset Property
   * - ``coefficient_of_performance``
     - Ratio of delivered secondary heat to electrical input power
     - -
     - ``COP``
   * - ``maximum_electrical_power``
     - Upper bound on electrical input power, if configured
     - W
     - ``power``
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

The controller provides setpoints for both hydraulic sides of the heat pump:

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
     - Flag that determines whether the secondary side is pressure-controlled or mass-flow-controlled
     - -

The secondary-side setpoints are applied first. If a maximum electrical power is configured, the
requested secondary heat output can be capped before the corresponding primary-side heat extraction
is determined.

Additional simulation outputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default per-port outputs for mass flow, pressure, temperature, and volume flow,
the heat pump asset provides the following additional outputs:

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - Signal
     - Description
     - Unit
   * - ``heat_power_primary``
     - Heat power on the primary side [#heat-power-primary]_
     - W
   * - ``heat_power_secondary``
     - Heat power on the secondary side [#heat-power-secondary]_
     - W
   * - ``electricity_consumption``
     - Electrical input power [#electric-power]_
     - W

.. [#heat-power-primary] The primary-side heat power is calculated from the solved primary mass flow
  and the internal-energy difference between primary outlet and inlet.

.. [#heat-power-secondary] The secondary-side heat power is calculated from the solved secondary mass
  flow and the internal-energy difference between secondary outlet and inlet.

.. [#electric-power] Electrical input power is reported as the absolute difference between the
  absolute primary-side and secondary-side heat powers.

Physics and Assumptions
-----------------------

The heat pump couples a cold primary side to a hot secondary side through an energy-transfer model.
The secondary side represents the useful heat delivered to the network. The primary side represents
heat extracted from a source circuit. Electricity supplies the remaining energy needed to raise heat
from the primary temperature level to the secondary temperature level.

COP-based coupling
~~~~~~~~~~~~~~~~~~

The model uses the coefficient of performance, :math:`COP`, to define the ratio between extracted
primary heat and delivered secondary heat:

.. math::

   Q_{hot} = Q_{cold} + W_{el}

.. math::

   COP = \frac{Q_{hot}}{W_{el}}

Combining these relations gives:

.. math::

   \frac{Q_{cold}}{Q_{hot}} = 1 - \frac{1}{COP}

The solver uses the ratio
:math:`c = Q_{cold}/Q_{hot} = 1 - 1/COP`
as the heat-transfer coefficient between the primary and secondary sides.

where:

.. list-table::
   :widths: 25 75
   :stub-columns: 1

   * - :math:`Q_{hot}`
     - Heat delivered on the secondary side [W]
   * - :math:`Q_{cold}`
     - Heat extracted on the primary side [W]
   * - :math:`W_{el}`
     - Electrical input power [W]
   * - :math:`COP`
     - Coefficient of performance [-]

Mass flow
~~~~~~~~~

For each side, the requested heat transfer is translated into a mass flow using the prescribed inlet
and outlet temperatures:

.. math::

   \dot{m} = \frac{Q}{c_p (T_{out} - T_{in})}

where:

.. list-table::
   :widths: 25 75
   :stub-columns: 1

   * - :math:`\dot{m}`
     - Mass flow rate [kg/s]
   * - :math:`Q`
     - Requested heat transfer on the selected side [W]
   * - :math:`c_p`
     - Specific heat capacity at the mean fluid temperature [J/(kg K)]
   * - :math:`T_{in}`
     - Inlet temperature on the selected side [K]
   * - :math:`T_{out}`
     - Outlet temperature on the selected side [K]

On the primary side, the resulting mass flow is used to initialize the heat-transfer balance. On the
secondary side, the asset either prescribes mass flow directly or prescribes pressure, depending on
``set_pressure``.

Electrical power cap
~~~~~~~~~~~~~~~~~~~~

If ``maximum_electrical_power`` is configured, the requested secondary heat output is limited so that

.. math::

   |W_{el}| \leq W_{el,max}

which implies

.. math::

   |Q_{hot}| \leq COP W_{el,max}

When this cap is active, the secondary heat-demand request is reduced before the corresponding
primary-side demand is derived.

Heat powers and electricity consumption
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After solving, the reported heat powers are evaluated from mass flow and internal-energy difference
on each side:

.. math::

   Q_{primary} = \dot{m}_{primary} (u_{out,primary} - u_{in,primary})

.. math::

   Q_{secondary} = \dot{m}_{secondary} (u_{out,secondary} - u_{in,secondary})

The electrical input power is then reported as:

.. math::

   W_{el} = \left| |Q_{primary}| - |Q_{secondary}| \right|

These outputs are useful for checking whether the simulated heat pump is operating near its intended
COP and electrical-power limit.

Assumptions
-----------

- The heat pump is represented as a steady-state coupling between a primary and secondary circuit.
- The coefficient of performance is constant during a timestep.
- Prescribed inlet and outlet temperatures are used directly; no internal refrigerant cycle is modeled.
- Dynamic compressor behavior, cycling, and start-up effects are not modeled.
- The secondary side can be operated either with prescribed mass flow or prescribed pressure.
- Fluid properties are represented through temperature-dependent water properties used elsewhere in the simulator.

Limitations
-----------

- No explicit refrigerant thermodynamics, compressor map, or part-load efficiency curve.
- No defrost behavior, auxiliary electric heater, or minimum on/off time logic.
- No explicit thermal losses to the surroundings.
- The COP does not vary with source temperature, sink temperature, or operating point within the asset model.
- The documentation describes the four-port ``HeatPump`` asset; the separate two-port ``AirToWaterHeatPump`` asset follows different behavior and should be documented separately.

See Also
--------

- :doc:`heat_exchanger_physics` — Related four-port heat transfer asset (passive coupling)
- :doc:`air_to_water_heat_pump_physics` — Two-port heat pump variant
- :doc:`producer_physics` — Simple heat source model

References
----------

.. rubric:: References

*(No references listed.)*
