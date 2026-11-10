Adding a new solver asset
=========================

Purpose
-------

Use this guide when no existing solver asset provides the equations a new component needs,
so you have to write a new class under ``solver/network/assets/``. It covers the choice of
base class, the layout of unknowns, writing ``EquationObject`` rows, and validating the new
asset with solver-level tests.

This guide is for contributors who change the solver layer. It stops at the point where the
solver asset can be built into a ``Network`` and solved with ``Solver``. Wrapping the solver
asset in an entity asset, mapping it from ESDL, and connecting it to a controller are covered
by :doc:`AddEntityLayerAsset`; once your solver asset exists, it is an existing solver asset
for that guide.

For the matrix formulation and convergence behavior, read :doc:`../solver/solver_main`,
:doc:`../solver/solver_unknowns`, and :doc:`../solver/solver_convergence`. For the
governing equations of existing assets, see :doc:`../physics/physics_main`. For a
class-level overview of the solver layer, see :doc:`solver_reference`.

Relevant modules and files
--------------------------

Paths are relative to ``src/omotes_simulator_core`` unless they start with ``unit_test/`` or
``doc/``.

.. list-table::
   :header-rows: 1
   :widths: 38 22 40

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``solver/network/assets/base_item.py``
     - Solver root class
     - ``BaseItem`` declares the abstract ``get_equations`` and ``disconnect_node``, holds
       ``prev_sol`` and ``matrix_index``, and provides ``get_index_matrix``.
   * - ``solver/network/assets/base_asset.py``
     - Solver asset base
     - ``BaseAsset`` implements node connection, result getters, and the shared equation
       builders ``get_press_to_node_equation``, ``get_thermal_equations``,
       ``get_prescribe_temp_equation``, and ``get_internal_energy_to_node_equation``.
   * - ``solver/network/assets/fall_type.py``
     - Two-port base with internal equations
     - ``FallType`` returns six equations and exposes the hooks ``update_loss_coefficient``
       and ``update_heat_supplied``. ``SolverPipe``, ``HeatBoundary``, and
       ``HeatBufferAsset`` derive from it.
   * - ``solver/network/assets/production_asset.py``
     - Example subclass of ``FallType``
     - ``HeatBoundary`` replaces the two internal equations with prescribed mass flow or
       pressure equations.
   * - ``solver/network/assets/heat_transfer_asset.py``
     - Example subclass of ``BaseAsset``
     - ``HeatTransferAsset`` uses four connection points, twelve unknowns, and switches
       between two equation sets.
   * - ``solver/matrix/index_core_quantity.py``
     - Unknown layout
     - Three core quantities per connection point: ``mass_flow_rate`` (0), ``pressure`` (1),
       and ``internal_energy`` (2).
   * - ``solver/matrix/equation_object.py``
     - Equation row
     - ``EquationObject`` holds ``indices``, ``coefficients``, and ``rhs`` for one row of the
       linear system.
   * - ``solver/network/network.py``
     - Solver graph
     - ``add_existing_asset`` and ``connect_assets`` build the graph that ``Solver`` solves;
       ``str_to_class_dict`` is used only by ``add_asset``.
   * - ``solver/solver.py``
     - Iteration loop
     - ``Solver.solve`` resets ``prev_sol``, collects equations, and iterates up to the
       iteration limit.
   * - ``unit_test/solver/network/assets/`` and ``unit_test/integration/``
     - Tests
     - One unit test file per solver asset class, and integration tests that build a
       ``Network`` by hand and call ``Solver.solve``.

Execution or extension flow
---------------------------

1. Design the unknowns and equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each connection point has three unknowns, so an asset with ``n`` connection points has
``3 n`` unknowns, stored in ``prev_sol`` in the order given by ``IndexCoreQuantity``.
``Matrix.solve`` requires the total number of equations to equal the total number of
unknowns, and ``Node`` objects only supply their own equations. A new asset therefore returns
as many equations from ``get_equations`` as it has unknowns: six for ``FallType`` and its
subclasses, twelve for ``HeatTransferAsset``.

Every connection point needs a pressure-to-node equation and a thermal equation. The
remaining equations are internal: in ``FallType`` they are continuity
(``m_0 + m_1 = 0``) and the pressure loss. Write down which equation constrains which unknown
before you write code; see :doc:`../solver/solver_unknowns`.

2. Choose the base class
~~~~~~~~~~~~~~~~~~~~~~~~

Pick the base class that already provides most of the equations:

- **A ``FallType`` subclass that overrides hooks.** If only the loss coefficient or the heat
  flux changes with the solution, override ``update_loss_coefficient`` or
  ``update_heat_supplied``. ``FallType`` calls them while building the pressure loss and
  internal energy equations. ``SolverPipe`` overrides both.
- **A ``FallType`` subclass that overrides ``get_equations``.** If the asset has two
  connection points but different internal equations, keep the four connection equations
  and replace the rest, as ``HeatBoundary`` does.
- **A direct ``BaseAsset`` subclass.** If the asset has a different number of connection
  points or no ``FallType`` equation fits, derive from ``BaseAsset`` and write all
  equations, as ``HeatTransferAsset`` does.

If an existing class already gives the right equations, do not add a solver asset; use
:doc:`AddEntityLayerAsset` instead. ``AirToWaterHeatPumpAsset`` only subclasses
``HeatBoundary`` without changing any equations.

3. Write the solver asset
~~~~~~~~~~~~~~~~~~~~~~~~~

Create a module in ``solver/network/assets/``. The constructor takes ``name`` and ``_id``,
passes the number of unknowns and connection points to ``BaseAsset``, and stores parameters
as attributes. The sketch below uses ``BaseAsset`` directly:

.. code-block:: python

    class MySolverAsset(BaseAsset):
        def __init__(
            self,
            name: str,
            _id: str,
            supply_temperature: float = 293.15,
            pressure_difference: float = 0.0,
        ) -> None:
            super().__init__(
                name=name,
                _id=_id,
                number_of_unknowns=index_core_quantity.number_core_quantities * 2,
                number_connection_points=2,
                supply_temperature=supply_temperature,
            )
            self.pressure_difference = pressure_difference

        def get_equations(self) -> list[EquationObject]:
            if len(self.connected_nodes) != 2:
                raise ValueError("The number of connected nodes must be 2!")
            return [
                self.get_press_to_node_equation(0),
                self.get_press_to_node_equation(1),
                self.get_thermal_equations(0),
                self.get_thermal_equations(1),
                self.get_internal_cont_equation(),
                self.get_pressure_difference_equation(),
            ]

        def get_pressure_difference_equation(self) -> EquationObject:
            equation_object = EquationObject()
            equation_object.indices = np.array(
                [
                    self.get_index_matrix(
                        property_name="pressure", connection_point=0, use_relative_indexing=False
                    ),
                    self.get_index_matrix(
                        property_name="pressure", connection_point=1, use_relative_indexing=False
                    ),
                ]
            )
            equation_object.coefficients = np.array([1.0, -1.0])
            equation_object.rhs = self.pressure_difference
            return equation_object

``get_internal_cont_equation`` is not part of ``BaseAsset``; write it in the same way, or
start from ``FallType`` when you need its continuity equation. Use
``use_relative_indexing=False`` for ``EquationObject.indices`` (matrix columns) and
``use_relative_indexing=True`` to read values from ``self.prev_sol``.

For nonlinear relations, linearize around the previous iteration: read the values you need
from ``self.prev_sol`` and put them in the coefficients and right-hand side, as
``FallType.get_internal_energy_equation`` and ``FallType.get_internal_pressure_loss_equation``
do.

Expose the values that the entity layer sets as plain attributes, as ``HeatBoundary`` does
with ``pre_scribe_mass_flow``, ``mass_flow_rate_set_point``, and ``set_pressure``. Results
are read through the ``BaseAsset`` getters ``get_mass_flow_rate``, ``get_pressure``,
``get_temperature``, and ``get_internal_energy``; add asset-specific getters only for values
that are not one of the core quantities.

4. Register the class (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ESDL path adds solver assets with ``Network.add_existing_asset``, so registration is not
needed for a full simulation. Add the class to ``Network.str_to_class_dict`` only if tests
or tools must create it with ``Network.add_asset`` and a type string; ``add_asset`` passes
only ``name`` and ``_id``, so every other constructor argument needs a default.

5. Hand over to the entity layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the solver asset passes its tests, follow :doc:`AddEntityLayerAsset` to subclass
``AssetAbstract``, create the solver asset in ``__init__``, assign it to
``self.solver_asset``, and map it from ESDL. The entity asset sets the attributes from
step 3 in ``set_setpoints``; it must not compute flows or temperatures itself.

Implementation notes
--------------------

- ``Solver.__init__`` assigns ``matrix_index`` to every asset, then every node, reserving
  ``number_of_unknowns`` columns each. Never hard-code matrix columns; always go through
  ``get_index_matrix``.
- ``Solver.solve`` calls ``reset_prev_sol`` on every asset and node, which sets ``prev_sol``
  to zeros. The first iteration therefore linearizes around zero flow, pressure, and internal
  energy. ``FallType.get_internal_pressure_loss_equation`` replaces a mass flow below
  ``1e-5`` with ``1e-5`` in its coefficient to keep the matrix non-singular; apply a similar
  guard to coefficients that vanish at zero.
- ``BaseAsset.get_thermal_equations`` and ``FallType.get_thermal_equations`` differ. The
  ``BaseAsset`` version returns ``get_prescribe_temp_equation`` (internal energy from
  ``supply_temperature``) when the previous mass flow at the connection point is positive,
  and ``get_internal_energy_to_node_equation`` otherwise. The ``FallType`` version returns
  the internal energy balance when the mass flow exceeds ``massflow_zero_limit`` (``1e-3``
  from ``solver_constants.py``). Choose the base class with this in mind.
- ``FallType.get_equations`` and ``HeatTransferAsset.get_equations_heat_transfer_mode``
  raise ``ValueError`` when the number of connected nodes or unknowns is wrong. Add the same
  checks to a new asset so that wiring errors are reported for the asset, not as a matrix
  error for the whole network.
- ``get_equations`` is called in every iteration. It may switch between equation sets based
  on ``prev_sol`` or attributes, as ``HeatTransferAsset`` does with ``bypass_mode``, but
  every set must have the same length.
- Hitting the iteration limit in ``Solver.solve`` logs a warning and does not raise. A
  badly linearized equation can therefore produce wrong results without an error.
- Solver assets do not import from ``entities``, ``adapter``, or ``esdl``, and contain no
  time or control logic.

Testing and validation
----------------------

Validate a new solver asset without the entity layer first:

- **Unit test** in ``unit_test/solver/network/assets/test_<asset>.py``, modelled on
  ``test_fall_type.py``. Connect ``Node`` objects with ``connect_node``, set ``prev_sol``
  where the equations depend on it, call ``get_equations``, and check the number of
  equations and the ``indices``, ``coefficients``, and ``rhs`` of each one. Test the
  ``ValueError`` paths for missing nodes and a wrong number of unknowns.
- **Solver-level integration test** in ``unit_test/integration/``, modelled on
  ``test_zero_flow_physics.py`` or ``test_heat_transfer_asset.py``. Create the assets,
  add them with ``Network.add_existing_asset``, connect them with ``connect_assets``, set
  boundary values on ``HeatBoundary`` objects, call ``Solver(network=network).solve()``, and
  assert on mass flow, pressure, and temperature through the asset getters or ``prev_sol``.
  Include a zero-flow case.
- **Existing integration tests.** Run ``test_heat_physics.py``, ``test_pressure_physics.py``,
  and ``test_zero_flow_physics.py`` if you changed a shared base class.

For a quick run of the solver tests:

.. code-block:: bash

    python -m pytest --no-cov -p no:faulthandler unit_test/solver unit_test/integration

Before opening a pull request, run the full suite with ``ci/linux/test_unit.sh`` or
``ci\win32\test_unit.cmd`` and the type checker with ``ci/linux/typecheck.sh`` or
``ci\win32\typecheck.cmd``. See :doc:`testing_strategy` for test levels and the coverage
requirement.

To document the new class, add an autodoc wrapper page under ``doc/solver/assets/``,
following ``doc/solver/assets/solver_production_asset.rst``, and list it in the
``API reference`` toctree of :doc:`solver_reference`. The generated pages under
``doc/developer/api/`` are rebuilt automatically. Build the documentation with
``doc/run_sphinx.bat`` on Windows or ``doc/run_sphinx.sh`` on Linux and check for warnings.

Common pitfalls
---------------

- **Equation count mismatch.** ``Matrix.solve`` raises ``ValueError`` for the whole network
  when equations and unknowns differ. Count equations per connection point.
- **Duplicated node coupling.** ``get_press_to_node_equation`` and the thermal equations
  already link the asset to its nodes, and ``Node.get_equations`` supplies the continuity,
  energy, and discharge equations of the node; do not add more coupling equations.
- **Wrong indexing mode.** Using relative indices in ``EquationObject.indices`` or absolute
  indices into ``prev_sol`` gives wrong results without an error.
- **Zero coefficients at start-up.** ``prev_sol`` starts at zero, so coefficients built from
  it can make the matrix singular (``RuntimeError: Matrix is singular``).
- **Physics in the entity layer.** Flows, pressures, and temperatures belong in the solver
  asset; the entity asset only sets attributes. See :doc:`AddEntityLayerAsset`.
- **Untested at solver level.** Equation errors are far easier to locate in a solver-level
  test than in a full ``SimulationManager`` run.

Related documentation
---------------------

- :doc:`AddEntityLayerAsset` — wrapping the solver asset in an entity asset, ESDL mapping,
  and controller connection.
- :doc:`solver_reference` — overview of ``Solver``, ``Matrix``, and the solver asset base
  classes.
- :doc:`network_reference` — how the ``Network`` graph is built.
- :doc:`testing_strategy` — test levels and commands.
- :doc:`../solver/solver_main` — conceptual solver description.
- :doc:`../solver/solver_unknowns` — unknowns per connection point.
- :doc:`../solver/solver_convergence` — convergence criteria.
- :doc:`../solver/asset_main` — equations shared by solver assets.
- :doc:`../physics/physics_main` — governing equations of existing assets.
- :doc:`api/omotes_simulator_core` — generated class and module reference.
