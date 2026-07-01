Adding a New Physics Asset
==========================

Purpose
-------

Use this guide when you need to implement a new thermo-hydraulic asset type in the simulator —
for example a new heat pump variant, a storage asset, or a pipe variant. The guide walks you
through all four implementation steps: entity layer, solver layer, ESDL mapper, and mapper
registration. It then points you to test patterns and related documentation.

This page is for contributors who work at the Python implementation level. It assumes you can
already navigate the repository and run the unit test suite. For conceptual asset behavior and
governing relations, consult the Physics section rather than this guide.

Where Assets Live
-----------------

The simulator represents each asset in two separate layers, each with a distinct responsibility:

**Entity layer** — ``src/omotes_simulator_core/entities/assets/``
    High-level Python classes that own per-timestep state, apply setpoints, and collect output.
    All entity-layer assets inherit from ``AssetAbstract``.

**Solver layer** — ``src/omotes_simulator_core/solver/network/assets/``
    Low-level classes that contribute matrix equations to the nonlinear solver. All solver-layer
    assets ultimately inherit from ``BaseItem`` (via ``BaseAsset`` for two-port thermo-hydraulic
    assets, or via specialized base classes such as ``FallType`` for assets with different
    topologies).

The entity-layer class holds a reference to its corresponding solver-layer instance as
``self.solver_asset``. The entity layer calls into the solver layer to read hydraulic and thermal
results; the solver layer calls ``get_equations()`` to supply the matrix builder.

Step-by-step Workflow
---------------------

1. Create the entity-layer asset class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new file in ``src/omotes_simulator_core/entities/assets/``, for example
``my_asset.py``.

Inherit from ``AssetAbstract``:

.. code-block:: python

    from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract

    class MyAsset(AssetAbstract):
        asset_type = "my_asset"
        number_of_con_points: int = 2  # adjust to match port count

        def __init__(self, asset_name: str, asset_id: str, connected_ports: list[str]) -> None:
            super().__init__(asset_name, asset_id, connected_ports)
            # initialise asset-specific state here

The following methods **must** be implemented:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Method
     - Responsibility
   * - ``set_setpoints(self, setpoints: dict)``
     - Accept a dictionary of setpoint names and values and apply them to the asset's internal
       state before each solver call. Raise ``KeyError`` if a required setpoint is missing.
   * - ``write_to_output(self)``
     - Append asset-specific computed quantities (e.g. heat power, electrical consumption) to
       ``self.outputs`` for the current timestep. Call ``self.write_standard_output()`` first to
       record the standard mass-flow, pressure, and temperature entries.

The following methods have default no-op implementations in ``AssetAbstract`` and may be
overridden when the asset carries state that must be exposed:

- ``get_setpoints(self) -> dict[str, float]`` — return current setpoint values.
- ``get_state(self) -> dict[str, float]`` — return current internal state values.

Instantiate the matching solver-layer object and assign it to ``self.solver_asset`` before
the asset is connected to the network. See the existing ``ProductionCluster.__init__`` and
``HeatPump.__init__`` for concrete examples.

2. Create the solver-layer asset class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new file in ``src/omotes_simulator_core/solver/network/assets/``, for example
``my_solver_asset.py``.

For a standard two-port thermo-hydraulic asset, inherit from ``BaseAsset``:

.. code-block:: python

    from omotes_simulator_core.solver.network.assets.base_asset import BaseAsset
    from omotes_simulator_core.solver.matrix.equation_object import EquationObject

    class MySolverAsset(BaseAsset):

        def __init__(self, name: str, _id: str) -> None:
            super().__init__(
                name=name,
                _id=_id,
                number_of_unknowns=6,       # 3 quantities × 2 ports
                number_connection_points=2,
            )

        def get_equations(self) -> list[EquationObject]:
            # Return the matrix equations that constrain this asset's unknowns.
            ...

``BaseItem`` (the root of the solver hierarchy) declares ``get_equations`` as abstract;
every concrete solver asset must implement it. The method must return one ``EquationObject``
per unknown so that the matrix builder can assemble the global system.

For assets with different topologies (for example an asset with four ports, such as a
water-to-water heat pump), examine ``HeatTransferAsset`` and ``FallType`` as starting points
rather than ``BaseAsset`` directly.

Setter methods for boundary conditions (e.g. supply temperature, prescribed mass flow,
prescribed pressure) are plain attributes or simple methods. Study ``HeatBoundary`` and
``HeatTransferAsset`` for representative patterns before writing new equation logic.

3. Create the ESDL mapper
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new file in
``src/omotes_simulator_core/adapter/transforms/esdl_asset_mappers/``, for example
``my_asset_mapper.py``.

Inherit from ``EsdlMapperAbstract``:

.. code-block:: python

    from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract
    from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
    from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
    from omotes_simulator_core.entities.assets.my_asset import MyAsset


    class EsdlMyAssetMapper(EsdlMapperAbstract):

        def to_esdl(self, entity: MyAsset) -> EsdlAssetObject:
            raise NotImplementedError("EsdlMyAssetMapper.to_esdl()")

        def to_entity(self, esdl_asset: EsdlAssetObject) -> AssetAbstract:
            return MyAsset(
                asset_name=esdl_asset.esdl_asset.name,
                asset_id=esdl_asset.esdl_asset.id,
                connected_ports=esdl_asset.get_port_ids(),
                # read additional ESDL properties with esdl_asset.get_property(name, default)
            )

Use ``esdl_asset.get_property(name, default)`` to read optional ESDL attributes safely.
Use ``esdl_asset.get_port_ids()`` to obtain the ordered list of port identifiers.

4. Register the mapper
~~~~~~~~~~~~~~~~~~~~~~~

Open ``src/omotes_simulator_core/adapter/transforms/esdl_asset_mapper.py`` and add two
changes.

First, import your new mapper class at the top of the file alongside the existing imports:

.. code-block:: python

    from omotes_simulator_core.adapter.transforms.esdl_asset_mappers.my_asset_mapper import (
        EsdlMyAssetMapper,
    )

Second, add one or more entries to ``conversion_dict_mappers``:

.. code-block:: python

    conversion_dict_mappers: dict[type, type[EsdlMapperAbstract]] = {
        ...
        esdl.MyEsdlAssetType: EsdlMyAssetMapper,
        ...
    }

The ``EsdlAssetMapper.to_entity`` method uses this dictionary to dispatch to the correct
mapper at runtime. A single mapper class may be registered for multiple ESDL types if they
share the same construction logic (see how ``EsdlAssetProducerMapper`` handles several
producer variants).

5. Test file placement and patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unit tests for the entity layer belong in ``unit_test/entities/``. Follow the pattern of
``test_heat_pump.py`` or ``test_production_cluster.py``:

- Construct the asset in ``setUp`` with representative port ids and setpoint values.
- Test ``set_setpoints`` with valid and invalid inputs.
- Mock ``self.solver_asset`` to isolate entity logic from the solver layer.
- Test ``write_to_output`` by calling it and inspecting ``self.outputs``.

Unit tests for the solver-layer class belong in ``unit_test/solver/network/assets/``.
Follow the pattern of ``test_production_asset.py`` or ``test_heat_transfer_asset.py``:

- Test that ``get_equations`` returns the correct number of ``EquationObject`` instances.
- Test boundary-condition setters by checking the ``prev_sol`` state after setting values.

Unit tests for the mapper belong in
``unit_test/adapters/transforms/esdl_asset_mappers/``.
Follow the pattern of ``test_esdl_asset_heat_pump_mapper.py``:

- Construct a mock ``EsdlAssetObject`` wrapping a representative PyESDL asset.
- Assert that ``to_entity`` returns an instance of the expected entity class.
- Assert that ESDL properties are correctly transferred to entity attributes.

Running and validating tests
----------------------------

After placing test files, verify end-to-end behavior by running the full unit test suite with
``python -m pytest`` from the repository root. If the asset is exercised by any existing ESDL
test-data files in ``testdata/``, run the relevant integration tests under
``unit_test/integration/`` as well. For new ESDL scenarios, add a minimal ``.esdl`` file to
``testdata/`` and write a corresponding integration test that asserts the simulation completes
without error and produces non-trivial output. See the existing integration tests for the
expected structure.

Cross-links
-----------

- Asset behavior and physics: :doc:`../physics/physics_main`
- Simulation orchestration and how assets are wired into the runtime: :doc:`simulation_contributor_flow`
- Test layout and test patterns: :doc:`testing`
