Solver
======

This section explains how the solver participates in each simulation timestep. It focuses on the
numerical role of the solver, the unknowns it resolves, and how convergence is handled between the
matrix solve and the broader timestep loop.

The solver operates on the network assembled from assets and nodes. For each solve, it builds the
equation system, computes updated hydraulic and thermal state values, and writes those results back
to the network entities.

How to use this section
-----------------------

- Start with the conceptual pages below to understand solver workflow and result interpretation.
- Use the Solver Reference page (linked below) for class-level information about solver internals.
- Use the Physics section for asset-specific constitutive relations and the Network section for
  connectivity concepts.

Conceptual pages
----------------

.. toctree::
   :maxdepth: 1

   solver_workflow
   solver_unknowns_and_equations
   solver_convergence

Implementation reference
-------------------------

For solver classes, matrix assembly, and asset-level solver implementation details, use
:doc:`../reference/solver_reference`.

Related Documentation
---------------------

- For network representation and connectivity, see :doc:`../network/network_main`.
- For interpretation of physical state variables and governing relations, see :doc:`../physics/physics_main`.
- For package-level execution context, see :doc:`../intro/intro_main`.






