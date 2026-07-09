Adding an Entity-Layer Asset for an Existing Solver Asset
==========================================================

Purpose
-------

Use this guide when a suitable solver-layer asset already exists and you only need to add
an entity-layer class to expose it through the simulation — for example, adding a new variant
of an existing asset type that reuses the same physics equations.

If no suitable solver-layer asset exists, use :doc:`AddSolverAndEntityLayerAssets` instead,
which covers creating both layers from scratch.

This guide is for contributors working at the Python implementation level. For conceptual
asset behavior, consult :doc:`../physics/physics_main`.

Relevant Modules and Files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 38 22 40

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``src/omotes_simulator_core/entities/assets/asset_abstract.py``
     - Entity-layer base class
     - Defines the interface all entity-layer assets must implement:
       ``set_setpoints``, ``write_to_output``, ``get_state``.
   * - ``src/omotes_simulator_core/entities/assets/asset_defaults.py``
     - Output column constants
     - Defines string constants used as output dictionary keys. Add new constants here
       rather than using string literals in ``write_to_output``.
   * - ``src/omotes_simulator_core/adapter/transforms/esdl_asset_mappers/``
     - Per-asset ESDL mappers
     - One mapper file per asset type. Your new mapper reads ESDL properties and constructs
       the entity-layer asset.
   * - ``src/omotes_simulator_core/adapter/transforms/esdl_asset_mapper.py``
     - Mapper dispatch table
     - Maps ESDL asset types to mapper classes via ``conversion_dict_mappers``. Must be
       updated to register your new mapper.
   * - ``unit_test/entities/``
     - Entity-layer unit tests
     - Follow existing test patterns (e.g. ``test_heat_pump.py``) for the new class.
   * - ``unit_test/adapters/transforms/esdl_asset_mappers/``
     - Mapper unit tests
     - Verify that ESDL properties are correctly transferred to entity attributes.

Extension Flow
--------------

1. Create the entity-layer asset class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new file in ``src/omotes_simulator_core/entities/assets/``, for example
``my_asset_variant.py``.

Inherit from ``AssetAbstract`` and assign the existing solver-layer asset in ``__init__``:

.. code-block:: python

    from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
    from omotes_simulator_core.solver.network.assets.existing_solver_asset import ExistingSolverAsset

    class MyAssetVariant(AssetAbstract):
        asset_type = "my_asset_variant"
        number_of_con_points: int = 2  # adjust to match port count

        def __init__(self, asset_name: str, asset_id: str, connected_ports: list[str]) -> None:
            super().__init__(asset_name, asset_id, connected_ports)
            self.solver_asset = ExistingSolverAsset(
                name=asset_name,
                _id=asset_id,
            )
            self._register_solver_asset(self.solver_asset)

The following methods **must** be implemented:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Method
     - Responsibility
   * - ``set_setpoints(self, setpoints: dict)``
     - Accept and apply setpoints before each solver call. Raise ``KeyError`` if a required
       setpoint is missing.
   * - ``write_to_output(self)``
     - Append asset-specific quantities to ``self.outputs`` for the current timestep. Call
       ``self.write_standard_output()`` first.

Use ``get_state(self) -> dict[str, float]`` to expose internal state the controller needs.
Study ``ProductionCluster`` or ``HeatPump`` for representative patterns before writing new
methods.

2. Create the ESDL mapper
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new file in
``src/omotes_simulator_core/adapter/transforms/esdl_asset_mappers/``, for example
``my_asset_variant_mapper.py``.

.. code-block:: python

    from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract
    from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
    from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
    from omotes_simulator_core.entities.assets.my_asset_variant import MyAssetVariant


    class EsdlMyAssetVariantMapper(EsdlMapperAbstract):

        def to_esdl(self, entity: MyAssetVariant) -> EsdlAssetObject:
            raise NotImplementedError("EsdlMyAssetVariantMapper.to_esdl()")

        def to_entity(self, esdl_asset: EsdlAssetObject) -> AssetAbstract:
            return MyAssetVariant(
                asset_name=esdl_asset.esdl_asset.name,
                asset_id=esdl_asset.esdl_asset.id,
                connected_ports=esdl_asset.get_port_ids(),
            )

Use ``esdl_asset.get_property(name, default)`` to read optional ESDL attributes safely.

3. Register the mapper
~~~~~~~~~~~~~~~~~~~~~~~

Open ``src/omotes_simulator_core/adapter/transforms/esdl_asset_mapper.py`` and add:

.. code-block:: python

    from omotes_simulator_core.adapter.transforms.esdl_asset_mappers.my_asset_variant_mapper import (
        EsdlMyAssetVariantMapper,
    )

Then add an entry to ``conversion_dict_mappers``:

.. code-block:: python

    conversion_dict_mappers: dict[type, type[EsdlMapperAbstract]] = {
        ...
        esdl.MyEsdlAssetVariantType: EsdlMyAssetVariantMapper,
        ...
    }

Testing and Validation
----------------------

Unit tests for the entity layer belong in ``unit_test/entities/``. Follow the pattern of
``test_heat_pump.py`` or ``test_production_cluster.py``:

- Construct the asset in ``setUp`` with representative port IDs and setpoint values.
- Test ``set_setpoints`` with valid inputs and missing required keys.
- Mock ``self.solver_asset`` to isolate entity logic from the solver layer.
- Test ``write_to_output`` by calling it and asserting the expected keys are present in
  ``self.outputs``.

Unit tests for the mapper belong in
``unit_test/adapters/transforms/esdl_asset_mappers/``. Follow the pattern of
``test_esdl_asset_heat_pump_mapper.py``:

- Construct a mock ``EsdlAssetObject`` wrapping a representative PyESDL asset.
- Assert that ``to_entity`` returns an instance of ``MyAssetVariant``.
- Assert that ESDL properties are correctly transferred to entity attributes.

Run the full test suite from the repository root:

.. code-block:: console

    python -m pytest unit_test/

Common Pitfalls
---------------

- **Referencing a solver asset that does not register itself with ``Network``.** Call
  ``self._register_solver_asset(self.solver_asset)`` in ``__init__``; without this the
  solver graph will not include the asset.
- **Not registering the mapper.** New asset types that are not in
  ``conversion_dict_mappers`` will silently produce no asset in the runtime network.
  Always register and always add a mapper unit test.
- **Using string literals as output keys.** Define all output column names as constants in
  ``asset_defaults.py`` and import them. String literals that differ by one character
  produce silently wrong output.
- **Confusing entity state with solver state.** The entity layer owns per-timestep state
  for control and output; the solver layer owns the matrix unknowns. Do not read solver
  unknowns directly in ``write_to_output`` — read them through ``self.solver_asset``
  properties that the solver layer already exposes.

Related Documentation
---------------------

- :doc:`AddSolverAndEntityLayerAssets` — full workflow when no solver asset exists yet.
- :doc:`simulation_flow` — execution flow showing where entity assets are constructed and
  how they interact with the solver.
- :doc:`testing_strategy` — test layout and patterns for entity-layer tests.
- :doc:`../physics/physics_main` — conceptual asset behavior and governing relations.
- :doc:`api/omotes_simulator_core` — generated API reference for class details.
