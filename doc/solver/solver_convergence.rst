Solver convergence
==================

Overview
--------

Convergence in OMOTES.SIMULATOR_CORE is handled at two levels: inside the solver itself and at the
broader timestep level in the network simulation loop.

Role in the Simulation Workflow
-------------------------------

Inside ``Solver.solve()``, the matrix solution is updated repeatedly until the solution vector is
considered converged or an iteration limit is reached. After each matrix solve, the network receives
the updated results so assets and nodes can evaluate their next equations from the latest state.

Outside the solver, ``NetworkSimulation.run()`` may repeat an entire timestep until asset-level
convergence is reached or the timestep iteration limit is hit.

Key Concepts
------------

- Matrix convergence: checks whether consecutive solution vectors are sufficiently close.
- Solver iteration limit: stops the internal solve loop after 100 iterations.
- Timestep convergence: checks whether assets report a converged state across repeated timestep runs.
- Timestep iteration limit: stops timestep retries after 20 iterations.

Behavior and Interpretation
---------------------------

Matrix convergence is tested using relative and absolute tolerances through a vector comparison:

.. math::

   x_{new} \approx x_{old}

where closeness is evaluated using configured absolute and relative convergence thresholds.

This means the solver is not checking a single scalar residual in isolation. It is checking whether
the full solved state stops changing materially between iterations.

The timestep loop adds a second layer of stability checking. Even if one solver call converges,
asset-level post-solve behavior may still require another timestep iteration before the network is
treated as converged for output purposes.

Assumptions
-----------

- Consecutive solution vectors are a sufficient indicator of internal numerical convergence.
- Asset-level ``is_converged()`` checks represent the network's timestep stability criterion.
- Resetting the solution state at the start of a new solve provides a consistent iteration start.

Limitations
-----------

- The documentation does not define asset-specific convergence logic; that depends on each asset implementation.
- If iteration limits are reached, the current code warns or exits the loop, but this page does not prescribe recovery strategy.

Related Documentation
---------------------

- For the overall solver flow, see :doc:`solver_workflow`.
- For unknown and equation structure, see :doc:`solver_unknowns_and_equations`.
- For simulation-loop context, see :doc:`../intro/simulation_input_and_output`.