Testing Strategy
================

Purpose
-------

This guide helps contributors understand where tests live, how to run the test suite, what
patterns to follow when writing new tests, and what to check before submitting a change.

Use this page when you are adding a feature, fixing a bug, or making any structural change that
requires new or modified tests. It is implementation-oriented and assumes you can already navigate
the repository. It does not cover physics derivations or user-facing behavior.

Test Layout
-----------

All tests live under ``unit_test/``. The directory is flat at the top level; each subdirectory
targets a distinct layer or cross-cutting concern.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Subdirectory
     - What it covers
   * - ``unit_test/adapters/``
     - ESDL-to-entity mapping: ``EsdlGraphMapper``, controller mappers, and ESDL asset mappers.
       Verifies that ESDL graph topology is translated correctly to internal objects.
   * - ``unit_test/entities/``
     - Entity-layer asset classes (``Pipe``, ``HeatPump``, ``Ates``, etc.) and all
       asset-level controller classes (``ControllerProducer``, ``ControllerConsumer``, etc.).
       Each asset and controller class has its own test module.
   * - ``unit_test/infrastructure/``
     - ``SimulationManager`` orchestration and plotting utilities. Tests here cover how
       ``SimulationManager`` wires ESDL input to ``HeatNetwork`` and ``NetworkController``.
   * - ``unit_test/integration/``
     - Cross-component end-to-end scenarios run through ``SimulationManager`` against real ESDL
       files from ``testdata/``. Covers heat physics, pressure physics, zero-flow conditions,
       heat transfer assets, and ideal heat buffers across full simulation runs.
   * - ``unit_test/simulation/``
     - ``NetworkSimulation`` time-step orchestration. Verifies the simulation loop, controller
       update sequencing, and convergence retry logic in isolation.
   * - ``unit_test/solver/``
     - Low-level solver components: solver-layer asset classes (``BaseAsset``, ``SolverPipe``,
       ``ProductionAsset``, etc.), the network matrix builder, and solver utility functions.
   * - ``unit_test/transforms/``
     - Data transformation utilities: ESDL-to-dataframe mapper and transform utility helpers.

Running Tests
-------------

Install the development dependencies before running tests::

    pip install -e ".[dev]"

Run the full test suite from the repository root:

.. code-block:: bash

    python -m pytest unit_test/

Because the previous step installs the package in editable mode, no manual ``PYTHONPATH``
setup is required on any platform. Add ``-p no:faulthandler`` to suppress low-level crash
reporting that can produce spurious output when the solver reaches certain numerical states.

To run only a single subdirectory during development::

    python -m pytest unit_test/entities/

To run a single test file::

    python -m pytest unit_test/entities/test_pipe.py

Unit Test Patterns
------------------

Asset unit tests
~~~~~~~~~~~~~~~~

Unit tests for entity-layer assets live in ``unit_test/entities/``. The pattern follows the
standard ``unittest.TestCase`` structure used throughout the repository:

- ``setUp`` constructs the asset with representative parameter values.
- Individual test methods verify one behavior each, using the ``Arrange / Act / Assert``
  sequence.
- Solver interactions are replaced with ``unittest.mock.patch`` or ``Mock`` objects so the
  entity layer can be tested independently of the solver.

A concrete example is ``unit_test/entities/test_pipe.py``:

.. code-block:: python

    class PipeTest(unittest.TestCase):
        def setUp(self) -> None:
            self.pipe = Pipe(
                asset_name="pipe",
                asset_id="pipe_id",
                port_ids=["test1", "test2"],
                length=5,
                inner_diameter=1,
                roughness=0.001,
                alpha_value=0.8,
                minor_loss_coefficient=0.0,
                external_temperature=293.15,
                qheat_external=0.0,
            )

        def test_pipe_create(self) -> None:
            # Act and Assert
            pipe = Pipe(...)
            self.assertIsInstance(pipe, Pipe)

When adding a new asset:

- Create ``unit_test/entities/test_<asset_name>.py`` mirroring the structure of
  ``unit_test/entities/test_pipe.py`` or the closest existing asset test.
- Test construction with valid parameters and any required defaults.
- Test that output properties return expected types or raise appropriate errors when the
  asset has not yet been solved.
- Test any asset-specific logic such as clamping, bypass conditions, or state transitions.

Solver-layer asset tests live in ``unit_test/solver/network/assets/``. Each file targets one
solver asset class (for example ``test_solver_pipe.py``, ``test_production_asset.py``). These
tests verify that ``get_equations()`` returns the expected matrix contributions for given inputs,
without running the full nonlinear solver.

Controller unit tests
~~~~~~~~~~~~~~~~~~~~~

Controller tests live in ``unit_test/entities/controller/``. See
``unit_test/entities/controller/test_controller_new_class.py`` for a worked example that
exercises ``NetworkController`` with mock ``ControllerNetwork`` instances. Use
``Mock(spec=<class>)`` to constrain mocks to the real interface.

When adding a new controller class:

- Create ``unit_test/entities/controller/test_controller_<role>.py``.
- Use ``Mock(spec=ControllerNetwork)`` for the network argument.
- Call ``update_setpoints`` and assert that the returned dict contains the expected keys and
  value types.
- Test edge cases such as zero demand, empty subnetworks, or profile boundaries.

Adapter tests
~~~~~~~~~~~~~

Mapper tests live in ``unit_test/adapters/``. The main file is
``unit_test/adapters/test_esdl_graph_mapper.py``. Mapper tests verify that a known ESDL
structure (supplied inline or from a small fixture) maps to the expected internal graph
topology. Use real ESDL objects rather than mocks where construction is straightforward; use
mocks only for external dependencies such as file loaders.

Integration Test Patterns
-------------------------

Integration tests live in ``unit_test/integration/``. Each file runs a complete simulation
through ``SimulationManager`` using a real ESDL file from ``testdata/``, then asserts on
output values such as supply temperatures, mass flow rates, pressures, or heat transfer
quantities.

When to add an integration test:

- A new asset or controller class introduces cross-component coupling that unit tests cannot
  exercise in isolation (for example, a new asset type that affects network-level pressure
  balance).
- A bug fix addresses emergent behavior that only manifests across multiple layers (entity,
  solver, controller).
- A new ESDL configuration produces a topology that no existing integration test covers.

The general pattern (taken from ``unit_test/integration/test_heat_physics.py``) is:

.. code-block:: python

    class HeatDemandTest(unittest.TestCase):
        def setUp(self) -> None:
            esdl_file_path = str(
                Path(__file__).parent / ".." / ".." / "testdata" / "test1.esdl"
            )
            esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
            self.controller = EsdlControllerMapper().to_entity(esdl_object)
            config = SimulationConfiguration(
                simulation_id=uuid.uuid1(),
                name="test run",
                timestep=3600,
                ...
            )
            manager = SimulationManager(esdl_object, self.controller, config)
            self.output = manager.execute()

        def test_supply_temperature(self) -> None:
            # Assert on self.output values

Integration tests are slower than unit tests because they run the full solver loop. Keep
individual integration test files focused on one ESDL topology. Add a new ESDL file to
``testdata/`` if no existing file exercises the required network configuration.

Testing Checklist
-----------------

Before submitting a change, verify the following:

- All existing tests pass: ``python -m pytest unit_test/``
- A unit test exists for every new entity-layer asset class.
- A unit test exists for every new solver-layer asset class.
- A unit test exists for every new controller class or subclass.
- A unit test exists for every new mapper or transform.
- An integration test has been added if the change introduces cross-component coupling.
- No test imports from a private module interface (i.e., ``_private_method``).
- Mocks use ``Mock(spec=<class>)`` to prevent silent attribute errors.
- New ESDL test fixtures are placed in ``testdata/`` with a descriptive name.
- The documentation build passes: ``python -m sphinx -b html doc doc/_build/html``.

Related Documentation
---------------------

- :doc:`simulation_contributor_flow` — traces the full orchestration path from entrypoint to
  solver and identifies which tests correspond to each orchestration layer.
- :doc:`add_new_asset` — step-by-step workflow for adding a new asset; includes test file
  placement and what to test at each implementation step.
- :doc:`control_extension` — contributor guide for adding or modifying controller classes,
  including the corresponding test patterns for controller unit tests.
