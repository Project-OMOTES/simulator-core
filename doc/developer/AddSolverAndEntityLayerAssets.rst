Adding new solver and entity-layer assets
=========================================

Purpose
-------

Use this guide when no existing solver asset provides the equations for a new asset type, so
you need a new solver asset, an entity asset that wraps it, ESDL mapping, and tests at every
level. If an existing solver asset fits, use :doc:`AddEntityLayerAsset` instead; it is less
work and less risk.

This guide is for contributors working on the Python implementation. For the governing
equations of existing assets, see :doc:`../physics/physics_main`. For how the solver
assembles and iterates equations, see :doc:`../solver/solver_main`.

Relevant modules and files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 38 22 40

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``src/omotes_simulator_core/solver/network/assets/base_item.py``
     - Solver root class
     - ``BaseItem`` declares the abstract ``get_equations`` and ``disconnect_node`` and
       holds ``prev_sol`` and the matrix index.
   * - ``src/omotes_simulator_core/solver/network/assets/base_asset.py``
     - Solver asset base
     - ``BaseAsset(name, _id, number_of_unknowns=6, number_connection_points=2,
       supply_temperature=293.15)`` implements node connection, result getters, and
       reusable equations such as ``get_press_to_node_equation``.
   * - ``src/omotes_simulator_core/solver/network/assets/fall_type.py``
     - Two-port base with internal equations
     - ``FallType`` returns six equations: two pressure-to-node, two thermal, internal
       continuity, and internal pressure loss. ``HeatBoundary``, ``SolverPipe``, and
       ``HeatBufferAsset`` derive from it.
   * - ``src/omotes_simulator_core/solver/network/assets/production_asset.py``
     - Example subclass
     - ``HeatBoundary`` replaces the internal equations with prescribed mass flow or
       pressure equations.
   * - ``src/omotes_simulator_core/solver/network/assets/heat_transfer_asset.py``
     - Four-port example
     - ``HeatTransferAsset`` derives from ``BaseAsset`` with ``number_connection_points=4``
       and twelve unknowns.
   * - ``src/omotes_simulator_core/solver/matrix/index_core_quantity.py``
     - Unknown layout
     - Three core quantities per connection point: mass flow rate, pressure, and internal
       energy.
   * - ``src/omotes_simulator_core/solver/network/network.py``
     - Solver graph
     - ``add_existing_asset`` and ``connect_assets`` build the graph; ``str_to_class_dict``
       is used only by ``add_asset`` with a type string.
   * - ``src/omotes_simulator_core/entities/assets/asset_abstract.py``
     - Entity base class
     - Abstract ``set_setpoints``, ``write_to_output``, and ``postprocess``.
   * - ``src/omotes_simulator_core/adapter/transforms/esdl_asset_mapper.py``
     - Mapper dispatch table
     - ``conversion_dict_mappers`` maps ESDL classes to mapper classes.
   * - ``unit_test/solver/network/assets/`` and ``unit_test/integration/``
     - Tests
     - Solver asset unit tests and solver-level integration tests to copy from.

Execution or extension flow
---------------------------

1. Design the unknowns and equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each connection point has three unknowns (mass flow rate, pressure, and internal energy), so
an asset with :math:`n` connection points has :math:`3n` unknowns. Existing solver assets
return as many equations from ``get_equations`` as they have unknowns: six for two-port
assets and twelve for ``HeatTransferAsset``. Nodes contribute their own equations. Write down
which equation constrains which unknown before you write code; see
:doc:`../solver/solver_unknowns`.

2. Create the solver asset
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a module in ``src/omotes_simulator_core/solver/network/assets/``. Pick the closest
base class:

- ``FallType`` or one of its subclasses for two-port assets that only change some
  equations, as ``HeatBoundary`` does.
- ``BaseAsset`` for a different port count or a different set of equations, as
  ``HeatTransferAsset`` does.

.. code-block:: python

    class MySolverAsset(BaseAsset):
        def __init__(self, name: str, _id: str, my_parameter: float = 0.0) -> None:
            super().__init__(
                name=name,
                _id=_id,
                number_of_unknowns=index_core_quantity.number_core_quantities * 2,
                number_connection_points=2,
            )
            self.my_parameter = my_parameter

        def get_equations(self) -> list[EquationObject]:
            return [
                self.get_press_to_node_equation(0),
                self.get_press_to_node_equation(1),
                self.get_thermal_equations(0),
                self.get_thermal_equations(1),
                self.get_my_first_equation(),
                self.get_my_second_equation(),
            ]

Store boundary values and parameters as attributes that the entity asset can set, as
``HeatBoundary`` does with ``pre_scribe_mass_flow``, ``mass_flow_rate_set_point``, and
``set_pressure``. Use ``self.prev_sol`` and ``get_index_matrix`` to linearize nonlinear
terms around the previous iteration, following ``FallType``.

3. Create the entity asset
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a module in ``src/omotes_simulator_core/entities/assets/``. Subclass
``AssetAbstract``, call ``super().__init__(asset_name, asset_id, connected_ports)``, create the
solver asset with ``name=self.name`` and ``_id=self.asset_id``, and assign it to
``self.solver_asset``. Implement:

- ``set_setpoints(setpoints)`` — check that the required ``PROPERTY_*`` keys are present
  (existing assets raise ``ValueError``) and set the solver asset attributes.
- ``write_to_output()`` — update ``self.outputs[port][-1]`` with asset-specific values.
- ``postprocess()`` — update state at the end of a timestep, or ``pass`` when there is none.

Override ``is_converged`` when the asset must check the solved result against its setpoint,
as ``ProductionCluster`` does, and ``get_state`` when the asset controller needs state.
:doc:`AddEntityLayerAsset` describes these steps in more detail.

4. Map and register the ESDL asset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a mapper derived from ``EsdlMapperAbstract`` in
``src/omotes_simulator_core/adapter/transforms/esdl_asset_mappers/``:

.. code-block:: python

    class EsdlAssetMyAssetMapper(EsdlMapperAbstract):
        def to_esdl(self, entity: MyAsset) -> EsdlAssetObject:
            raise NotImplementedError("EsdlAssetMyAssetMapper.to_esdl()")

        def to_entity(self, esdl_asset: EsdlAssetObject) -> MyAsset:
            return MyAsset(
                asset_name=esdl_asset.esdl_asset.name,
                asset_id=esdl_asset.esdl_asset.id,
                port_ids=esdl_asset.get_port_ids(),
                my_parameter=esdl_asset.get_property(
                    esdl_property_name="myParameter", default_value=0.0
                ),
            )

Add the ESDL class and the mapper to ``conversion_dict_mappers`` in
``esdl_asset_mapper.py``. ``EsdlEnergySystemMapper`` then creates the entity, adds its
solver asset to the ``Network``, and connects it; you do not register the solver asset
yourself.

5. Connect the asset to control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure ``EsdlControllerMapper`` creates a controller for the asset and that the setpoint
dictionary contains the keys your ``set_setpoints`` requires. Reusing an existing
controller is described in :doc:`AddEntityLayerAsset`; new control behavior is described
in :doc:`ControlExtension`.

Implementation notes
--------------------

- Keep physics in the solver asset. The entity asset only translates setpoints into solver
  attributes and reads results through getters such as ``get_mass_flow_rate``,
  ``get_pressure``, ``get_temperature``, and ``get_internal_energy``.
- ``Solver.solve`` resets ``prev_sol`` before it starts and iterates until the matrix has
  converged or the iteration limit of 100 is passed. Equations that depend on
  ``prev_sol`` must give a solvable system for the reset values.
- ``FallType.get_equations`` raises ``ValueError`` when fewer than two nodes are connected
  or when ``number_of_unknowns`` is not six. Keep similar checks in new assets so that
  wiring errors fail early.
- Register the solver class in ``Network.str_to_class_dict`` only if tests or tools need to
  create it with ``Network.add_asset`` and a type string; the ESDL path uses
  ``add_existing_asset``.
- Solver assets do not import from ``entities`` or ``esdl``.

Testing and validation
----------------------

Add tests at each level:

- **Solver asset unit test** in ``unit_test/solver/network/assets/``, modelled on
  ``test_fall_type.py``: connect ``Node`` objects with ``connect_node``, call
  ``get_equations``, and check the number of equations and their indices, coefficients,
  and right-hand side. Test the error paths for missing nodes.
- **Solver-level integration test** in ``unit_test/integration/``, modelled on
  ``test_zero_flow_physics.py`` or ``test_heat_transfer_asset.py``: build a ``Network``
  with ``add_existing_asset`` and ``connect_assets``, set boundary values, call
  ``Solver(network).solve()``, and assert on mass flow, pressure, and temperature.
- **Entity unit test** in ``unit_test/entities/`` with patched solver getters, as described
  in :doc:`testing_strategy`.
- **Mapper test** in ``unit_test/adapters/transforms/esdl_asset_mappers/`` using an ESDL
  fixture in ``testdata/``.
- **Full run** through ``SimulationManager`` on a fixture that contains the asset.

Run the full suite with ``ci/linux/test_unit.sh`` or ``ci\win32\test_unit.cmd`` and the
type checker with ``ci/linux/typecheck.sh`` or ``ci\win32\typecheck.cmd``.

Common pitfalls
---------------

- **Equation count mismatch.** Returning fewer or more equations than unknowns gives a
  singular or overdetermined matrix. Count them per connection point.
- **Duplicated base equations.** ``get_press_to_node_equation`` and the thermal equations
  already link the asset to its nodes; do not add separate node-coupling equations.
- **Registering the solver asset twice.** ``Network.add_existing_asset`` raises
  ``ValueError`` for an existing name, and the mapper already adds every enabled asset.
- **Physics in the entity asset.** Computing flows or temperatures in ``set_setpoints``
  bypasses the solver and breaks convergence checks.
- **Untested at solver level.** Errors in equations are much easier to find in a
  solver-level test than in a full run.

Related documentation
---------------------

- :doc:`AddEntityLayerAsset` — entity asset, mapping, and controller details.
- :doc:`../solver/solver_main` — solver behavior.
- :doc:`../solver/solver_unknowns` — unknowns per connection point.
- :doc:`../solver/solver_convergence` — convergence criteria.
- :doc:`../physics/physics_main` — governing equations of existing assets.
- :doc:`testing_strategy` — test levels and commands.
- :doc:`api/omotes_simulator_core` — generated class and module reference.
