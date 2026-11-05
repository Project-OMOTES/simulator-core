.. _solver-workflow:

Solve Workflow
==============

Overview
--------

The solver reaches the network state through iteration by using a Newton-Rapson method to
linearize the equations: it repeatedly assembles a linear system from the current solution,
solves it, transfers the result back to the assets and nodes, and tests whether the solution
has stopped changing. The loop stops when the solution has converged or when an iteration limit
is reached.

Workflow
--------

Each call to the solver runs the following loop.

**Initialize.** The matrix solution is reset and every asset and node discards its previous
solution, so the iteration starts from a clean state.

**Assemble.** Each asset and then each node contributes its equations, linearized about the
current solution, into a single system. The number of equations always matches the number of
unknowns, so the linear system is square.

**Solve.** The assembled linear system is solved for a new solution vector. This solution is
the linearized estimate of the network state for the current iteration.

**Transfer.** The new solution is written back onto the assets and nodes, so that the next
assembly step linearizes around the updated state.

**Check and iterate.** Convergence is tested by comparing the new solution against the
solution of the previous iteration (see :doc:`solver_convergence`). If the two agree within
tolerance, the loop stops and the network state is final for the timestep. Otherwise the loop
repeats from the assembly step.

**Iteration limit.** The loop is capped at 100 iterations. If convergence is not reached
within that limit, a warning is logged and the last computed iterate is used as the result.

Because the equations are re-linearized about the latest solution on every pass, successive
iterates move toward the state that satisfies the full nonlinear network equations.

Related Documentation
---------------------

- :doc:`solver_main` — the conceptual overview and Newton-Raphson linearization statement.
- :doc:`solver_unknowns` — the quantities assembled into each linear system.
- :doc:`solver_convergence` — how the convergence check in the loop is evaluated.
- :doc:`../physics/physics_main` — the asset-internal relations that form the equations.
- :doc:`../reference/solver_reference` — class-level reference.
