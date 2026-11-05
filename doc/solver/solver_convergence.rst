.. _solver-convergence:

Convergence
===========

Overview
--------

The solver decides that it has found the network state when the solution stops changing
between iterations. Convergence is judged by comparing the new solution vector against the
previous iteration's vector using a combined absolute and relative tolerance test.

Convergence
-----------

The iteration is converged when every entry of the new solution agrees with the corresponding
entry of the previous solution within tolerance:

.. math::

   \left| s_{new} - s_{old} \right| \le a_{tol} + r_{tol} \left| s_{old} \right|

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - :math:`s_{new}`
     - Solution entry from the current iteration
   * - :math:`s_{old}`
     - Solution entry from the previous iteration
   * - :math:`a_{tol}`
     - Absolute tolerance, :math:`10^{-6}`
   * - :math:`r_{tol}`
     - Relative tolerance, :math:`10^{-6}`

The absolute term keeps quantities that are near zero from blocking convergence, while the
relative term scales the allowed change with the magnitude of the quantity, so large
pressures and small mass flows are each judged on a comparable footing. The check must hold
for every solved unknown at once; a single entry still changing keeps the iteration running.

In practice, tighter tolerances require more iterations to satisfy, while looser tolerances
converge sooner at the cost of accuracy. If the criterion is not met within the iteration
limit, the solver logs a non-converged warning and reports the last iterate as the result for
the timestep (see :doc:`solver_workflow`).

Related Documentation
---------------------

- :doc:`solver_main` — the conceptual overview.
- :doc:`solver_workflow` — where the convergence check sits in the solve loop.
- :doc:`solver_unknowns` — the solved vector that is tested against tolerance.
- :doc:`../reference/solver_reference` — class-level reference.
