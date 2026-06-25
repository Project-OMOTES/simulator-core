Solver Behavior
================

Overview
--------

This page describes the equation system the solver assembles each simulation timestep and how
solving that system determines the realized hydraulic and thermal state. It explains the solver
at the same level of detail as the physics asset pages, but from the perspective of the equation
system rather than a single asset's constitutive relations.

The solver does not decide operational setpoints. Those are written onto assets by the controller
before the solve begins (see :doc:`../controller/controller_behavior`). The solver's task is to
find mass flow rates, pressures, and internal energies that satisfy every asset and node equation
simultaneously for that fixed set of inputs. The timestep path is centered on ``Solver.solve()``:
it assembles equations from every asset and node, solves the resulting sparse linear system, writes
the result back onto the network, and repeats until the solution stops changing materially between
iterations or an iteration limit is reached.

Solver Inputs
-------------

The solver reads the following inputs each timestep.

.. list-table::
   :header-rows: 1

   * - Input
     - Description
     - Unit
   * - Asset and node equation contributions
     - Mass continuity, energy balance, and pressure-drop equations each asset and node
       contributes for the current iteration
     - -
   * - Controller setpoints
     - Heat demand, prescribed inlet/outlet temperatures, and the pressure-setting flag already
       written onto assets before the solve begins
     - asset-specific
   * - Previous-iteration solution
     - The most recently solved mass flow rate, pressure, and internal energy at every
       connection point, used to linearize nonlinear terms
     - kg/s, Pa, J/kg
   * - Absolute convergence tolerance
     - Threshold below which an unknown is treated as unchanged between iterations
     - matches unknown
   * - Relative convergence tolerance
     - Threshold below which an unknown's relative change is treated as negligible
     - -
   * - Iteration limit
     - Maximum number of iterations attempted before the solve is abandoned with a warning
     - -

Equation Assembly and Iteration
--------------------------------

Core Unknowns
~~~~~~~~~~~~~

Every connection point in the network carries three unknowns: mass flow rate :math:`\dot{m}`
[kg/s], pressure :math:`p` [Pa], and specific internal energy :math:`u` [J/kg]. A node has one
implicit connection point of its own; a two-port asset (pipes, heat-transfer two-port components,
boundaries, producers, consumers, storages) has two; the four-port heat-transfer asset has four.

Node Equations
~~~~~~~~~~~~~~

Each node contributes three equations:

- **Mass continuity**: the sum of the node's own mass flow rate and the mass flow rates of every
  connected asset at its connecting point equals zero.
- **Energy balance**: if every connected flow is inbound, every connected flow is outbound, or all
  connected flows are within the numerical zero-flow threshold, the node instead prescribes its
  internal energy to a fixed initial value (there is no meaningful mixing to solve for). Otherwise
  the node enforces a linearized energy balance across all connected flows:

  .. math::

     \sum_i \dot{m}_i u_i = 0

  Because :math:`\dot{m}_i u_i` is bilinear in the unknowns, each iteration linearizes it around
  the previous iteration's values (superscript :math:`k-1`):

  .. math::

     \sum_i \left( \dot{m}_i^{k-1} u_i + u_i^{k-1} \dot{m}_i \right) = \sum_i \dot{m}_i^{k-1} u_i^{k-1}

  where the sum runs over the node's own connection and every asset connected to it.
- **Discharge equation**: a third equation fixes the node's own implicit mass flow rate to zero,
  completing the three equations needed for the node's three unknowns. Exactly one asset in each
  hydraulically connected part of the network instead carries a fixed reference pressure, chosen
  by the controller (see :doc:`../controller/controller_behavior`'s "Pressure-Setting Behavior").

Two-Port Asset Equations
~~~~~~~~~~~~~~~~~~~~~~~~~

Two-port assets (for example pipes, producers, consumers, and ideal/ATES storages) carry six
unknowns (two connection points times three core quantities) and six equations:

- Two **pressure-to-node** equations, one per connection point, tying the asset's pressure at that
  point to its connected node's pressure.
- Two **thermal** equations, chosen per connection point from the previous iteration's flow at
  that point: a connection point with significant inflow contributes the asset's bilinear internal
  energy balance,

  .. math::

     \dot{m}_0 u_0 + \dot{m}_1 u_1 + Q_{asset} = 0

  linearized the same way as the node energy balance, where :math:`Q_{asset}` is the heat supplied
  to or extracted from the asset (positive when heat is added). A connection point with negligible
  or reversed inflow instead ties the asset's internal energy directly to its connected node's
  value.
- One **internal continuity** equation, :math:`\dot{m}_0 + \dot{m}_1 = 0`, enforcing that no mass
  accumulates inside the asset.
- One **internal pressure-loss** equation,

  .. math::

     p_0 - p_1 - 2 K \left| \dot{m}_0 \right| \dot{m}_0 = 0

  where :math:`K` is the asset's loss coefficient. For pipes, :math:`K` is derived each iteration
  from the previous iteration's flow through the friction-factor correlations described in
  :doc:`../physics/pipe_physics`; this page does not re-derive that correlation.

Four-Port Heat-Transfer Asset Equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The four-port heat-transfer asset (used for heat exchangers and four-port heat pumps) carries
twelve unknowns (four connection points times three core quantities) and extends the same pattern
to both of its hydraulic sides: each side's pressures link to its connected node, each side's
outlet temperature is prescribed or linked to its node depending on flow direction, and one
mass-flow-or-pressure pair per side encodes whether that side is actively converting heat or
passing flow through as a bypass. Which mode is active is decided by the controller for the
current timestep (see :doc:`../controller/controller_behavior`'s "Heat-Transfer Asset Handling");
the asset's conversion-factor physics are described in :doc:`../physics/heat_pump_physics` and
:doc:`../physics/heat_exchanger_physics`.

Iteration Scheme
~~~~~~~~~~~~~~~~~

``Solver.solve()`` resets the solution vector to a uniform initial guess, then repeats the
following sequence:

#. Assemble the equations above from every asset and node, using the previous iteration's values
   wherever a nonlinear or bilinear term needs linearizing.
#. Solve the resulting sparse linear system with a direct sparse solver.
#. Write the new solution back onto every asset and node so the next iteration linearizes around
   it.
#. Check whether the new and previous solution vectors are close within the configured absolute
   and relative tolerances; if so, stop. Otherwise repeat, up to the iteration limit. If the limit
   is reached first, the solver logs a warning and returns the last computed solution as-is.

This is a fixed-point (successive-substitution) iteration: nonlinear terms are not solved
implicitly within one linear solve, they are re-linearized and resolved repeatedly until the
solution stabilizes. For the equation-count bookkeeping behind "every asset and node contributes
exactly the equations needed for its unknowns," see :doc:`solver_unknowns_and_equations`.

Quantities Solved
------------------

Each solve produces the following per connection point, written back onto the corresponding asset
or node.

.. list-table::
   :header-rows: 1

   * - Quantity
     - Description
     - Unit
   * - ``mass_flow_rate``
     - Solved mass flow rate at the connection point
     - kg/s
   * - ``pressure``
     - Solved pressure at the connection point
     - Pa
   * - ``internal_energy``
     - Solved specific internal energy at the connection point; interpreted as temperature through
       the fluid-property relations
     - J/kg

Physical Impact
----------------

Pressure Drop and Flow Distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The pressure-drop closure :math:`p_0 - p_1 = 2 K |\dot{m}_0| \dot{m}_0` is quadratic in flow, and
for pipes :math:`K` itself depends on the flow through the friction-factor correlation. Because
both are re-evaluated each iteration from the previous flow before the next linear solve, the
converged flow split across parallel paths is the outcome of an iterative search, not a fixed
proportional division. The practical consequence is that a topology or boundary-pressure change
can shift flow distribution nonlinearly rather than in direct proportion to the change.

Node Mixing and Delivered Temperature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Where multiple flows merge at a node, the linearized energy balance converges to the flow-weighted
mix of every connected inflow's internal energy. The practical consequence is that the temperature
seen downstream of a junction depends on the converged mass-flow split between its inflows, so a
change in demand or production elsewhere in the network can shift downstream delivered temperature
even when the total injected heat is unchanged. For the asset-level heat-to-temperature relation,
see :doc:`../physics/consumer_physics` and :doc:`../physics/producer_physics`.

Flow Direction and Thermal-Equation Choice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because each two-port connection point's thermal equation is selected from the previous
iteration's flow sign, a connection point whose solved flow direction reverses during iteration
switches between a prescribed-temperature equation and a node-linked equation. The practical
consequence is that the solved flow direction at a connection need not match the direction implied
by controller setpoints, and the realized temperature interpretation at that point changes
accordingly.

Pressure-Setting Choice
~~~~~~~~~~~~~~~~~~~~~~~~

Exactly one asset in each hydraulically connected part of the network anchors that part with a
fixed reference pressure, selected by the controller rather than by the solver itself (see
:doc:`../controller/controller_behavior`'s "Pressure-Setting Choice"). Changing which asset carries
that boundary changes the solved pressure distribution and flow pattern throughout that part of the
network even when every heat setpoint is unchanged.

Non-Convergence
~~~~~~~~~~~~~~~~

If the iteration limit is reached before the solution satisfies the convergence tolerances, the
solver returns the last computed solution without a warning being escalated beyond a log message.
The practical consequence is that any of the interpretations above are only valid once convergence
is confirmed; an unconverged solve should be treated as an unreliable snapshot of the equation
system rather than a physically consistent state.

Assumptions
-----------

- Controller setpoints (heat demand, prescribed temperatures, the pressure-setting flag) are fixed
  inputs to the solve and do not change while the solver iterates.
- Nonlinear and bilinear terms are linearized using the previous iteration's values rather than
  solved implicitly within a single linear solve.
- The assembled system has exactly one equation per declared unknown.
- The solution vector starts from a uniform initial guess at the beginning of every new solve.

Limitations
-----------

- This page does not describe asset-specific constitutive correlations (friction factor,
  heat-transfer coefficients, conversion factors); see the relevant page under
  :doc:`../physics/physics_main`.
- It does not enumerate every equation branch for every asset type; boundary, production, buffer,
  and heat-pump assets follow the same continuity/energy/pressure-drop pattern with parameters
  described in Physics.
- If the iteration limit is reached, this page does not prescribe a recovery strategy; the
  returned state should be treated as unreliable.
- It does not replace the lower-level class reference for ``Solver``, ``Matrix``, or ``Network``.

Related Documentation
----------------------

- :doc:`solver_main` for the conceptual solver overview.
- :doc:`solver_unknowns_and_equations` for how unknowns and equations are counted and indexed.
- :doc:`solver_convergence` for the conceptual description of matrix- and timestep-level
  convergence.
- :doc:`../physics/pipe_physics` for the friction-factor and heat-transfer-coefficient
  correlations used in the pressure-drop and energy equations.
- :doc:`../physics/physics_main` for asset-level physical interpretation more broadly.
- :doc:`../controller/controller_behavior` for how controller setpoints, including the
  pressure-setting choice, become solver inputs.
- :doc:`../reference/solver_reference` for solver implementation reference.
