Asset reference
===============

Purpose
-------

This page is a curated overview of the asset layer: the ``AssetAbstract`` methods that
every entity asset follows, how entity assets pair with solver assets, how they are created
from ESDL, and how the rest of the code uses them. It is meant for contributors who add or
change an asset, or who need to understand why an asset receives certain setpoints or
writes certain output.

For the physics of each asset, read :doc:`../physics/physics_main`. For step-by-step guides,
read :doc:`AddEntityLayerAsset` and :doc:`AddSolverLayerAssets`. For the full list
of methods, use the generated API reference (:doc:`api/omotes_simulator_core`).

Relevant modules and files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``entities/assets/asset_abstract.py``
     - ``AssetAbstract``: base class for all entity assets.
     - Defines the methods ``HeatNetwork`` calls on every asset.
   * - ``entities/assets/``
     - Concrete entity assets: ``ProductionCluster``, ``GasHeater``, ``ElecBoiler``,
       ``AirToWaterHeatPump``, ``DemandCluster``, ``Pipe``, ``HeatPump``, ``HeatExchanger``,
       ``AtesCluster``, ``IdealHeatStorage``, plus ``Junction``.
     - Translate setpoints into solver asset settings and collect output.
   * - ``entities/assets/asset_defaults.py``
     - Default values and property name constants.
     - Shared setpoint keys and fallback values used by assets and mappers.
   * - ``entities/assets/esdl_asset_object.py``
     - ``EsdlAssetObject``: wrapper around one ESDL asset.
     - The input every asset mapper reads properties and port IDs from.
   * - ``adapter/transforms/esdl_asset_mapper.py``
     - ``EsdlAssetMapper``: dictionary from ESDL type to asset mapper.
     - The registration point for a new ESDL asset type.
   * - ``adapter/transforms/esdl_asset_mappers/``
     - One mapper per asset family.
     - Reads ESDL attributes and creates the entity asset.
   * - ``solver/network/assets/``
     - Solver assets.
     - The equations behind each entity asset; see :doc:`solver_reference`.

Execution or extension flow
---------------------------

Entity and solver pairing
~~~~~~~~~~~~~~~~~~~~~~~~~

Every entity asset creates exactly one solver asset in its constructor and stores it as
``solver_asset``. The current pairs are:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Entity asset
     - Solver asset
   * - ``ProductionCluster``, ``GasHeater``, ``ElecBoiler``, ``AirToWaterHeatPump``
     - ``HeatBoundary``
   * - ``DemandCluster``, ``AtesCluster``
     - ``HeatBoundary``
   * - ``Pipe``
     - ``SolverPipe``
   * - ``HeatPump``, ``HeatExchanger``
     - ``HeatTransferAsset``
   * - ``IdealHeatStorage``
     - ``HeatBufferAsset``

``Junction`` is not an ``AssetAbstract``; it wraps a solver ``Node``.

Creation from ESDL
~~~~~~~~~~~~~~~~~~

1. ``EsdlEnergySystemMapper`` wraps each enabled ESDL asset in an ``EsdlAssetObject``.
2. ``EsdlAssetMapper.to_entity`` looks up the exact ESDL type in
   ``conversion_dict_mappers`` and raises ``NotImplementedError`` if it is missing.
3. The selected mapper creates the entity asset. Some mappers choose between classes:
   the producer mapper creates ``GasHeater`` or ``ElecBoiler`` for those ESDL types, and
   the heat pump mapper creates ``HeatPump`` for four ports or ``AirToWaterHeatPump`` for
   two ports.
4. The solver asset is registered in the solver ``Network``; see
   :doc:`network_reference`.

Per-timestep calls
~~~~~~~~~~~~~~~~~~

``HeatNetwork`` calls these ``AssetAbstract`` methods:

- ``set_time_step``, ``set_time`` (defaults store the values) and ``set_setpoints``
  (abstract), before every solve, but only for assets whose ID is a key in the controller
  output.
- ``is_converged`` (default ``True``) after every solve.
- ``postprocess`` (abstract) and then ``write_to_output`` (abstract), once per time step
  after the convergence loop.
- ``get_timeseries`` at the end of the run, to collect the output columns keyed by
  ``(port_id, property)``.

``NetworkController`` calls ``get_state`` (default empty) before computing setpoints.

Implementation notes
--------------------

- Entity assets own the conversion from setpoints to solver values. The solver asset
  should not read setpoints or ESDL data.
- ``set_setpoints`` usually checks that all required keys are present and raises an error
  otherwise. Keep the keys aligned with the controller; see :doc:`controller_reference`.
- ``write_standard_output`` writes mass flow, pressure, temperature and volume flow per
  port. Call it from ``write_to_output`` and add asset-specific values afterwards; see
  :doc:`AddOutputFormat`.
- Override ``is_converged`` when the asset changes solver settings based on the solved
  state. ``ProductionCluster``, ``DemandCluster``, ``AtesCluster`` and
  ``IdealHeatStorage`` do this.
- ``AssetAbstract.number_of_con_points`` is 2. Assets with a different number of ports
  must set it; the network mapper uses it to connect ports.
- ``AirToWaterHeatPump`` extends ``ProductionCluster`` and replaces its solver asset with a
  ``HeatBoundary``. The solver class ``AirToWaterHeatPumpAsset`` exists but is not used by
  the entity layer.
- ESDL ``HeatExchange`` is mapped by the heat pump mapper. ``HeatExchanger`` and its mapper
  exist but are not registered in ``conversion_dict_mappers``.

Testing and validation
----------------------

- ``unit_test/entities/`` contains one test file per entity asset, for example
  ``test_pipe.py``, ``test_production_cluster.py``, ``test_gas_heater.py`` and
  ``test_ideal_buffer.py``.
- ``unit_test/adapters/transforms/esdl_asset_mappers/`` covers the asset mappers.
- ``unit_test/integration/test_heat_transfer_asset.py``, ``test_ideal_heat_buffer.py`` and
  ``test_ates_network.py`` check assets inside a solved network.

See :doc:`testing_strategy` for commands and test patterns.

Common pitfalls
---------------

- Forgetting to register a new ESDL type in ``conversion_dict_mappers``. Lookup uses the
  exact type, so subclasses are not matched.
- Putting physics in the entity asset instead of the solver asset, or control logic in
  the solver asset.
- Writing output without ``write_standard_output``, which leaves the standard columns
  missing.
- Assuming an asset receives setpoints every time step; it only does when the controller
  returns its ID.
- Documenting physics on this page; that belongs in the physics section.

Related documentation
---------------------

- :doc:`AddEntityLayerAsset` and :doc:`AddSolverLayerAssets` — guides for new entity and
  solver assets.
- :doc:`AddOutputFormat` — guide for output columns.
- :doc:`architecture` — the two-layer asset model.
- :doc:`network_reference` — how assets are connected.
- :doc:`solver_reference` — solver assets and equations.
- :doc:`controller_reference` — where setpoints come from.
- :doc:`../physics/physics_main` — physics per asset.

API reference
-------------

.. toctree::
   :maxdepth: 1

   ../assets/asset_abstract_asset
   ../assets/asset_defaults_asset
   ../assets/asset_utils_asset
   ../assets/esdl_asset_object_asset
   ../assets/producer_asset
   ../assets/air_to_water_heat_pump_asset
   ../assets/consumer_asset
   ../assets/pipe_asset
   ../assets/heat_pump_asset
   ../assets/heat_exchanger_asset
   ../assets/ates_asset
   ../assets/ideal_heat_storage_asset
   ../assets/junction_asset
   ../assets/pyjnius_loader_asset
