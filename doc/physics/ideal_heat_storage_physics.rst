Ideal Heat Storage
==================

Description
-----------

The ``IdealHeatStorage`` asset represents a two-layer hot-water buffer that can either absorb heat
(charging) or release heat (discharging) in a thermal network. The storage exchanges heat with the
network through one inlet and one outlet and tracks the amount of hot volume in the vessel via a
fill level between 0 and 1.

In simulation, the asset behaves as an idealized control volume with stratified hot and cold zones.
It receives a thermal power setpoint and translates that request into mass flow and port
temperatures based on whether the storage is charging, discharging, or idle. The asset is mapped
from ESDL ``HeatStorage``.

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
     - Maximum charging power
     - W
     - ``maxChargeRate``
   * - ``max_discharge_power``
     - Maximum discharging power
     - W
     - ``maxDischargeRate``

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

The requested storage power can be clipped by the effective charge or discharge capacity of the
storage. This becomes important near empty or full states, or when the temperature difference
between the hot and cold zones is small. For controller-level dispatch behavior, see
:doc:`../controller/controller`.

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

The solved mass-flow sign follows this mode definition: charging corresponds to flow into the
storage and discharging corresponds to flow out of the storage hot zone.

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

The usable storage power is limited by both the configured charge or discharge rating and the
amount of hot or cold volume that can be exchanged during one timestep. A concise engineering
approximation is:

.. math::

  P_{ch,eff} = \min\left(P_{ch,max}, \frac{V_{max} - V_{hot}}{\Delta t} \rho c_p \Delta T\right)

.. math::

  P_{dis,eff} = \min\left(P_{dis,max}, \frac{V_{hot}}{\Delta t} \rho c_p \Delta T\right)

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
  * - :math:`\Delta T`
    - Temperature difference between hot and cold zones, :math:`T_{hot} - T_{cold}` [K]
  * - :math:`\rho`
    - Fluid density at representative storage conditions [kg/m3]
  * - :math:`c_p`
    - Specific heat capacity at representative storage conditions [J/(kg K)]

In practical terms, requested charge or discharge power can be clipped even when the configured
power rating is higher. Clipping becomes more likely when the storage approaches full or empty, or
when the hot and cold zones have little temperature difference and therefore little usable thermal
capacity.

Temperature state update
~~~~~~~~~~~~~~~~~~~~~~~~

When charging or discharging, each zone is updated with an ideal-mixing energy balance. In compact
form, the updated specific internal energy of a zone is:

.. math::

  u_{new} = \frac{u_{old} m_{old} + u_{in} m_{in}}{m_{old} + m_{in}}

The new zone temperature then follows from the fluid-property relation :math:`T(u)`. This means
incoming flow mixes instantaneously with the corresponding hot or cold zone over the timestep.

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

- :doc:`../controller/controller` -- Controller behavior for storage dispatch and coordination
- :doc:`../network/network_main` -- Network equations that determine hydraulic interaction
- :doc:`ates_cluster_physics` — Aquifer thermal energy storage (ATES) system
- :doc:`producer_physics` — Heat supply source
- :doc:`consumer_physics` — Heat demand sink

References
----------

.. rubric:: References

*(No references listed.)*
