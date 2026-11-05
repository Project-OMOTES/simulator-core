Adding a new output format
==========================

Purpose
-------

Use this guide when you want the simulator to report more results: a new computed column
for an existing asset, columns for a new asset, or a change in how the collected output is
assembled. It is written for contributors who can navigate the repository and run the unit
tests. For the physical meaning of the quantities, see :doc:`../physics/physics_main`.

The simulator has one output format: ``SimulationManager.execute`` returns a single
``pandas.DataFrame``. There is no pluggable writer. Output is built in three layers:
each entity asset appends values per timestep, ``HeatNetwork`` concatenates the asset
timeseries, and ``NetworkSimulation`` and ``SimulationManager`` pass the result on. New
output therefore starts in the entity layer and reaches the result without changes to the
other layers. Writing the ``DataFrame`` to a file or another format is up to the caller of
``SimulationManager.execute``.

Relevant modules and files
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 25 35

   * - File or Module
     - Role
     - Why it matters for this topic
   * - ``src/omotes_simulator_core/entities/assets/asset_abstract.py``
     - Abstract base class for all entity-layer assets
     - Defines ``write_standard_output`` (standard columns) and the abstract
       ``write_to_output`` (asset-specific columns); all output columns are written here
   * - ``src/omotes_simulator_core/entities/assets/asset_defaults.py``
     - Named property-key constants
     - By convention every column name is a constant here, so the writing side and any
       code reading the ``DataFrame`` use the same string
   * - ``src/omotes_simulator_core/entities/assets/pipe.py``
     - Concrete asset — pipe
     - Practical reference implementation of ``write_to_output`` with multiple columns
       and per-port output
   * - ``src/omotes_simulator_core/entities/assets/gas_heater.py``
     - Concrete asset — gas heater
     - Single-port pattern: ``GasHeater.write_to_output`` adds the set point, supplied heat,
       and ``PROPERTY_GAS_CONSUMPTION`` to ``outputs[1][-1]``
   * - ``src/omotes_simulator_core/entities/heat_network.py``
     - Network container
     - ``store_output`` calls ``write_standard_output`` and then ``write_to_output`` on every
       asset; ``gather_output`` concatenates ``get_timeseries`` of all assets
   * - ``src/omotes_simulator_core/simulation/networksimulation.py``
     - Simulation orchestrator
     - Calls ``post_process_assets`` and then ``store_output`` once per timestep, after the
       convergence loop; ``gather_output`` returns the network output
   * - ``src/omotes_simulator_core/infrastructure/simulation_manager.py``
     - Top-level entry point
     - ``execute`` returns ``worker.gather_output()``
   * - ``unit_test/entities/test_pipe.py``, ``test_gas_heater.py``
     - Unit tests for asset output
     - Reference pattern: patch the solver asset, call ``write_standard_output`` and
       ``write_to_output``, assert on ``outputs[i][-1]``
   * - ``unit_test/simulation/test_networksimulation.py``
     - Simulation test
     - Checks that ``gather_output`` has one row per timestep after ``run``

Execution or extension flow
---------------------------

How output is produced
~~~~~~~~~~~~~~~~~~~~~~

For every timestep, after the convergence loop, ``NetworkSimulation.run``:

1. Calls ``HeatNetwork.post_process_assets``, which calls ``postprocess`` on every asset.
   ``IdealHeatStorage`` updates its fill level and temperatures here.
2. Calls ``HeatNetwork.store_output``. For every asset ``write_standard_output`` appends a new
   dictionary per port with mass flow, pressure, temperature, and volume flow, and
   ``write_to_output`` adds asset-specific keys to those dictionaries.

After the run, ``AssetAbstract.get_timeseries`` turns each asset's ``outputs`` into a
``DataFrame`` with ``(port_id, property_name)`` column tuples, and
``HeatNetwork.gather_output`` concatenates them along the column axis. The row index is a
plain range index with one row per timestep.

Adding output columns
~~~~~~~~~~~~~~~~~~~~~

The steps below add one or more columns to an existing or new asset. Steps 1–3 are always
required. Step 4 applies only when you add a new asset.

1. Define a named property constant
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open ``src/omotes_simulator_core/entities/assets/asset_defaults.py`` and add a module-level
constant for each new column name:

.. code-block:: python

    PROPERTY_MY_NEW_QUANTITY = "my_new_quantity"

Using a named constant prevents mismatched string literals between the writing side and any
downstream code that reads the ``DataFrame`` columns.

2. Implement or extend ``write_to_output``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the target asset class, add or extend ``write_to_output``. The method must:

- add keys with ``self.outputs[port_index][-1].update({...})``, so they go into the
  dictionary that ``write_standard_output`` appended for this timestep,
- not call ``write_standard_output`` itself; ``HeatNetwork.store_output`` already calls it
  first, and a second call would append an extra row,
- not replace the dictionary, so the standard columns are kept.

Example, following ``GasHeater``, which adds its columns to port 1:

.. code-block:: python

    from omotes_simulator_core.entities.assets.asset_defaults import PROPERTY_MY_NEW_QUANTITY

    def write_to_output(self) -> None:
        output_dict_temp = {
            PROPERTY_MY_NEW_QUANTITY: self._compute_my_quantity(),
        }
        self.outputs[1][-1].update(output_dict_temp)

When you extend an existing asset, add to its current ``write_to_output`` instead of
replacing it. A subclass that overrides ``write_to_output`` replaces the parent's columns
unless it calls ``super().write_to_output()``; ``GasHeater`` deliberately rewrites the
``ProductionCluster`` columns itself.

For assets with symmetric ports, such as ``Pipe``, iterate over all ports:

.. code-block:: python

    def write_to_output(self) -> None:
        for i in range(len(self.connected_ports)):
            self.outputs[i][-1].update(
                {PROPERTY_MY_NEW_QUANTITY: self._compute_my_quantity(i)}
            )

3. Verify the column appears in ``get_timeseries``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``AssetAbstract.get_timeseries`` converts ``self.outputs`` to a ``pandas.DataFrame`` with
multi-level columns ``(port_id, property_name)``. No changes to this method are required for
new columns; the new key is picked up automatically from the updated dictionary.

The assembled result flows through ``HeatNetwork.gather_output`` and is returned by
``SimulationManager.execute`` as one ``DataFrame`` with all asset timeseries concatenated
along the column axis.

4. Register the asset (new asset only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A new asset only produces output when the ESDL mapper adds it to the ``HeatNetwork``. See
:doc:`AddEntityLayerAsset` or :doc:`AddSolverAndEntityLayerAssets` for the mapping
workflow; output needs nothing beyond the steps above.

Implementation notes
--------------------

- ``write_standard_output`` is called by ``HeatNetwork.store_output`` before
  ``write_to_output`` for every asset each timestep. It appends a fresh dictionary to
  ``self.outputs[i]`` for each port, so ``self.outputs[i][-1]`` is always the current
  timestep when ``write_to_output`` runs.

- ``store_output`` runs once per timestep, after the convergence loop and after
  ``post_process_assets``. Values read in ``write_to_output`` therefore reflect the state
  after ``postprocess``; for ``IdealHeatStorage`` that is the updated fill level.

- The indexing convention for ``outputs[i]`` follows ``self.connected_ports``: index 0 is
  typically the inlet and index 1 is the outlet. Some multi-circuit assets (for example
  ``HeatPump`` and ``HeatExchanger`` with four connection points) use indices 0–3. Match
  the index to the physical port.

- ``get_timeseries`` builds ``DataFrame`` columns as ``(port_id, property_name)`` tuples,
  where ``port_id`` is the ESDL port identifier string from ``self.connected_ports[i]``.
  Downstream consumers must use the same tuple structure when reading specific columns.

- There is no registry of valid column names. Adding a constant to ``asset_defaults.py``
  is a convention, not a framework requirement; however, it is enforced by code review and
  prevents duplicate or diverging string literals.

- ``write_to_output`` is abstract in ``AssetAbstract``. Every concrete asset must provide
  an implementation. If the asset has no asset-specific columns beyond the standard ones,
  provide a no-op body:

  .. code-block:: python

      def write_to_output(self) -> None:
          pass

Testing and validation
----------------------

Follow the pattern in ``unit_test/entities/test_gas_heater.py`` and
``unit_test/entities/test_pipe.py``:

1. Construct the asset under test and patch the solver asset getters
   (``get_mass_flow_rate``, ``get_pressure``, ``get_temperature``) or prime
   ``solver_asset.prev_sol`` with representative values.
2. Call ``asset.write_standard_output()`` to append the standard columns. In the full
   simulation ``HeatNetwork.store_output`` does this.
3. Call ``asset.write_to_output()`` to add the asset-specific columns.
4. Assert that the expected keys exist in ``asset.outputs[port_index][-1]`` and that the
   values match.

Example assertion pattern:

.. code-block:: python

    def test_write_to_output(self) -> None:
        self.my_asset.write_standard_output()
        self.my_asset.write_to_output()
        self.assertAlmostEqual(
            self.my_asset.outputs[1][-1][PROPERTY_MY_NEW_QUANTITY],
            expected_value,
        )

For end-to-end coverage, ``unit_test/simulation/test_networksimulation.py`` checks that
``gather_output`` returns one row per timestep after a complete run. If your change affects
the shape of the returned ``DataFrame``, add or update an assertion on the column index.

Run the unit tests with ``ci/linux/test_unit.sh`` or ``ci\win32\test_unit.cmd``, or run a
single file with ``python -m pytest unit_test/entities/test_gas_heater.py --no-cov``. See
:doc:`testing_strategy` for details.

To validate the documentation build after updating this page, use the repository
convenience script. This is an intentional platform-specific exception because the
wrapper script differs by shell (``.bat`` on Windows and ``.sh`` on Linux):

.. code-block:: console

  doc\run_sphinx.bat

On Linux, run ``doc/run_sphinx.sh`` instead.

Common pitfalls
---------------

- **Calling ``write_standard_output`` from ``write_to_output``.** ``store_output`` already
  calls it, so the asset gets two rows per timestep and its timeseries no longer lines up
  with the other assets.

- **Calling ``update`` on an empty list.** ``self.outputs[i][-1]`` raises ``IndexError``
  when ``write_standard_output`` has not run yet, which mostly happens in unit tests.

- **Replacing instead of updating.** Assigning ``self.outputs[i][-1] = {...}`` overwrites
  the standard columns. Always use ``.update``.

- **Using a raw string literal as a column key.** String literals that differ by a single
  character produce silently wrong output. Define every column name as a constant in
  ``asset_defaults.py`` and import it.

- **Writing to the wrong port index.** Confirm which index corresponds to the inlet versus
  outlet for the specific asset topology before choosing ``outputs[0]`` or ``outputs[1]``.
  Multi-circuit assets have more than two ports; check ``self.connected_ports`` to match
  the physical port.

- **Assuming ``get_timeseries`` produces flat column names.** The method returns a
  multi-level ``(port_id, property_name)`` column index. Code that reads specific columns
  from the returned ``DataFrame`` must use the tuple form, not a plain string.

- **Editing generated API pages.** Pages under ``doc/developer/api/`` are autogenerated by
  ``sphinx.ext.apidoc`` on every build. Do not hand-edit them to document new constants or
  methods; the source docstrings in ``asset_defaults.py`` and the asset files are the
  canonical location for that reference material.

Related documentation
---------------------

- :doc:`AddEntityLayerAsset` — adding an asset based on an existing solver asset, using
  ``GasHeater`` as the example.
- :doc:`AddSolverAndEntityLayerAssets` — complete workflow for a new asset type,
  including entity-layer, solver-layer, ESDL mapper, and mapper registration steps that
  precede output implementation for a brand-new asset.
- :doc:`simulation_flow` — end-to-end code layout and execution flow from
  ``app.py`` through ``SimulationManager``, ``NetworkSimulation``, and ``HeatNetwork``.
- :doc:`testing_strategy` — test layout, how to run the full test suite, and the contributor
  checklist.
- :doc:`../network/network_main` — conceptual overview of how the network
  simulation coordinates assets, the solver, and the controller.
- For class-level details on ``AssetAbstract``, ``HeatNetwork``, and related types, consult
  the :doc:`api/omotes_simulator_core` root index.
