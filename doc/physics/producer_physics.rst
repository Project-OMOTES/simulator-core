ProductionCluster
=================

Description
-----------

The ``ProductionCluster`` asset models a controllable heat production unit within a thermal network.
The asset may represent different types of heat producers, because the simulation treats it as a
controllable thermal boundary that injects heat into the network.
The asset adds heat to the circulating fluid according to time-varying temperature, production,
and operating-mode setpoints. It is intended as a generic controllable heat source whose actual
delivery depends on both the requested operating mode and the solved network state.


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
     - user-configured operating parameter

Controlled Parameters
~~~~~~~~~~~~~~~~~~~~~

The producer receives the following user-relevant control signals:

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
     - Requested heat production
     - W
   * - ``pressure-controlled mode``
     - If enabled, the producer fixes supply pressure. If disabled, it prescribes mass flow to
       target the requested heat production.
     - -

The controller chooses between the two operating modes each timestep. For the broader control
strategy that coordinates production with demand and storage, see
:doc:`../controller/controller`.


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
     - Requested heat production written to the simulation output
     - W
   * - ``heat_supplied``
     - Actual heat added to the network fluid
     - W

The reported heat supply is evaluated as:

.. math::

  Q_{supplied} = \left(u_1 - u_0\right) \dot{m}_1

where port 0 is the inlet and port 1 is the outlet. In the usual operating direction,
:math:`u_1 > u_0` and :math:`\dot{m}_1 > 0`, so the reported heat supply is positive when the
producer injects heat into the network.

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
     - Requested heat production [W]
   * - :math:`c_p`
     - Specific heat capacity of the fluid [J/(kg K)]
   * - :math:`T_{out}`,\ :math:`T_{in}`
     - Outlet and inlet temperatures [K]

The specific heat capacity (:math:`c_p`) is determined based on the average of the inlet and outlet temperature.

Pressure
~~~~~~~~

The producer does not model internal pressure losses. When pressure control is enabled, the supply
pressure is prescribed and the resulting mass flow follows from the network solution. When pressure
control is disabled, the asset prescribes mass flow directly to target the requested heat
production.

.. note:: The current default value for the supply pressure is 10 bar, with a pressure drop of (:math:`\Delta p`) of 5 bar over the asset.


Operating Modes
~~~~~~~~~~~~~~~

The asset supports two operating modes:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Mode
     - Description
   * - **Mass flow controlled**
     - Mass flow is set directly to target the requested heat production.
   * - **Pressure controlled**
     - Supply pressure is fixed; mass flow and delivered heat follow from the solved network
       hydraulics.

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

See Also
--------

- :doc:`../controller/controller` -- Control behavior that selects production mode and targets
- :doc:`../network/network_main` -- Network equations that determine pressure-driven operation
- :doc:`consumer_physics` — Complementary heat demand asset model
- :doc:`ideal_heat_storage_physics` — Heat buffering for supply stability

References
----------

.. rubric:: References

*(No references listed.)*