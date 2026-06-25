Solver unknowns and equations
=============================

Overview
--------

The solver resolves hydraulic and thermal state variables over the assembled network. Unknowns are
stored in one global solution vector and indexed across assets and nodes.

Role in the Simulation Workflow
-------------------------------

Before the first solve, the solver assigns matrix indices to each asset and node according to the
number of unknowns they contribute. During each iteration, assets and nodes return their current
equations and the matrix layer solves the resulting system.

Key Concepts
------------

The primary unknowns described by the solver documentation are:

#. Mass flow rate :math:`\dot{m}` [kg/s]
#. Pressure :math:`p` [Pa]
#. Specific internal energy :math:`u` [J/kg]

Specific internal energy is used as the thermal state variable in the solve. Temperature is then
interpreted through the fluid-property relations described in the Physics section.

Behavior and Interpretation
---------------------------

The global equation system is assembled from two sources:

- Asset equations: represent pressure, energy, and component-specific behavior across each asset.
- Node equations: enforce continuity and state consistency where assets connect.

For the system to be solvable, the number of equations must equal the number of unknowns:

.. math::

   N_{equations} = N_{unknowns}

The matrix layer verifies this equality before solving. If too many or too few equations are
supplied, the solve is rejected rather than silently proceeding with an inconsistent system.

Users should interpret the solution vector as the internal numerical representation of the network
state. Asset and node result values are derived by mapping segments of that vector back to the
corresponding objects.

Assumptions
-----------

- Assets and nodes correctly report how many unknowns and equations they contribute.
- The assembled system can be represented as a sparse matrix.
- The solved state is meaningful only after it has been propagated back to assets and nodes.

Limitations
-----------

- This page does not enumerate asset-specific equations; those belong in Physics.
- It does not document every matrix or equation-object method; those belong in the detailed solver pages.

Related Documentation
---------------------

- For timestep flow around the solver, see :doc:`solver_workflow`.
- For convergence handling, see :doc:`solver_convergence`.
- For governing physical relations, see :doc:`../physics/physics_main`.
