.. _solver-unknowns:

Solved Unknowns
===============

Overview
--------

The solver solves for a fixed set of core quantities at every connection point of the
network. These quantities are chosen so that the assembled system is as linear as possible,
which keeps the Newton-Raphson iteration well behaved and fast to converge.

Solved Unknowns
---------------

Each asset and node registers how many unknowns it needs and receives the matrix indices for
them. Per connection point, the solver solves for three core quantities:

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - Quantity
     - Description
     - Unit
   * - :math:`p`
     - Pressure at the connection point
     - Pa
   * - :math:`\dot{m}`
     - Mass flow rate through the connection point
     - kg/s
   * - :math:`u`
     - Specific internal energy at the connection point
     - J/kg

Specific internal energy is used as the thermal state variable rather than temperature
directly. This keeps the energy-transport terms bilinear in the solved unknowns: convective
energy transport appears as the product of mass flow and specific internal energy, both of
which are solved quantities. Temperature is recovered from the specific internal energy
through the fluid-property relations; those relations are not re-derived here (see
:doc:`../physics/physics_main`).

Near-zero flow is handled with a small mass-flow limit, ``MASSFLOW_ZERO_LIMIT`` =
:math:`10^{-3}` kg/s. Flows below this magnitude are treated as effectively zero, which
avoids ill-conditioned energy relations where the convective term would otherwise be divided
by a vanishing mass flow.

Related Documentation
---------------------

- :doc:`solver_main` — the conceptual overview.
- :doc:`solver_workflow` — how these unknowns are assembled and solved each iteration.
- :doc:`solver_convergence` — how the solved vector is tested for convergence.
- :doc:`../physics/physics_main` — fluid-property relations and asset-internal physics.
- :doc:`../reference/solver_reference` — class-level reference.
