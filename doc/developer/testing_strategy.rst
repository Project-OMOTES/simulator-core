Testing strategy
================

Purpose
-------

This guide explains where tests live, how to run them, which test level to choose, and
what to check before submitting a change. Use it when you add a feature, fix a bug, or
restructure code. It does not cover physics derivations or user-facing behavior.

Relevant modules and files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``unit_test/adapters/``
     - Mapper tests
     - ``transforms/esdl_asset_mappers/`` tests one ESDL asset mapper per file,
       ``transforms/controller_mappers/`` tests controller mappers and
       ``EsdlControllerMapper``, ``transforms/test_esdl_graph_mapper.py`` tests graph
       creation, and ``utility/test_graph.py`` tests the graph utility.
   * - ``unit_test/transforms/``
     - ``EsdlEnergySystemMapper`` and port utilities
     - ``test_mapper.py`` tests ``EsdlEnergySystemMapper.to_entity`` and joint
       replacement; ``test_transform_utils.py`` tests port sorting helpers.
   * - ``unit_test/entities/``
     - Entity assets and asset controllers
     - One file per entity asset (for example ``test_pipe.py``, ``test_gas_heater.py``);
       ``controller/`` holds asset controller tests and ``test_controller_new_class.py``
       for ``NetworkController``.
   * - ``unit_test/solver/``
     - Solver assets, network, and matrix
     - ``network/assets/`` has one file per solver asset class; ``network/test_network.py``
       tests the solver graph; ``matrix/`` tests ``Matrix`` and ``EquationObject``.
   * - ``unit_test/simulation/``
     - Time loop
     - ``test_networksimulation.py`` tests ``NetworkSimulation``.
   * - ``unit_test/infrastructure/``
     - Orchestration and plotting
     - ``test_simulationmanager.py`` runs ``SimulationManager`` end to end.
   * - ``unit_test/integration/``
     - Multi-component scenarios
     - Physics checks at three entry levels; see `Integration test patterns`_.
   * - ``testdata/``
     - ESDL fixtures
     - Real ESDL files, such as ``test1.esdl`` and ``test_ates.esdl``, used by mapper,
       simulation, and integration tests.
   * - ``ci/linux/`` and ``ci/win32/``
     - Convenience scripts
     - ``test_unit``, ``lint``, ``typecheck``, ``format``, and ``check_formatting`` run
       the same checks as the pipeline.
   * - ``pyproject.toml``
     - Tool configuration
     - ``[tool.pytest.ini_options]`` adds coverage options with ``--cov-fail-under 90``;
       ``[tool.flake8]``, Black, and isort settings also live here.

Execution or extension flow
---------------------------

Set up the environment once with ``ci/linux/create_venv.sh`` or ``ci\win32\create_venv.cmd``.
These scripts create ``.venv`` and install the pinned runtime and development dependencies.
Alternatively, install the package in editable mode with its ``dev`` extra.

Run the full suite with ``ci/linux/test_unit.sh`` on Linux or ``ci\win32\test_unit.cmd`` on
Windows. Both scripts add ``src`` to ``PYTHONPATH`` and run
``pytest -p no:faulthandler unit_test/``. The full run includes the coverage check from
``pyproject.toml``.

For a single directory or file during development, call pytest directly and disable
coverage. Without ``--no-cov`` a partial run fails the 90% coverage threshold even when all
selected tests pass. The package must be importable, either through an editable install or
by adding ``src`` to ``PYTHONPATH`` as the scripts do:

.. code-block:: bash

    python -m pytest --no-cov -p no:faulthandler unit_test/entities/test_pipe.py

Before submitting, also run the lint, type check, and formatting scripts in the same
``ci`` folder (``lint``, ``typecheck``, ``check_formatting``). Use ``format`` to apply Black
and isort.

Implementation notes
--------------------

Unit tests use ``unittest.TestCase`` with ``setUp`` and one behavior per test method,
commented as Arrange, Act, and Assert. Follow the closest existing test file.

Entity asset tests
~~~~~~~~~~~~~~~~~~

Construct the entity asset directly with keyword arguments, as in
``unit_test/entities/test_pipe.py`` and ``unit_test/entities/test_gas_heater.py``. Replace
solver results with ``unittest.mock.patch.object`` on ``asset.solver_asset`` getters such as
``get_mass_flow_rate``, ``get_pressure``, and ``get_temperature``, so no solve is needed.

To test ``write_to_output``, call ``write_standard_output()`` first, as ``HeatNetwork``
does, and then assert on ``asset.outputs[port_index][-1]``. ``test_gas_heater.py`` shows
this sequence for the output port of a producer.

Solver asset tests
~~~~~~~~~~~~~~~~~~

Solver asset tests live in ``unit_test/solver/network/assets/``, one file per class (for
example ``test_solver_pipe.py``, ``test_heat_transfer_asset.py``). They call methods such as
``get_equations`` or individual equation helpers on a solver asset and check the returned
``EquationObject`` contents, without running ``Solver``.

Controller tests
~~~~~~~~~~~~~~~~

Asset controller tests live in ``unit_test/entities/controller/`` and construct the
controller directly. ``test_controller_new_class.py`` tests ``NetworkController`` with
``Mock(spec=ControllerNetwork)``, ``Mock(spec=ControllerConsumer)``, and
``Mock(spec=ControllerStorageAbstract)`` objects, so the tests fail when a mocked attribute
does not exist on the real class.

Mapper tests
~~~~~~~~~~~~

Mapper tests load a real ESDL file from ``testdata/`` with
``EsdlObject(pyesdl_from_file(...))``, select assets with
``esdl_object.get_all_assets_of_type(...)``, and call ``mapper.to_entity``.
``test_esdl_asset_producer_mapper.py`` checks the resulting entity's name, ID, and
connected ports against the ESDL asset. Add an ESDL fixture to ``testdata/`` when no
existing file contains the asset type you need.

Integration test patterns
~~~~~~~~~~~~~~~~~~~~~~~~~

Integration tests in ``unit_test/integration/`` enter the stack at one of three levels:

.. list-table::
   :header-rows: 1
   :widths: 20 45 35

   * - Level
     - Pattern
     - Examples
   * - Full run
     - ``SimulationManager(EsdlObject(pyesdl_from_file(path)), config)`` followed by
       ``execute(callback)``; assertions on the returned ``DataFrame``.
     - ``test_heat_physics.py``, ``test_pressure_physics.py``
   * - Network
     - ``HeatNetwork(EsdlEnergySystemMapper(esdl_object).to_entity)`` with a hand-written
       ``controller_input`` passed to ``run_time_step``; no controller.
     - ``test_ates_network.py``, ``test_communication_controller_network.py``
   * - Solver
     - A solver ``Network()`` built with ``add_existing_asset`` and ``connect_assets``,
       boundary values set on solver assets, then ``Solver(network).solve()``.
     - ``test_zero_flow_physics.py``, ``test_heat_transfer_asset.py``,
       ``test_ideal_heat_buffer.py``

A minimal full-run setup, based on ``test_heat_physics.py``:

.. code-block:: python

    esdl_file_path = str(Path(__file__).parent / ".." / ".." / "testdata" / "test1.esdl")
    config = SimulationConfiguration(
        simulation_id=uuid.uuid1(),
        name="test run",
        timestep=3600,
        start=datetime.strptime("2019-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S"),
        stop=datetime.strptime("2019-01-01T06:00:00", "%Y-%m-%dT%H:%M:%S"),
    )
    app = SimulationManager(EsdlObject(pyesdl_from_file(esdl_file_path)), config)
    result = app.execute(progress_calback=lambda progress, message: None)

Use the lowest level that exercises the behavior you changed. Solver-level tests isolate
equations; network-level tests check entity and solver coupling with fixed setpoints; full
runs check control and physics together.

Testing and validation
----------------------

Before submitting a change, check that:

- The full suite passes through ``ci/linux/test_unit.sh`` or ``ci\win32\test_unit.cmd``,
  including the 90% coverage threshold.
- ``lint``, ``typecheck``, and ``check_formatting`` in ``ci/linux/`` or ``ci/win32/``
  report no issues.
- Every new entity asset, solver asset, asset controller, and mapper has a unit test.
- An integration test exists when the change couples components in a new way, such as a
  new asset type in a network or a change to control logic.
- New ESDL fixtures are in ``testdata/`` with a descriptive name.
- The documentation builds without new warnings when you changed docstrings or pages under
  ``doc/``. Use ``doc/run_sphinx.sh`` on Linux or ``doc/run_sphinx.bat`` on Windows.

Common pitfalls
---------------

- Running a subset of tests without ``--no-cov`` and reading the coverage failure as a test
  failure.
- Asserting on ``outputs[port][-1]`` after ``write_to_output`` without calling
  ``write_standard_output`` first; the output list is then empty or holds the previous row.
- Using a bare ``Mock()`` for controllers or networks; use ``Mock(spec=...)`` so misspelled
  attributes fail the test.
- Writing a full-run integration test for a solver-only change; it is slower and harder to
  diagnose than a solver-level test.
- Testing an ESDL asset mapper with a hand-built mock asset when a ``testdata/`` file already
  contains that asset type.

Related documentation
---------------------

- :doc:`simulation_flow` — which call each test level enters.
- :doc:`developer_guides` — extension guides, each with test guidance.
- :doc:`ControlExtension` — tests for control changes.
- :doc:`documentation_with_ai_agents` — documentation build and review workflow.
