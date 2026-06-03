AtesCluster
===========

Description
-----------

The ``AtesCluster`` asset represents an Aquifer Thermal Energy Storage (ATES) system in the
thermal network. It can operate in charging mode (injecting heat into the aquifer) and
discharging mode (extracting heat from the aquifer). In the network equations, the asset behaves
as a controllable thermal boundary with a prescribed mass flow and supply temperature.

The subsurface thermal response is represented through ROSIM, an external aquifer model developed
by TNO, and the resulting hot-well and cold-well temperatures are used to update the ATES
operating point between timesteps.
The asset is mapped from ESDL ``ATES`` properties and receives controller-provided setpoints during
simulation.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 40 20 30

   * - Parameter
     - Description
     - Unit
     - ESDL Asset Property
   * - ``aquifer_depth``
     - Depth of the top of the aquifer
     - m
     - ``aquiferTopDepth``
   * - ``aquifer_thickness``
     - Aquifer thickness
     - m
     - ``aquiferThickness``
   * - ``aquifer_mid_temperature``
     - Undisturbed aquifer mid temperature
     - degC
     - ``aquiferMidTemperature``
   * - ``aquifer_net_to_gross``
     - Net-to-gross ratio used in aquifer parameterization
     - -
     - ``aquiferNetToGross``
   * - ``aquifer_porosity``
     - Effective porosity
     - -
     - ``aquiferPorosity``
   * - ``aquifer_permeability``
     - Horizontal permeability
     - mD
     - ``aquiferPermeability``
   * - ``aquifer_anisotropy``
     - Permeability anisotropy factor
     - -
     - ``aquiferAnisotropy``
   * - ``salinity``
     - Groundwater salinity
     - ppm
     - ``salinity``
   * - ``well_casing_size``
     - Well casing diameter parameter
     - inch
     - ``wellCasingSize``
   * - ``well_distance``
     - Distance between hot and cold wells
     - m
     - ``wellDistance``
   * - ``temperature_in``
     - Initial inlet temperature used to start operation
     - K
     - controller-set (runtime)
   * - ``temperature_out``
     - Initial outlet temperature used to start operation
     - K
     - controller-set (runtime)

Controlled Parameters
~~~~~~~~~~~~~~~~~~~~~

The controller provides a setpoint dictionary with the following user-relevant signals:

.. list-table::
   :header-rows: 1
   :widths: 20 60 10

   * - Signal
     - Description
     - Unit
   * - :math:`Q_{demand}`
     - Requested heat demand. The ATES thermal allocation uses opposite sign internally.
     - W
   * - :math:`T_{in,set}`
     - Inlet temperature setpoint used at the first timestep.
     - K
   * - :math:`T_{out,set}`
     - Outlet temperature setpoint used at the first timestep.
     - K

From the second timestep onward, the inlet or outlet temperature is partly taken from the solved
network state and partly from aquifer well temperatures, depending on charging or discharging mode.

Additional simulation outputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ATES asset writes the following result signals for each timestep:

.. list-table::
   :header-rows: 1
   :widths: 20 60 10

   * - Signal
     - Description
     - Unit
   * - ``mass_flow``
     - Solved mass flow through the ATES boundary
     - kg/s
   * - ``pressure_supply``
     - Pressure at ATES connection point 0
     - Pa
   * - ``pressure_return``
     - Pressure at ATES connection point 1
     - Pa
   * - ``temperature_in``
     - Solved inlet temperature at connection point 0
     - K
   * - ``temperature_out``
     - Solved outlet temperature at connection point 1
     - K

Physics and Assumptions
-----------------------

The ``AtesCluster`` couples network-side heat exchange to subsurface thermal storage behavior. The
controller requests thermal exchange, the model computes the required mass flow from the network
temperature lift, and the aquifer model updates hot- and cold-well temperatures used in subsequent
timesteps.

Operating mode and sign convention
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The internal thermal allocation is defined as:

.. math::

   Q_{alloc} = -Q_{demand}

with:

.. math::

   Q_{alloc} > 0 \Rightarrow \text{injection (charging aquifer)}

.. math::

   Q_{alloc} < 0 \Rightarrow \text{production (discharging aquifer)}

Mass flow
~~~~~~~~~

The required mass flow follows the standard thermal power balance:

.. math::

   \dot{m} = \frac{Q_{alloc}}{c_p (T_{out} - T_{in})}

where :math:`c_p` is fluid specific heat capacity and :math:`T_{in}, T_{out}` are the active ATES
boundary temperatures for the current mode.

Temperature coupling with wells
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ATES boundary supply temperature depends on flow direction:

.. math::

   \dot{m} \ge 0 \Rightarrow T_{supply} = T_{cold,well}

.. math::

   \dot{m} < 0 \Rightarrow T_{supply} = T_{hot,well}

After each timestep, the aquifer model updates :math:`T_{hot,well}` and :math:`T_{cold,well}` from
the exchanged flow and thermal conditions. This captures long-term thermal storage and recovery
effects in simplified form.

Aquifer flow conversion
~~~~~~~~~~~~~~~~~~~~~~~

Before calling the aquifer model, mass flow is converted to volumetric flow using a fixed saline
density:

.. math::

   \dot{V} = \frac{\dot{m}}{\rho}

with :math:`\rho \approx 1027\ \text{kg/m3}` in the current model.

Assumptions
-----------

- The aquifer response is represented by ROSIM, configured from ESDL aquifer and well properties.
- Network-side ATES behavior is quasi-steady per timestep.
- Fixed fluid density is used for mass-to-volume conversion in aquifer calculations.
- First timestep temperatures are taken directly from controller setpoints.

Limitations
-----------

- The model does not resolve detailed 3D groundwater hydraulics in the network solver itself.
- Density and thermophysical-property variation in the aquifer flow conversion are simplified.
- Wellbore thermal losses and mechanical constraints are not modeled explicitly.
- Accuracy depends on the validity and calibration of the configured external aquifer model.

See Also
--------

- :doc:`ideal_heat_storage_physics` — In-tank heat storage system
- :doc:`producer_physics` — Heat production boundary
- :doc:`consumer_physics` — Heat demand boundary

References
----------

.. rubric:: References

- TNO and Geological Survey of the Netherlands (NLOG), tools overview including ROSIM:
  https://www.nlog.nl/en/tools