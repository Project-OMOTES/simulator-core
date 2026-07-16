.. _solver-main:

Solver
======

Overview
--------

The solver computes the hydraulic and thermal state of the thermal network for each
simulation step. It owns the :doc:`Network <../network/network_main>` of assets and nodes
together with the matrix that holds the assembled system, and it mediates between the two:
it collects the linearized equations contributed by each asset and node, passes them to the
matrix to solve, and writes the resulting state back onto the assets and nodes.

The network equations are nonlinear, mainly because pressure losses and convective energy
transport depend on the unknowns themselves. The solver does not solve this nonlinear system
directly. Instead, each iteration linearizes the equations about the current solution using
the Newton-Raphson method, assembles them into a linear system, and solves that system. The
new state becomes the linearization point for the next iteration, and the process repeats
until the solution no longer changes within tolerance.

Role in the Simulation Workflow
-------------------------------

The solver runs once per simulation timestep, after the controller has translated its
setpoints into asset inputs. Given those inputs it determines the network state — pressure,
mass flow, and thermal state at every connection point — that is consistent with both the
controller's operation and the asset-internal physics. The solved state is then reported as
the result for that timestep.

The three pages below expand the individual aspects of this process: how the iteration is
assembled and driven, which quantities are solved, and how convergence is determined.

.. toctree::
   :maxdepth: 1

   solver_workflow
   solver_unknowns
   solver_convergence

Related Documentation
---------------------

- :doc:`solver_workflow` — the assemble, solve, check, and iterate loop.
- :doc:`solver_unknowns` — the quantities solved per connection point.
- :doc:`solver_convergence` — the absolute and relative convergence criteria.
- :doc:`../network/network_main` — how assets and nodes are connected into the network.
- :doc:`../physics/physics_main` — the asset-internal constitutive relations.
- :doc:`../controller/controller_behavior` — how setpoints become solver inputs.
- :doc:`../reference/solver_reference` — class-level reference.
