Adding an entity-layer asset for an existing solver asset
=========================================================

Purpose
-------

Use this guide when the equations you need already exist in a solver asset and you only
need a new entity asset: different setpoint handling, extra parameters, or extra output.
``GasHeater`` and ``ElecBoiler`` are the reference examples. Both subclass
``ProductionCluster``, reuse its ``HeatBoundary`` solver asset, and add an efficiency and a
fuel or electricity consumption output.

If no solver asset provides the equations you need, first add one with
:doc:`AddSolverLayerAssets` and then return to this guide. For asset physics, see
:doc:`../physics/physics_main`.

Relevant modules and files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 38 22 40

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``src/omotes_simulator_core/entities/assets/asset_abstract.py``
     - Entity base class
     - Declares the abstract ``set_setpoints``, ``write_to_output``, and ``postprocess``
       methods and the ``outputs`` structure.
   * - ``src/omotes_simulator_core/entities/assets/production_cluster.py``,
       ``gas_heater.py``, ``elec_boiler.py``
     - Reference implementation
     - Show a base entity asset and two subclasses that reuse its solver asset.
   * - ``src/omotes_simulator_core/entities/assets/asset_defaults.py``
     - Constants
     - ``PROPERTY_*`` output and setpoint keys and default values such as
       ``DEFAULT_GAS_ENERGY_CONTENT``.
   * - ``src/omotes_simulator_core/adapter/transforms/esdl_asset_mappers/producer_mapper.py``
     - ESDL asset mapper
     - ``EsdlAssetProducerMapper.to_entity`` chooses ``ElecBoiler``, ``GasHeater``, or
       ``ProductionCluster`` with ``isinstance`` checks on the ESDL asset.
   * - ``src/omotes_simulator_core/adapter/transforms/esdl_asset_mapper.py``
     - Mapper dispatch table
     - ``conversion_dict_mappers`` maps each ESDL class to a mapper class.
   * - ``src/omotes_simulator_core/adapter/transforms/string_to_esdl.py``
     - Asset labels
     - ``OmotesAssetLabels`` and ``StringEsdlAssetMapper`` define which ESDL classes
       ``EsdlObject.get_all_assets_of_type`` returns for a label.
   * - ``src/omotes_simulator_core/adapter/transforms/controller_mapper.py``
     - Controller creation
     - ``EsdlControllerMapper.to_entity`` creates asset controllers per label; an asset
       without a controller never receives setpoints.
   * - ``unit_test/entities/test_gas_heater.py``
     - Entity test example
     - Tests construction, parameter validation, and ``write_to_output`` with patched
       solver getters.
   * - ``unit_test/adapters/transforms/esdl_asset_mappers/test_esdl_asset_producer_mapper.py``
     - Mapper test example
     - Maps a producer from ``testdata/test1.esdl`` and checks name, ID, and ports.

Execution or extension flow
---------------------------

1. Choose the base class
~~~~~~~~~~~~~~~~~~~~~~~~

If an existing entity asset already handles the setpoints your asset receives, subclass it,
as ``GasHeater`` subclasses ``ProductionCluster``. You inherit the solver asset, setpoint
validation, convergence check, and output port choice.

Otherwise subclass ``AssetAbstract``, create the solver asset in ``__init__``, and assign it
to ``self.solver_asset``. You must then implement ``set_setpoints``, ``write_to_output``,
and ``postprocess``. Override ``get_state`` or ``is_converged`` when the defaults (an empty
dictionary and ``True``) do not fit.
:doc:`developer_navigation` lists which solver class each existing entity uses.

2. Write the entity class
~~~~~~~~~~~~~~~~~~~~~~~~~

Create a module in ``src/omotes_simulator_core/entities/assets/``. The following is
``GasHeater``, shortened:

.. code-block:: python

    class GasHeater(ProductionCluster):
        def __init__(
            self,
            asset_name: str,
            asset_id: str,
            port_ids: list[str],
            efficiency: float = 1.0,
        ) -> None:
            if efficiency == 0 or efficiency > 1.0:
                logger.warning(...)
                self.efficiency = 1.0
            else:
                self.efficiency = efficiency
            self.gas_energy_content = DEFAULT_GAS_ENERGY_CONTENT
            super().__init__(asset_name=asset_name, asset_id=asset_id, port_ids=port_ids)

        def get_gas_consumption(self) -> float:
            return abs(self.get_actual_heat_supplied()) / self.gas_energy_content / self.efficiency

        def write_to_output(self) -> None:
            output_dict_temp = {
                PROPERTY_HEAT_SUPPLY_SET_POINT: self.heat_demand_set_point,
                PROPERTY_HEAT_SUPPLIED: self.get_actual_heat_supplied(),
                PROPERTY_GAS_CONSUMPTION: self.get_gas_consumption(),
            }
            self.outputs[1][-1].update(output_dict_temp)

Follow the existing constructor convention: entity assets take ``asset_name``,
``asset_id``, and ``port_ids`` (``HeatPump`` uses ``connected_ports``) and pass them to
``AssetAbstract.__init__(asset_name, asset_id, connected_ports)``. Validate parameters in
the constructor and log a warning when you fall back to a default.

3. Add constants
~~~~~~~~~~~~~~~~

Add new output keys and defaults to ``asset_defaults.py``, as was done for
``PROPERTY_GAS_CONSUMPTION`` and ``DEFAULT_GAS_ENERGY_CONTENT``. See :doc:`AddOutputFormat`
for how output keys become ``DataFrame`` columns.

4. Map the ESDL asset to the entity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two options:

- **Branch in an existing mapper.** When the new entity is a variant of an existing one,
  add an ``isinstance`` branch to that mapper before the generic case, as
  ``EsdlAssetProducerMapper.to_entity`` does for ``esdl.ElectricBoiler`` and
  ``esdl.GasHeater``, and make sure the ESDL class is a key in ``conversion_dict_mappers``.
- **Add a new mapper.** Create a class derived from ``EsdlMapperAbstract`` in
  ``adapter/transforms/esdl_asset_mappers/`` with ``to_entity(esdl_asset)`` and a
  ``to_esdl`` that raises ``NotImplementedError``. Add the ESDL class and the mapper to
  ``conversion_dict_mappers``.

Read ESDL attributes in the mapper, for example ``esdl_asset.esdl_asset.efficiency`` or
``esdl_asset.get_property(esdl_property_name=..., default_value=...)``, and pass plain values
to the entity constructor.

5. Make sure the asset gets a controller
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``HeatNetwork.run_time_step`` only calls ``set_setpoints`` on assets whose ID is in the
controller output, so the asset also needs an asset controller:

- Check that the ESDL class is returned by ``EsdlObject.get_all_assets_of_type`` for some
  ``OmotesAssetLabels`` value. If not, add a label and add the class to
  ``StringEsdlAssetMapper.label_to_type_map``.
- Check that ``EsdlControllerMapper.to_entity`` creates a controller for that label. For
  ``GAS_HEATER`` and ``ELECTRIC_BOILER`` it adds ``ControllerProducerMapper`` results to the
  producer list. Add a similar list comprehension for a new label.

See :doc:`ControlExtension` when the asset needs a new kind of controller.

Implementation notes
--------------------

- Do not add the solver asset to the ``Network`` yourself.
  ``EsdlEnergySystemMapper._convert_assets`` calls ``network.add_existing_asset`` for each
  enabled entity's ``solver_asset``, and ``_create_junctions`` connects the solver assets
  according to the ESDL port connections.
- ``Network`` stores solver assets by name, and existing entity classes pass the asset name
  as the solver asset ``name``. ``add_existing_asset`` raises ``ValueError`` for a duplicate
  name.
- ``write_to_output`` runs after ``write_standard_output`` has appended one dictionary per
  port. Update ``self.outputs[port][-1]``; do not append and do not call
  ``write_standard_output`` yourself. ``ProductionCluster`` and its subclasses write to
  port 1.
- ``set_setpoints`` can run up to 20 times per timestep. Keep it free of cumulative side
  effects and put end-of-timestep state updates in ``postprocess``.
- ``ProductionCluster.set_setpoints`` raises ``ValueError`` when one of
  ``PROPERTY_TEMPERATURE_IN``, ``PROPERTY_TEMPERATURE_OUT``, ``PROPERTY_HEAT_DEMAND``, or
  ``PROPERTY_SET_PRESSURE`` is missing. Subclasses inherit this check.
- Entity classes do not import ``esdl``; the mapper translates ESDL data.

Testing and validation
----------------------

- **Entity test.** Add ``unit_test/entities/test_<asset>.py`` modelled on
  ``test_gas_heater.py``: test construction and parameter fallback, test derived values
  with ``patch.object`` on the entity or ``solver_asset`` getters, and test
  ``write_to_output`` by calling ``write_standard_output()`` first and asserting on
  ``outputs[port][-1]``.
- **Mapper test.** Add or extend a test in
  ``unit_test/adapters/transforms/esdl_asset_mappers/`` that loads an ESDL file from
  ``testdata/`` and checks the type and attributes of the mapped entity. ``testdata/``
  does not contain a ``GasHeater`` or ``ElectricBoiler`` yet, so a new ESDL type needs a new
  fixture.
- **Controller mapping.** Extend
  ``unit_test/adapters/transforms/controller_mappers/test_esdl_controller_mapper.py`` when
  you add a label or a controller list comprehension.
- **Full run.** Run a ``SimulationManager`` integration test on a fixture that contains the
  asset to check that it receives setpoints and produces output.

Run the full suite with ``ci/linux/test_unit.sh`` or ``ci\win32\test_unit.cmd``. See
:doc:`testing_strategy` for targeted runs.

Common pitfalls
---------------

- **Unregistered ESDL class.** ``EsdlAssetMapper.to_entity`` looks up
  ``type(esdl_asset)`` in ``conversion_dict_mappers`` and raises ``NotImplementedError``
  when it is missing. Subclasses of a registered ESDL class are not matched.
- **No controller.** Without a controller entry the asset is built and solved but keeps its
  constructor defaults; no error is raised.
- **Duplicate selection.** ``StringEsdlAssetMapper`` requires unique labels and types.
  Listing both a base ESDL class and its subclass under labels can select an asset twice.
- **Duplicated output rows.** Calling ``write_standard_output`` inside ``write_to_output``
  appends a second row per timestep.
- **String literals as keys.** Use ``PROPERTY_*`` constants from ``asset_defaults.py`` for
  setpoints and outputs.

Related documentation
---------------------

- :doc:`AddSolverLayerAssets` — when a new solver asset is needed.
- :doc:`AddOutputFormat` — adding output columns.
- :doc:`ControlExtension` — adding or changing controllers.
- :doc:`simulation_flow` — where entity assets are built and called.
- :doc:`testing_strategy` — test levels and commands.
- :doc:`../physics/physics_main` — asset physics.
- :doc:`api/omotes_simulator_core` — generated class and module reference.
