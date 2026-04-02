ProductionCluster
=================

Description
-----------

The ``ProductionCluster`` asset models a controllable heat production unit within a thermal network.
The asset may represent different types of heat producers, because the simulation treats it as a
controllable thermal boundary that injects heat into the network.
The asset supplies heat according to controller-provided setpoints for inlet temperature, outlet
temperature, heat demand, and operating mode.
The asset is mapped from ESDL (Energy System Description Language) objects and receives
controller-set values during simulation.


Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Unit
     - ESDL Asset Property
   * - ``pressure_supply``
     - Supply pressure used when the asset operates in pressure-controlled mode
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
   * - ``control_mass_flow``
     - Boolean flag indicating whether the asset prescribes mass flow instead of pressure
     - -
     - controller-set
   * - ``controlled_mass_flow``
     - Mass flow prescribed in mass-flow-controlled mode
     - kg/s
     - controller-set
   * - ``thermal_production_required``
     - Requested thermal production derived from the controller heat-demand setpoint
     - W
     - controller-set
   * - ``heat_demand_set_point``
     - Heat supply target used to determine the required operating point
     - W
     - controller-set

Controlled Parameters
~~~~~~~~~~~~~~~~~~~~~

The controller supplies a setpoints dictionary containing:

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
     - Heat demand [#heat-demand-set-point]_
     - W
   * - ``set_pressure``
     - Pressure-control flag [#pressure-flag]_
     - -


.. [#pressure-flag] The pressure flag determines whether the producer fixes pressure or prescribes
  mass flow. If the flag is true, the supply pressure is fixed at ``pressure_supply`` and mass flow
  follows from the network hydraulics. If the flag is false, the asset prescribes the mass flow
  required to meet the requested heat demand.

.. [#heat-demand-set-point] The heat demand set point defines the mass flow required to meet the
  heat demand, given the inlet and outlet temperatures. The mass flow is calculated as:
  :math:`\dot{m} = Q_{set}/\left(c_p (T_{out} - T_{in})\right)` where :math:`c_p` is the
  specific heat capacity of the fluid, which is determined based on the average of the inlet and outlet temperature.


Additional simulation outputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default per-port outputs for mass flow, pressure, temperature, and volume flow,
the producer asset provides the following additional outputs:

.. list-table::
   :header-rows: 1
   :widths: 20 50 10

   * - Signal
     - Description
     - Unit
   * - ``heat_supply_set_point``
     - Heat supply set point
     - W
   * - ``heat_supplied``
     - Actual heat supplied [#heat-supplied]_
     - W

.. [#heat-supplied] The actual heat supplied is calculated as :math:`Q_{supplied} = \left( U_1 - U_0 \right) \dot{m}_1`, 
  where :math:`U_1` and :math:`U_0` are the internal energies at the outlet and inlet, respectively, and :math:`\dot{m}_1` is the mass flow rate at the outlet.

Physics and Assumptions
-----------------------

The producer acts as a controllable heat boundary. In mass-flow-controlled operation, it computes
the mass flow required to deliver the requested heat at the specified inlet and outlet
temperatures. In pressure-controlled operation, it fixes the supply pressure and lets the network
hydraulics determine the resulting flow.

Mass flow
~~~~~~~~~

When the producer is operated in mass-flow-controlled mode, the required mass flow rate is:

.. math::

  \dot{m} = \frac{Q_{set}}{c_p (T_{out} - T_{in})}

where:

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - :math:`\dot{m}`
     - Mass flow rate [kg/s]
   * - :math:`Q_{set}`
     - Heat demand set point [W]
   * - :math:`c_p`
     - Specific heat capacity of the fluid [J/(kg·K)]
   * - :math:`T_{out}`,\ :math:`T_{in}`
     - Outlet and inlet temperatures [K]

The specific heat capacity (:math:`c_p`) is determined based on the average of the inlet and outlet temperature.

Pressure
~~~~~~~~

The producer does not model internal pressure losses. When pressure control is enabled, the supply
pressure is prescribed and the resulting mass flow follows from the network solution. When pressure
control is disabled, the asset prescribes mass flow directly to meet the requested heat output.


Operating Modes
~~~~~~~~~~~~~~~

The asset supports two operating modes:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Mode
     - Description
   * - **Mass flow controlled**
     - Mass flow is set directly to achieve the required heat demand.
   * - **Pressure controlled**
     - Supply pressure is fixed; mass flow is determined by network hydraulics.

The actual heat supplied is evaluated from the solved internal-energy difference and outlet mass
flow:

.. math::

  Q_{supplied} = \left( U_1 - U_0 \right) \dot{m}_1

where:

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - :math:`U_0`
     - Internal energy at inlet [J/kg]
   * - :math:`U_1`  
     - Internal energy at outlet [J/kg]
   * - :math:`\dot{m}_1`
     - Mass flow rate at outlet [kg/s]

The internal energy at each port is derived from fluid temperature with a reference internal energy
defined at 0 °C.

Assumptions
-----------

- The asset responds instantaneously (e.g., within the simulation timestep) to setpoints — no dynamic effects are modelled.
- Negative mass flow values are physically disallowed and will raise errors.
- Heat losses, pressure losses, and transient effects are not accounted for.

Limitations
-----------

- No modelling of part-load efficiency or startup/shutdown dynamics.
- No explicit modelling of heat losses or environmental interactions.
- Convergence is checked against a 0.1% tolerance between supplied and demanded heat.

References
----------

.. rubric:: References

*(No references listed.)*