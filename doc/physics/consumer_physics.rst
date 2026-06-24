DemandCluster
=============

Description
-----------

The ``DemandCluster`` asset models a controllable heat demand unit within a thermal network.
The asset may represent different types of heat consumers, because the simulation treats it as a
controllable thermal boundary that extracts heat from the network.
The asset removes heat from the circulating fluid according to time-varying temperature and heat
setpoints. In practice, it represents the thermal behavior that a controller or supervisory input
requests from a consumer, while the network solution determines whether that request can be met.


Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 40 20 30

   * - Parameter
     - Description
     - Unit
     - ESDL Asset Property
   * - ``max_power``
     - Maximum heat demand that can be allocated to the consumer
     - W
     - ``power`` property of ESDL asset


Controlled Parameters
~~~~~~~~~~~~~~~~~~~~~

The consumer receives the following user-relevant control signals:

.. list-table::
   :header-rows: 1
   :widths: 20 50 10

   * - Signal
     - Description
     - Unit
   * - :math:`T_{in}`
     - Inlet temperature used to initialize the first timestep; afterwards the inlet temperature
       is solved by the network and used to interpret the heat demand
     - K
   * - :math:`T_{out}`
     - Target outlet temperature at the consumer return side
     - K
   * - :math:`Q_{set}`
     - Requested heat demand
     - W

The requested heat demand is typically derived from a time series or supervisory control action.
It can be curtailed by the configured maximum power or by limited upstream heat supply. For how
the controller coordinates demand with available production and storage, see
:doc:`../controller/controller`.


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
     - Requested heat demand written to the simulation output
     - W
   * - ``heat_demand``
     - Actual heat extracted from the network fluid
     - W

The reported heat demand is evaluated as:

.. math::

  Q_{demanded} = \left(u_1 - u_0\right) \dot{m}_0

where port 0 is the inlet and port 1 is the outlet. For a consuming asset, the outlet fluid has
lower specific internal energy than the inlet fluid and the solved inlet mass flow is typically
negative, so the reported heat demand is positive when the consumer removes heat from the network.

Physics and Assumptions
-----------------------

The consumer acts as a controllable heat sink. It prescribes a mass flow that extracts the
requested heat from the network at the specified inlet and outlet temperatures. The inlet
temperature is taken from the network solution after the first timestep, while the outlet
temperature remains control-defined.

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
     - Specific heat capacity of the fluid [J/(kg K)] [#specific-heat-capacity]_
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

Heat reporting
~~~~~~~~~~~~~~

The actual heat absorbed by the consumer is evaluated from the internal-energy difference across
the asset and the solved inlet mass flow:

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

This relation is used for reporting and convergence checking. For a consumer, :math:`U_1 < U_0`
and :math:`\dot{m}_0 < 0` in the usual operating direction, so :math:`Q_{demanded}` is positive
when heat is extracted from the network fluid. The asset itself does not include internal heat
losses or thermal storage.

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

- :doc:`../controller/controller` -- Control behavior that allocates demand across the network
- :doc:`../network/network_main` -- Network equations that determine available flow and inlet state
- :doc:`producer_physics` — Complementary heat production asset model

References
----------

.. rubric:: References

*(No references listed.)*