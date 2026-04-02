Pipes
=====

Description
-----------

The ``Pipe`` asset models a physical pipe segment in a thermal network. It represents the hydraulic
and thermal transport of fluid between two nodes, accounting for pressure losses, heat
losses, and flow characteristics. The asset is mapped from ESDL (Energy System Description
Language) objects and is parameterised by its geometric and material properties.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 40 20 30

   * - Parameter
     - Description
     - Unit
     - ESDL Asset Property
   * - ``length``
     - Pipe length
     - m
     - ``length``
   * - ``inner_diameter``
     - Inner diameter
     - m
     - see remarks on diameter [#diameter-remarks]_
   * - ``roughness``
     - Wall roughness
     - m
     - ``roughness``
   * - ``alpha_value``
     - Heat transfer coefficient
     - W/(m²·K)
     - see remarks on alpha value [#alpha-value-remarks]_
   * - ``minor_loss_coefficient``
     - Minor loss coefficient
     - —
     - ``minor_loss_coefficient``
   * - ``external_temperature``
     - Surrounding temperature
     - K
     - ``external_temperature``
   * - ``qheat_external``
     - External heat flow
     - W
     - ``qheat_external``

.. [#diameter-remarks] The inner diameter can be specified in multiple ways.
  If the ``innerDiameter`` property is not null, it is used directly.
  Otherwise, if ``diameter`` is supplied, the inner diameter is derived from the EDR database
  using default schedule ``S1``.
  If neither is available, a default diameter of 1.2 m is used.

.. [#alpha-value-remarks] The alpha value is derived from the thermal conductivity table of the ESDL asset.
  It uses a routine (``get_thermal_conductivity_table``) to extract the diameters and corresponding alpha values from the ESDL asset.
  If the table is empty, the alpha value will be set to 0 W/(m²·K) by default, meaning no heat loss. 

Additional simulation outputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default per-port outputs for mass flow, pressure, temperature, and volume flow,
the pipe asset provides the following additional outputs:

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Signal
     - Description
     - Unit
   * - ``velocity``
     - Fluid velocity at each port, see remark [#velocity-remarks]_
     - m/s
   * - ``pressure_loss``
     - Pressure loss
     - Pa
   * - ``pressure_loss_per_length``
     - Pressure loss per unit length
     - Pa/m
   * - ``heat_loss``
     - Heat loss
     - W

.. [#velocity-remarks] The fluid velocity is multiplied by a negative sign for odd ports to ensure
  that the flow direction is consistent with the sign convention used in the equations.

Physics and Assumptions
-----------------------

The pipe asset computes hydraulic and thermal behaviour using the relationships below. 

Temperature dependence of fluid properties (density, viscosity, specific heat) is accounted for using interpolation functions of
the property tables for water at constant pressure.

Pressure loss
~~~~~~~~~~~~~

Pressure loss :math:`\Delta p` is calculated using the Darcy-Weisbach equation, 
which accounts for both frictional losses along the pipe length and minor losses due to fittings, bends, etc.:

.. math::

  \Delta p = f \frac{L}{D} \frac{\rho v^2}{2} + K_{minor} \frac{\rho v^2}{2}

where:

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - :math:`\Delta p`
     - Pressure loss [Pa]
   * - :math:`f`
     - Darcy friction factor [—]
   * - :math:`L`
     - Pipe length [m]
   * - :math:`D`
     - Inner diameter [m]
   * - :math:`\rho`
     - Fluid density [kg/m³]
   * - :math:`v`
     - Fluid velocity [m/s]
   * - :math:`K_{minor}`
     - Minor loss coefficient [—]

Estimation of Darcy friction factor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Darcy friction factor :math:`f` depends on the Reynolds number :math:`Re=\left(\rho v D\right)/\mu` and is estimated as follows:

- For :math:`Re < 100`:

  .. math::
     f = 0.64

- For :math:`100 \leq Re < 2000`:

  .. math::
     f = \frac{64}{Re}

- For :math:`2000 \leq Re < 4000`, the friction factor is interpolated linearly between the laminar and turbulent values.

  .. math::
     f = f_{laminar} + \left( \frac{Re - 2000}{4000 - 2000} \right) (f_{turbulent} - f_{laminar})

  where :math:`f_{laminar} = 64/2000` and :math:`f_{turbulent}` is calculated using the turbulent correlation at :math:`Re = 4000`.

  
- For :math:`Re \geq 4000` (turbulent), the Mileikovskyi and Tkachenko (2020) explicit correlation is used:

  .. math::
     f = \left( \frac{8.128943 + A_1}{8.128943 A_0 - 0.86859209 A_1 \ln \left( \frac{A_1}{3.7099535 Re} \right)} \right)^2

  with

  .. math::
     A_0 = -0.79638 \ln \left( \frac{\epsilon/D}{8.208} + \frac{7.3357}{Re} \right)

  .. math::
    A_1 = Re \frac{\epsilon}{D} + 9.3120665 A_0

  where :math:`\epsilon` is the pipe roughness.

Heat loss
~~~~~~~~~

Heat loss :math:`Q_{loss}` is calculated using a linear heat transfer model based on the overall heat transfer coefficient :math:`U`:

.. math::

  Q_{loss} = U A (T_{fluid} - T_{ext})

where:

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - :math:`Q_{loss}`
     - Heat loss [W]
   * - :math:`U`
     - Overall heat transfer coefficient [W/(m²·K)]
   * - :math:`A`
     - Pipe surface area [m²]
   * - :math:`T_{fluid}`
     - Fluid temperature [K]
   * - :math:`T_{ext}`
     - External (surrounding) temperature [K]


Estimation of U (overall heat transfer coefficient)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The total heat transfer coefficient :math:`U` is calculated as:

.. math::
  \frac{1}{U} = \frac{1}{\alpha_{fluid}} + \frac{1}{\alpha_{wall}}

where:

- :math:`\alpha_{fluid}` is the convective heat transfer coefficient (from Nusselt number correlations)
- :math:`\alpha_{wall}` is the wall (external) heat transfer coefficient

The temperature dependent properties in the overall heat transfer coefficient are derived from the inflow temperature of the fluid.
For :math:`\dot{m} < 0`, the inflow temperature is determined by the fluid properties at the odd port, while for :math:`\dot{m} \geq 0`, it is determined by the fluid properties at the even port.
If there is no flow (:math:`\dot{m} = 0`), the inflow temperature is set to be the ambient temperature (:math:`T_{ext}`).

For laminar flow (:math:`Re \leq 10^4`), the Nusselt number is determined using the Graetz number. The Graetz number is defined as:

.. math::
  Gz = \frac{D}{L} Re Pr

and :math:`k` is the thermal conductivity of the fluid, :math:`D` is the pipe diameter, :math:`L` is the pipe length, :math:`Re` is the Reynolds number, and :math:`Pr` is the Prandtl number.

For small Reynolds numbers (:math:`Re < 1\times 10^{-6}`), the Graetz number is set to 10 to ensure a finite, but low, Nusselt number. 
This prevents numerical issues while still reflecting the low convective heat transfer in this regime.

The Nusselt number for laminar flow is then calculated as follows:

.. math::
  Nu = \begin{cases}
    1.62 Gz^{-1/3} & \text{if } Gz \leq 0.1 \\
    3.66 & \text{if } Gz > 0.1
  \end{cases}

For turbulent flow (:math:`Re > 10^4`):

.. math::
  Nu = 0.023 Re^{0.8} Pr^{0.33}

For both laminar and turbulent flow, the convective heat transfer coefficient is calculated as:

.. math::
  \alpha_{fluid} = \frac{Nu k}{D}


Assumptions
-----------

- Steady-state, one-dimensional flow.
- Fluid properties (density, viscosity, specific heat) are assumed constant along the pipe length but can vary with temperature.
- Heat loss is linear with temperature difference.
- No phase change or chemical reactions occur.
- Minor losses are lumped into a single coefficient.

Limitations
-----------

- No modelling of transient (dynamic) effects.
- No explicit modelling of pipe ageing, fouling, or insulation degradation.
- Assumes fully developed flow and uniform fluid properties along the pipe.
- The current documentation describes the intended physical meaning of the configured pipe parameters; if minor losses, ambient conditions, or external heat input are critical to a study, verify the active model configuration against the implementation used in the simulation setup.

References
----------

.. rubric:: References

- Mileikovskyi, V. & Tkachenko, T. (2020). *Precise explicit approximations of the Colebrook-White equation for engineering systems*.
- Incropera, F.P., DeWitt, D.P., Bergman, T.L., & Lavine, A.S. (2007). *Fundamentals of Heat and Mass Transfer*, 6th Edition.
- White, F.M. (2011). *Fluid Mechanics*, 7th Edition.