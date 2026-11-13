Developer navigation
====================

Purpose
-------

This page is a map of the OMOTES.SIMULATOR_CORE repository for contributors. It lists the
packages under ``src/omotes_simulator_core``, what each one is responsible for, and where
to start reading for common tasks. Use it before opening the generated API reference: the
API pages tell you what a class contains, this page tells you which class to look at.

For how the packages depend on each other, see :doc:`architecture`. For the per-timestep
call sequence, see :doc:`simulation_flow`. For the responsibilities and interfaces of each
subsystem, see the curated reference pages :doc:`network_reference`,
:doc:`controller_reference`, :doc:`solver_reference` and :doc:`asset_reference`.

Relevant modules and files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 34 26 40

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``infrastructure/app.py``, ``__main__.py``
     - Command-line entrypoint
     - ``run()`` builds a ``SimulationConfiguration``, loads the ESDL file with
       ``pyesdl_from_file`` (``infrastructure/utils.py``), and calls
       ``SimulationManager.execute``.
   * - ``infrastructure/simulation_manager.py``
     - Run orchestration
     - ``SimulationManager`` creates ``HeatNetwork``, ``NetworkController``, and
       ``NetworkSimulation`` and returns the result ``DataFrame``.
   * - ``infrastructure/plotting.py``, ``infrastructure/profiling.py``
     - Debugging utilities
     - Map plotting and profiling helpers; not part of the simulation path.
   * - ``adapter/transforms/mappers.py``
     - ESDL-to-network mapper
     - ``EsdlEnergySystemMapper.to_entity`` converts every enabled ESDL asset, registers
       its solver asset in ``Network``, and connects assets through junctions.
   * - ``adapter/transforms/esdl_asset_mapper.py`` and ``esdl_asset_mappers/``
     - ESDL-to-asset dispatch
     - ``conversion_dict_mappers`` maps ESDL classes to per-asset mappers such as
       ``EsdlAssetProducerMapper``.
   * - ``adapter/transforms/controller_mapper.py`` and ``controller_mappers/``
     - ESDL-to-controller mapping
     - ``EsdlControllerMapper.to_entity`` builds asset controllers per
       ``OmotesAssetLabels`` label, splits them into ``ControllerNetwork`` objects, and
       returns a ``NetworkController``.
   * - ``adapter/transforms/string_to_esdl.py``
     - Asset labels
     - ``OmotesAssetLabels`` and ``StringEsdlAssetMapper`` define which ESDL classes are
       returned by ``EsdlObject.get_all_assets_of_type``.
   * - ``adapter/transforms/esdl_graph_mapper.py``, ``adapter/utility/graph.py``
     - Connectivity graph
     - Used by ``EsdlControllerMapper`` to find hydraulically connected sub-networks.
   * - ``entities/esdl_object.py``, ``entities/assets/esdl_asset_object.py``
     - ESDL wrappers
     - ``EsdlObject`` and ``EsdlAssetObject`` give mappers access to assets, ports,
       properties, profiles, and temperatures.
   * - ``entities/assets/``
     - Entity-layer assets
     - One class per asset type (``ProductionCluster``, ``GasHeater``, ``ElecBoiler``,
       ``DemandCluster``, ``Pipe``, ``HeatPump``, ``HeatExchanger``, ``AtesCluster``,
       ``IdealHeatStorage``, ``AirToWaterHeatPump``), all derived from ``AssetAbstract``.
       Output keys and defaults live in ``asset_defaults.py``.
   * - ``entities/assets/controller/``
     - Asset controllers
     - ``ControllerProducer``, ``ControllerConsumer``, ``ControllerAtesStorage``,
       ``ControllerIdealHeatStorage``, ``ControllerHeatTransferAsset``, and
       ``ControllerNetwork``, plus profile resampling in ``profile_interpolation.py``.
   * - ``entities/heat_network.py``
     - Runtime network container
     - ``HeatNetwork`` owns the entity assets, the solver ``Network``, and the
       ``Solver``.
   * - ``entities/network_controller.py``, ``entities/network_controller_abstract.py``
     - Network-level control
     - ``NetworkController`` computes the setpoint dictionary each timestep;
       ``NetworkControllerAbstract`` declares ``update_setpoints``.
   * - ``simulation/networksimulation.py``
     - Time loop
     - ``NetworkSimulation.run`` drives the controller and ``HeatNetwork`` per timestep.
   * - ``simulation/mappers/mappers.py``
     - Mapper base class
     - ``EsdlMapperAbstract`` declares ``to_entity`` and ``to_esdl`` for all mappers.
   * - ``solver/solver.py``
     - Nonlinear solve loop
     - ``Solver.solve`` assembles equations from all solver assets and nodes and iterates
       the ``Matrix`` until convergence.
   * - ``solver/network/network.py``, ``solver/network/assets/``
     - Solver graph and solver assets
     - ``Network`` holds ``BaseAsset`` and ``Node`` objects; solver assets such as
       ``HeatBoundary``, ``SolverPipe``, ``HeatTransferAsset``, and ``HeatBufferAsset``
       implement ``get_equations``.
   * - ``solver/matrix/``
     - Linear system
     - ``Matrix``, ``EquationObject``, and ``index_core_quantity`` define unknown indexing
       and equation assembly.
   * - ``solver/utils/fluid_properties.py``, ``solver/solver_constants.py``
     - Shared physical constants
     - ``fluid_props`` provides temperature-dependent water properties used by both
       layers; ``MASSFLOW_ZERO_LIMIT`` is used by solver assets.
   * - ``unit_test/``, ``testdata/``
     - Tests and ESDL fixtures
     - Test folders mirror the source packages; ``testdata/`` holds the ESDL files used
       by mapper and integration tests.

Paths in the first column are relative to ``src/omotes_simulator_core`` unless they start
with ``unit_test/`` or ``testdata/``.

Extension flow
--------------

Use the following table to find the first file to open for a given task and the guide that
covers the full workflow.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Task
     - Start in
     - Guide
   * - Support a new ESDL type with existing physics
     - ``entities/assets/production_cluster.py`` and ``gas_heater.py``
     - :doc:`AddEntityLayerAsset`
   * - Add a new physical asset type
     - ``solver/network/assets/base_asset.py`` and ``solver/network/assets/fall_type.py``
     - :doc:`AddSolverLayerAssets`, then :doc:`AddEntityLayerAsset`
   * - Change dispatch or add a controlled asset role
     - ``entities/network_controller.py`` and
       ``entities/assets/controller/controller_network.py``
     - :doc:`ControlExtension`
   * - Add an output column
     - ``entities/assets/asset_defaults.py`` and the asset's ``write_to_output``
     - :doc:`AddOutputFormat`
   * - Change the time loop or convergence retries
     - ``simulation/networksimulation.py``
     - :doc:`simulation_flow`
   * - Change equation assembly or solver iteration
     - ``solver/solver.py`` and ``solver/matrix/matrix.py``
     - :doc:`solver_reference`
   * - Change how the network is built from ESDL
     - ``adapter/transforms/mappers.py`` and ``solver/network/network.py``
     - :doc:`network_reference`

Implementation notes
--------------------

Entity-layer and solver-layer files use different names for the same asset. The entity
class creates its solver asset in ``__init__`` and stores it as ``self.solver_asset``:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Entity class (``entities/assets/``)
     - Solver class (``solver/network/assets/``)
   * - ``ProductionCluster``, ``GasHeater``, ``ElecBoiler``, ``AirToWaterHeatPump``,
       ``DemandCluster``, ``AtesCluster``
     - ``HeatBoundary`` (``production_asset.py``)
   * - ``Pipe``
     - ``SolverPipe`` (``solver_pipe.py``)
   * - ``HeatPump``, ``HeatExchanger``
     - ``HeatTransferAsset`` (``heat_transfer_asset.py``)
   * - ``IdealHeatStorage``
     - ``HeatBufferAsset`` (``buffer_asset.py``)
   * - ``Junction`` (not an ``AssetAbstract``)
     - ``Node`` (``node.py``), created by ``Network.connect_assets``

Mapper names also differ per side: ESDL asset mappers are named ``EsdlAsset*Mapper`` (for
example ``EsdlAssetProducerMapper``; ``EsdlIdealHeatStorageMapper`` is the exception),
controller mappers are named ``Controller*Mapper`` (for example
``ControllerProducerMapper``). Both derive from ``EsdlMapperAbstract``.

Testing and validation
----------------------

The test tree mirrors the source tree with two naming differences: adapter tests live in
``unit_test/adapters/`` (plural), and tests for ``adapter/transforms/mappers.py`` and
``transform_utils.py`` live in ``unit_test/transforms/``. Integration tests live in
``unit_test/integration/``. See :doc:`testing_strategy` for test patterns and commands.

Common pitfalls
---------------

- Searching only ``entities/assets/`` for physics: equations live in
  ``solver/network/assets/``; the entity class only translates setpoints and output.
- Looking for a dedicated mapper for every ESDL class: ``EsdlAssetProducerMapper`` handles
  several producer types, and ``EsdlAssetHeatPumpMapper`` handles both ``esdl.HeatPump`` and
  ``esdl.HeatExchange`` (four ports give ``HeatPump``, two ports give
  ``AirToWaterHeatPump``). ``HeatExchanger`` and ``EsdlAssetHeatExchangerMapper`` exist but
  are not registered in ``conversion_dict_mappers``. Check that dictionary first.
- Treating ``adapter/presentation/`` as an output layer: it currently contains only an
  ``__init__.py``. Output is assembled by ``HeatNetwork.gather_output``.
- Editing files under ``doc/developer/api/``: they are regenerated on every build.

Related documentation
---------------------

- :doc:`architecture` — layering, dependency direction, and the two-layer asset model.
- :doc:`network_reference`, :doc:`controller_reference`, :doc:`solver_reference` and
  :doc:`asset_reference` — curated per-subsystem reference pages.
- :doc:`simulation_flow` — per-timestep execution flow.
- :doc:`testing_strategy` — test layout and commands.
- :doc:`developer_guides` — extension how-to guides.
- :doc:`../network/network_main` — conceptual description of the network representation.
- :doc:`api/omotes_simulator_core` — generated class and module reference.
