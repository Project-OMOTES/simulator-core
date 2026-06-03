Air To Water Heat Pump
======================

Description
-----------

The ``AirToWaterHeatPump`` asset models a two-port heat producer that delivers heat to the water
network by consuming electricity. In the thermal network, it behaves as a controllable producer on
one hydraulic circuit, unlike the four-port ``HeatPump`` asset that couples two water circuits.

The asset is mapped from ESDL ``HeatPump`` objects with two ports. The coefficient of performance
(COP) is mapped from ESDL and is used to convert delivered thermal power into electrical power
consumption. During simulation, the controller provides temperature, heat-demand, and pressure or
mass-flow control setpoints.

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
     - Ratio of thermal heat supplied to electrical power input
     - -
     - ``COP``
   * - ``pressure_supply``
     - Supply pressure setpoint used in pressure-controlled mode
     - Pa
     - controller-set
   * - ``temperature_in``
     - Inlet temperature
     - K
     - controller-set
   * - ``temperature_out``
     - Outlet temperature
     - K
     - controller-set
   * - ``heat_demand_set_point``
     - Thermal heat supply setpoint
     - W
     - controller-set

Controlled Parameters
~~~~~~~~~~~~~~~~~~~~~

The controller supplies producer-style setpoints for the two-port heat pump:

.. list-table::
   :header-rows: 1
   :widths: 20 50 10

   * - Signal
     - Description
     - Unit
   * - :math:`T_{in}`
     - Inlet temperature (connection point 0)
     - K
   * - :math:`T_{out}`
     - Outlet temperature (connection point 1)
     - K
   * - :math:`Q_{set}`
     - Requested heat supply to the network
     - W
   * - ``set_pressure``
     - If true, pressure is prescribed. If false, mass flow is prescribed to satisfy the heat setpoint.
     - -

Additional simulation outputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default per-port outputs for mass flow, pressure, temperature, and volume flow,
the air-to-water heat pump provides:

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - Signal
     - Description
     - Unit
   * - ``heat_supply_set_point``
     - Heat supply setpoint requested by the controller
     - W
   * - ``heat_supplied``
     - Actual heat supplied to the water network
     - W
   * - ``electricity_consumption``
     - Electrical power consumption derived from supplied heat and COP
     - W

Physics and Assumptions
-----------------------

The asset sets temperatures and either pressure or mass flow as producer boundary conditions. The
primary physical relation is the heat-demand-to-mass-flow conversion on the water side, followed by
calculation of actual supplied heat from solved mass flow and internal-energy difference.

Mass flow
~~~~~~~~~

When operating in mass-flow-controlled mode, the required mass flow is computed from the requested
heat supply and prescribed inlet and outlet temperatures:

.. math::

  \dot{m} = \frac{Q_{set}}{c_p (T_{out} - T_{in})}

where:

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - :math:`\dot{m}`
     - Mass flow rate [kg/s]
   * - :math:`Q_{set}`
     - Heat supply setpoint [W]
   * - :math:`c_p`
     - Specific heat capacity at the mean fluid temperature [J/(kg K)]
   * - :math:`T_{in}`
     - Inlet temperature [K]
   * - :math:`T_{out}`
     - Outlet temperature [K]

Heat supplied
~~~~~~~~~~~~~

The actual supplied heat is evaluated from solved internal energy and mass flow:

.. math::

  Q_{supplied} = (U_1 - U_0) \dot{m}_1

where:

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - :math:`U_0`
     - Internal energy at inlet [J/kg]
   * - :math:`U_1`
     - Internal energy at outlet [J/kg]
   * - :math:`\dot{m}_1`
     - Outlet mass flow rate [kg/s]

Electricity consumption
~~~~~~~~~~~~~~~~~~~~~~~

Electrical power consumption is computed from delivered heat and COP:

.. math::

  P_{el} = \frac{|Q_{supplied}|}{COP}

This relation provides a direct interpretation of the reported electricity usage for a given thermal
output.

Assumptions
-----------

- The asset is modeled as a steady-state producer boundary on the water network.
- COP is constant during a timestep.
- Internal compressor and refrigerant-cycle dynamics are not modeled.
- Internal pressure losses and thermal losses inside the asset are neglected.
- The response to controller setpoints is instantaneous within the timestep.

Limitations
-----------

- No part-load COP curve or temperature-dependent COP model.
- No startup, shutdown, minimum runtime, or defrost behavior.
- No explicit maximum electrical power cap in this two-port implementation.
- This page documents only the two-port ``AirToWaterHeatPump``; the four-port ``HeatPump`` has different physics and controls.

See Also
--------

- :doc:`heat_pump_physics` — Four-port heat pump with coupled primary and secondary circuits
- :doc:`producer_physics` — Simpler heat production model
- :doc:`consumer_physics` — Heat demand boundary

References
----------

.. rubric:: References

*(No references listed.)*
