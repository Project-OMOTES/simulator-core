Solver reference
================

Purpose
-------

This page is a curated overview of the solver layer: the ``Solver`` iteration loop, the
``Matrix`` that assembles and solves the linear system, the equation objects that carry
coefficients, and the solver-side asset base classes that produce equations. It is meant
for contributors who change convergence behavior, add equations, or write a new solver
asset.

For the mathematical formulation, read :doc:`../solver/solver_main`,
:doc:`../solver/solver_workflow`, :doc:`../solver/solver_unknowns` and
:doc:`../solver/solver_convergence`. For the full list of methods, use the generated API
reference (:doc:`api/omotes_simulator_core`).

Relevant modules and files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``solver/solver.py``
     - ``Solver``: assigns matrix indices and runs the iteration loop.
     - Entry point called by ``HeatNetwork.run_time_step``.
   * - ``solver/matrix/matrix.py``
     - ``Matrix``: collects equations, solves the sparse system and checks convergence.
     - Owns the convergence criterion and the singular-matrix error.
   * - ``solver/matrix/equation_object.py``
     - ``EquationObject``: one row of the linear system (indices, coefficients, right-hand
       side).
     - The data structure every asset and node returns from ``get_equations``.
   * - ``solver/matrix/index_core_quantity.py``
     - ``IndexCoreQuantity``: maps named quantities to positions in an item's unknowns.
     - Used to find the matrix column of, for example, the mass flow at a connection point.
   * - ``solver/network/assets/base_item.py``, ``base_asset.py``, ``base_node_item.py``
     - Abstract base classes for solver assets and nodes.
     - Provide unknown bookkeeping, node connections and shared equation builders.
   * - ``solver/network/assets/``
     - Concrete solver assets (``FallType``, ``SolverPipe``, ``HeatBoundary``,
       ``HeatBufferAsset``, ``HeatTransferAsset``, ``AirToWaterHeatPumpAsset``,
       ``BaseBoundary``) and ``Node``.
     - The physics of each component, expressed as equations.
   * - ``solver/utils/``
     - Fluid properties and helper functions.
     - Temperature-dependent water properties used by the equations.

Execution or extension flow
---------------------------

Solve loop
~~~~~~~~~~

1. ``Solver.__init__`` stores the ``Network``, creates a ``Matrix`` and calls
   ``set_unknowns_matrix``. That method gives every asset and then every node a
   ``matrix_index``, reserving ``number_of_unknowns`` columns for each.
2. ``Solver.solve`` resets the matrix solution and the previous solution of every item.
3. While ``Matrix.is_converged`` is ``False``:

   a. ``get_equations`` collects the equations of all assets and nodes.
   b. ``Matrix.solve`` checks that the number of equations equals the number of unknowns,
      builds a SciPy sparse matrix and solves it with ``spsolve``.
   c. ``results_to_assets`` slices the solution vector and stores it in each asset and
      node as ``prev_sol``, which the next iteration uses to linearise the equations.

4. After 100 iterations the loop logs a warning and stops, even if the solution has not
   converged.

Adding equations
~~~~~~~~~~~~~~~~

A solver asset contributes equations through ``get_equations``. Each equation is an
``EquationObject`` whose indices are matrix columns, found with ``matrix_index`` and
``IndexCoreQuantity``. ``BaseAsset`` already provides builders for the equations that
connect an asset to its nodes (pressure, energy and mass flow to node). A new asset normally
adds only its internal equations. The step-by-step guide is
:doc:`AddSolverAndEntityLayerAssets`.

Implementation notes
--------------------

- ``Matrix.is_converged`` compares the new and previous solution with ``numpy.allclose``,
  using ``absolute_convergence`` and ``relative_convergence`` (both ``1e-6``) as the
  absolute and relative tolerances.
- ``Matrix.reset_solution`` sets only the new solution back to ones at the start of each
  ``Solver.solve`` call. The old solution still holds the result of the previous call
  until the first ``Matrix.solve`` of the new call replaces it.
- ``Matrix.solve`` raises ``ValueError`` when equations and unknowns do not match, and
  ``RuntimeError`` ("Matrix is singular") when the solution contains ``NaN``. Both usually
  mean an asset returned the wrong number of equations or a node is not connected.
- Hitting the iteration limit does not raise an error. The entity layer reports
  non-convergence separately through ``is_converged`` on the entity assets.
- ``BaseAsset`` defaults to six unknowns and two connection points. Boundaries
  (``BaseBoundary``) use three unknowns and one connection point. ``Node`` uses three
  unknowns. If you change these numbers, the number of equations must change with them.
- The solver layer does not know about ESDL, controllers or time. It only sees the
  ``Network`` and the values that entity assets set on solver assets.

Testing and validation
----------------------

- ``unit_test/solver/matrix/test_matrix.py`` and ``test_equation_object.py`` cover the
  matrix and equation objects.
- ``unit_test/solver/network/assets/`` holds one test file per solver asset class,
  including ``test_base_asset.py``, ``test_node.py`` and ``test_solver_pipe.py``.
- ``unit_test/integration/test_heat_physics.py``, ``test_pressure_physics.py`` and
  ``test_zero_flow_physics.py`` build networks by hand with ``Network`` and ``Solver`` and
  check physical results. Use them to validate equation changes.

See :doc:`testing_strategy` for commands and test patterns.

Common pitfalls
---------------

- Returning a different number of equations than the asset has unknowns. The matrix check
  fails for the whole network, not for the asset.
- Hard-coding matrix column numbers instead of using ``matrix_index`` and
  ``IndexCoreQuantity``.
- Assuming the loop raises an error when it does not converge.
- Adding control or time-dependent logic to solver assets. That belongs in the entity
  asset or the controller.
- Changing the convergence settings without running the integration tests.

Related documentation
---------------------

- :doc:`architecture` — package layering and the two-layer asset model.
- :doc:`simulation_flow` — where ``Solver.solve`` is called.
- :doc:`network_reference` — how the ``Network`` passed to the solver is built.
- :doc:`asset_reference` — entity assets that set values on solver assets.
- :doc:`AddSolverAndEntityLayerAssets` — guide for writing a new solver asset.
- :doc:`../solver/solver_main` — conceptual solver description.
- :doc:`../physics/physics_main` — per-asset equations.

API reference
-------------

.. toctree::
   :maxdepth: 1

   ../solver/solver
   ../solver/matrix
   ../solver/equation_object
   ../solver/solver_utility
   ../solver/asset_main
   ../solver/assets/base_node_item
   ../solver/assets/solver_boundary
   ../solver/assets/solver_production_asset
   ../solver/assets/solver_buffer_asset
   ../solver/assets/solver_heat_transfer_asset
   ../solver/assets/solver_air_to_water_heat_pump_asset
