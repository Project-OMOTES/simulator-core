Ideal Heat Storage
==================

Description
-----------

The ``IdealHeatStorage`` asset represents a two-layer hot-water buffer that can either absorb heat
(charging) or release heat (discharging) in a thermal network. The storage exchanges heat with the
network through one inlet and one outlet and tracks the amount of hot volume in the vessel via a
fill level between 0 and 1.

In simulation, the asset behaves as an idealized control volume with stratified hot and cold zones.
The controller provides a thermal power setpoint, and the asset translates that setpoint into mass
flow and port temperatures based on the current operating mode. The asset is mapped from ESDL
``HeatStorage`` and receives controller-driven setpoints during simulation.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 40 20 30

   * - Parameter
     - Description
     - Unit
     - ESDL Asset Property
   * - ``volume``
     - Maximum storage volume
     - m3
     - ``volume``
   * - ``fill_level``
     - Initial hot-volume fraction (0 to 1)
     - -
     - ``fillLevel``
   * - ``temperature_in``
     - Initial hot-side temperature (connection point 0)
     - K
     - from ESDL carrier temperature at In/Supply port
   * - ``temperature_out``
     - Initial cold-side temperature (connection point 1)
     - K
     - from ESDL carrier temperature at Out/Return port
   * - ``max_charge_power``
     - Maximum charging power enforced by controller
     - W
     - ``maxChargeRate``
   * - ``max_discharge_power``
     - Maximum discharging power enforced by controller
     - W
     - ``maxDischargeRate``
   * - ``effective_max_charge_power``
     - Effective charging limit used by the controller, derived from remaining volume,
       timestep, temperature difference, and ``max_charge_power``
     - W
     - derived in controller (not directly mapped)
   * - ``effective_max_discharge_power``
     - Effective discharging limit used by the controller, derived from available hot volume,
       timestep, temperature difference, and ``max_discharge_power``
     - W
     - derived in controller (not directly mapped)
   * - ``buffer_temperature_hot``
     - Hot-zone buffer temperature state used for storage state updates
     - K
     - state variable (not directly mapped)
   * - ``buffer_temperature_cold``
     - Cold-zone buffer temperature state used for storage state updates
     - K
     - state variable (not directly mapped)

Controlled Parameters
~~~~~~~~~~~~~~~~~~~~~

The storage receives one user-relevant control signal from the controller:

.. list-table::
   :header-rows: 1
   :widths: 20 60 10

   * - Signal
     - Description
     - Unit
   * - :math:`Q_{set}`
     - Thermal power setpoint for storage operation. Positive values charge the storage and
       negative values discharge the storage.
     - W

The controller typically clips :math:`Q_{set}` to feasible charging or discharging power based on
state of charge, volume, timestep, and configured power limits.

Additional simulation outputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default per-port outputs for mass flow, pressure, temperature, and volume flow,
the storage asset provides:

.. list-table::
   :header-rows: 1
   :widths: 20 60 10

   * - Signal
     - Description
     - Unit
   * - ``fill_level``
     - Updated fraction of hot volume in the storage after each timestep
     - -

Physics and Assumptions
-----------------------

The Ideal Heat Storage is modeled with three operating modes: charging, discharging, and idle.
The mode is determined by the sign of :math:`Q_{set}`. The asset uses a prescribed thermal power
request and computes the corresponding mass flow using the current supply and return temperatures.

Operating modes and sign convention
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The storage uses the following sign convention for the controller thermal setpoint:

.. math::

  Q_{set} > 0 \Rightarrow \text{charging}

.. math::

  Q_{set} < 0 \Rightarrow \text{discharging}

.. math::

  Q_{set} = 0 \Rightarrow \text{idle}

The corresponding temperature assignment follows the active mode:

- **Charging**: network inlet temperature is used at connection point 0 and the storage cold
  temperature is used at connection point 1.
- **Discharging**: storage hot temperature is used at connection point 0 and network temperature at
  connection point 1.
- **Idle**: both connection temperatures are set to the internal hot and cold buffer temperatures.

Internally, the solver mass-flow sign is chosen so that discharge and charge map consistently to the
selected port orientation.

Mass flow and thermal power
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The requested mass flow magnitude is based on:

.. math::

  \dot{m} = \frac{Q_{set}}{c_p \left(T_{out} - T_{in}\right)}

where:

.. list-table::
   :widths: 25 75
   :stub-columns: 1

   * - :math:`\dot{m}`
     - Mass flow rate [kg/s]
   * - :math:`Q_{set}`
     - Controller thermal power setpoint [W]
   * - :math:`c_p`
     - Specific heat capacity at mean fluid temperature [J/(kg K)]
   * - :math:`T_{in}`
     - Inlet temperature for the current mode [K]
   * - :math:`T_{out}`
     - Outlet temperature for the current mode [K]

A storage-specific sign convention is applied internally so that charging and discharging map to
the solver mass-flow direction consistently.

Fill level update
~~~~~~~~~~~~~~~~~

The hot-volume fraction is updated from transported volume over the accumulation interval:

.. math::

   f_{new} = \mathrm{clip}\left(f_{old} + \frac{\dot{V}\,\Delta t}{V_{max}}, 0, 1\right),
   \quad \dot{V} = \frac{\dot{m}}{\rho}

where:

.. list-table::
   :widths: 25 75
   :stub-columns: 1

   * - :math:`f`
     - Fill level (hot-volume fraction) [-]
   * - :math:`\Delta t`
     - Accumulation time used for volume update [s]
   * - :math:`V_{max}`
     - Maximum storage volume [m3]
   * - :math:`\rho`
     - Fluid density at inlet-side temperature [kg/m3]

This means fill level always remains bounded between empty and full.

Effective charge and discharge power
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before assigning a storage setpoint, the controller computes effective charging and discharging
power limits from both configured power limits and available storage volume over the timestep.

The power corresponding to an available volume :math:`V_{avail}` is:

.. math::

  P_{vol} = \frac{V_{avail}}{\Delta t} \rho(\bar{T}) c_p(\bar{T}) \Delta T

with :math:`\bar{T} = (T_{hot} + T_{cold})/2` and :math:`\Delta T = T_{hot} - T_{cold}`.

The effective limits are then:

.. math::

  P_{dis,eff} = \min\left(P_{dis,max}, P_{vol}(V_{hot})\right)

.. math::

  P_{ch,eff} = \min\left(P_{ch,max}, P_{vol}(V_{max} - V_{hot})\right)

For implementation-specific edge cases, the controller applies the following piecewise behavior:

.. math::

  P_{ch,eff} =
  \begin{cases}
    0, & V_{avail,ch} \leq 0 \\
    0, & \Delta T = 0 \\
    \min\left(P_{ch,max}, P_{vol}(V_{avail,ch})\right), & \Delta T > 0
  \end{cases}

.. math::

  P_{dis,eff} =
  \begin{cases}
    0, & V_{hot} \leq 0 \\
    P_{dis,max}, & \Delta T = 0 \;\text{and}\; 0 < f < 1 \\
    0, & \Delta T = 0 \;\text{and}\; (f = 0 \;\text{or}\; f = 1) \\
    \min\left(P_{dis,max}, P_{vol}(V_{hot})\right), & \Delta T > 0
  \end{cases}

where:

.. list-table::
  :widths: 25 75
  :stub-columns: 1

  * - :math:`P_{dis,max}`
    - Configured maximum discharging power [W]
  * - :math:`P_{ch,max}`
    - Configured maximum charging power [W]
  * - :math:`P_{dis,eff}`
    - Effective maximum discharging power [W]
  * - :math:`P_{ch,eff}`
    - Effective maximum charging power [W]
  * - :math:`V_{hot}`
    - Current hot volume in storage [m3]
  * - :math:`V_{avail,ch}`
    - Available volume for charging, :math:`V_{max} - V_{hot}` [m3]
  * - :math:`f`
    - Fill level (hot-volume fraction) [-]

**Practical consequence**: as the storage approaches empty or full, the effective power limits reduce,
which may clip controller requests even when configured maximum power is higher. Also, charging
power becomes zero when :math:`\Delta T = 0`, while discharging follows the special piecewise rule
above.

Temperature state update
~~~~~~~~~~~~~~~~~~~~~~~~

When charging or discharging, the hot and cold buffer temperatures are updated using a mixing-based
specific internal energy balance for each zone. Internal energy from incoming flow is blended with
existing zone energy, then converted back to temperature through fluid property relations.

For each zone, the updated specific internal energy is:

.. math::

  u_{hot,new} = \frac{u_{hot,old} m_{hot} + u_{in,0} m_0}{m_{hot} + m_0}

.. math::

  u_{cold,new} = \frac{u_{cold,old} m_{cold} + u_{in,1} m_1}{m_{cold} + m_1}

with zone masses defined as:

.. math::

  m_{hot} = V_{hot} \rho(T_{hot}), \quad m_{cold} = (V_{max} - V_{hot}) \rho(T_{cold})

.. math::

  m_0 = \dot{m}_0 \Delta t, \quad m_1 = \dot{m}_1 \Delta t

The updated temperatures follow from the fluid-property inverse relation:

.. math::

  T_{hot,new} = T(u_{hot,new}), \quad T_{cold,new} = T(u_{cold,new})

where:

.. list-table::
  :widths: 25 75
  :stub-columns: 1

  * - :math:`u_{hot,old}`, :math:`u_{cold,old}`
    - Previous hot and cold zone specific internal energies [J/kg]
  * - :math:`u_{in,0}`, :math:`u_{in,1}`
    - Specific internal energies of incoming flow at both ports [J/kg]
  * - :math:`m_0`, :math:`m_1`
    - Inflowing masses over the timestep [kg]
  * - :math:`T(u)`
    - Temperature obtained from fluid-property relation for specific internal energy

This captures first-order thermal state evolution while remaining computationally lightweight.

Assumptions
-----------

- The storage is idealized as two **well-mixed** thermal zones (hot and cold).
- Charging and discharging are represented by sign of one power setpoint.
- Heat losses to ambient are neglected.
- Hydraulic losses inside the storage are neglected.
- Dynamic effects below the simulation timestep are not resolved.
- Fill level is clipped to the physical range [0, 1].

Limitations
-----------

- No explicit tank geometry, thermocline thickness, or stratification diffusion model.
- No dedicated startup, shutdown, or actuator dynamics.
- No explicit thermal losses through walls or piping inside the tank.
- No pressure-drop model for internal storage components.
- Accuracy depends on timestep size; large timesteps can smooth short transients.

See Also
--------

- :doc:`ates_cluster_physics` — Aquifer thermal energy storage (ATES) system
- :doc:`producer_physics` — Heat supply source
- :doc:`consumer_physics` — Heat demand sink

References
----------

.. rubric:: References

*(No references listed.)*
