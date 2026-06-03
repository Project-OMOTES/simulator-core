DemandCluster
=============

Description
-----------

The ``DemandCluster`` asset models a controllable heat demand unit within a thermal network.
The asset may represent different types of heat consumers, because the simulation treats it as a
controllable thermal boundary that extracts heat from the network.
The asset demands heat according to controller-provided setpoints for inlet temperature, outlet
temperature, and heat demand.
The asset is mapped from ESDL (Energy System Description Language) objects and receives
controller-set values during simulation.


Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 40 20 30

   * - Parameter
     - Description
     - Unit
     - ESDL Asset Property
   * - ``temperature_in``
     - Inlet temperature (initial value from ESDL carrier)
     - K
     - not mapped from ESDL; set by controller
   * - ``temperature_out``
     - Outlet temperature (initial value from ESDL carrier)
     - K
     - not mapped from ESDL; set by controller
   * - ``temperature_out_target``
     - Outlet temperature target
     - K
     - not mapped from ESDL; set by controller
   * - ``mass_flowrate``
     - Mass flow rate
     - kg/s
     - not mapped from ESDL; set by controller
   * - ``thermal_power_allocation``
     - Heat demand set point
     - W
     - not mapped from ESDL; set by controller
   * - ``max_power``
     - Maximum power (control limit)
     - W
     - ``power`` property of ESDL asset


Controlled Parameters
~~~~~~~~~~~~~~~~~~~~~

The controller (see :class:`ControllerConsumer`) supplies a setpoints dictionary containing:

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

The heat demand of the consumer is in principle determined by the profile on *connection point 1* (outlet). 
This profile defines the heat demand as a function of time. Interpolation is used to determine the heat 
demand at each simulation timestep. 

The controller can override this profile value when it surpasses the maximum power limit of the asset, 
or when there is insufficient heat supply in the network to meet the demand. See
:doc:`../controller/controller` for more details on how the controller allocates heat supply to meet demand across the network.

.. [#heat-demand-set-point] The heat demand set point defines the mass flow required to meet the
  heat demand, given the inlet and outlet temperatures. The mass flow is calculated as:
  :math:`\dot{m} = Q_{set}/\left(c_p (T_{out} - T_{in})\right)` where :math:`c_p` is the
  specific heat capacity of the fluid, which is determined based on the average of the inlet and outlet temperature.


Additional simulation outputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default per-port outputs for mass flow, pressure, temperature, and volume flow,
the consumer asset provides the following additional outputs:

.. list-table::
   :header-rows: 1
   :widths: 20 50 10

   * - Signal
     - Description
     - Unit
   * - ``heat_demand_set_point``
     - Heat demand set point
     - W
   * - ``heat_demand``
     - Actual heat demanded [#heat-demanded]_
     - W

.. [#heat-demanded] The actual heat demanded is calculated as :math:`Q_{demanded} = \left( U_1 - U_0 \right) \dot{m}_1`,
  where :math:`U_1` and :math:`U_0` are the internal energies at the outlet and inlet, respectively, and :math:`\dot{m}_1` is the mass flow rate at the outlet.

Physics and Assumptions
-----------------------

The consumer acts as a controllable heat sink. It prescribes a mass flow that extracts the
requested heat from the network at the specified inlet and outlet temperatures. The inlet
temperature is taken from the network solution after the first timestep, while the outlet
temperature remains controller-defined.

Mass flow
~~~~~~~~~

The asset prescribes the mass flow required to meet the heat demand set point, given the inlet and
outlet temperatures:

.. math::

  \dot{m} = \frac{Q_{set}}{c_p (T_{out} - T_{in})}


.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - :math:`\dot{m}`
     - Mass flow rate [kg/s]
   * - :math:`Q_{set}`
     - Heat demand set point [W]
   * - :math:`c_p`
     - Specific heat capacity of the fluid [J/(kg·K)] [#specific-heat-capacity]_
   * - :math:`T_{out}`
     - Outlet temperature [K] [#outlet-temperature]_
   * - :math:`T_{in}`
     - Inlet temperature [K] [#inlet-temperature]_

.. [#specific-heat-capacity] The specific heat capacity (:math:`c_p`) is determined based on the average of the inlet and outlet temperature.
.. [#outlet-temperature] The outlet temperature is set by the controller, and is used to determine the heat demand set point.
.. [#inlet-temperature] The inlet temperature is determined by the network hydraulics and only set by the controller for the first time step.

Pressure
~~~~~~~~

The consumer does not model internal pressure losses.
Supply and return pressures are determined by the network hydraulics.

Internal energy
~~~~~~~~~~~~~~~

The actual heat absorbed by the consumer is evaluated from the internal-energy difference across
the asset and the solved mass flow:

.. math::

  Q_{demanded} = \left( U_1 - U_0 \right) \dot{m}_0

where:

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - :math:`U_0`
     - Internal energy at inlet [J/kg]
   * - :math:`U_1`
     - Internal energy at outlet [J/kg]
   * - :math:`\dot{m}_0`
     - Mass flow rate at inlet [kg/s]

This relation is used for reporting and convergence checking. The asset itself does not include
internal heat losses or thermal storage.

Assumptions
-----------

- The asset responds instantaneously (e.g., within the simulation timestep) to setpoints — no dynamic effects are modelled.
- Negative mass flow values are physically disallowed and will raise errors.
- Heat losses, pressure losses, and transient effects inside the control volume are not accounted for.


Limitations
-----------

- No modelling of part-load efficiency or startup/shutdown dynamics.
- No explicit modelling of heat losses or environmental interactions.
- Convergence is checked against a 0.1% tolerance between supplied and demanded heat.

See Also
--------

- :doc:`producer_physics` — Complementary heat production asset model
- :doc:`heat_exchanger_physics` — Multi-circuit heat transfer
- :doc:`ideal_heat_storage_physics` — Heat storage for supply smoothing

References
----------

.. rubric:: References

*(No references listed.)*