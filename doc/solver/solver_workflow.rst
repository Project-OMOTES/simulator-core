Solver workflow
===============

Overview
--------

The solver is responsible for computing the hydraulic and thermal state of the network for a single
solve. It sits inside the timestep execution path and is called after controller setpoints have been
applied to the network assets.

Role in the Simulation Workflow
-------------------------------

At a high level, the execution flow is:

#. The simulation loop advances to the next timestep.
#. The controller updates network state and computes setpoints for that timestep.
#. The heat network applies those setpoints to assets.
#. The solver assembles and solves the network equation system.
#. Results are written back to assets and nodes.
#. Asset-level convergence is checked at timestep level before output is stored.

In the implementation, ``NetworkSimulation.run()`` drives the timestep loop, ``HeatNetwork`` applies
controller input and invokes ``Solver.solve()``, and the solver delegates equation solution to the
matrix layer.

Key Concepts
------------

- Timestep solve: one call to the solver that computes updated state values for the current network state.
- Equation assembly: assets and nodes each contribute equations to the global system.
- Result propagation: the solved vector is transferred back into asset and node state.

Behavior and Interpretation
---------------------------

The solver itself does not decide operational setpoints. Those come from the controller. Its task is
to find a network state that satisfies the assembled hydraulic and thermal equations for the current
inputs and topology.

Because the solve runs inside the broader timestep loop, users should interpret solver output as the
numerical state associated with one controller-driven network condition, not as a standalone control
decision.

Assumptions
-----------

- Controller inputs have already been applied before the solve begins.
- Asset and node equations together provide a square system with one equation per unknown.
- The solver writes results back into network entities after each matrix solve.

Limitations
-----------

- This page describes solver workflow, not asset-specific physical models.
- It does not replace the lower-level class reference pages for ``Solver``, ``Matrix``, or ``Network``.

Related Documentation
---------------------

- For unknowns and equation structure, see :doc:`solver_unknowns_and_equations`.
- For convergence behavior across iterations and timesteps, see :doc:`solver_convergence`.
- For asset-level physics, see :doc:`../physics/physics_main`.
