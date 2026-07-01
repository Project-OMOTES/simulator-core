Adding a New Output Format
==========================

Purpose
-------

Use this guide when you need to extend the simulator's output — for example, to add a new
computed column to an existing asset's output, add output columns to an asset that currently
emits none, or change how the collected output is assembled and returned.

This page is for contributors who work at the Python implementation level. It assumes you can
navigate the repository and run the unit test suite. For conceptual system behavior and
governing relations, consult the Physics and Architecture sections instead.

The output pipeline has three layers: per-asset output accumulation (entity layer), network-wide
collection (``HeatNetwork``), and simulation-level assembly (``NetworkSimulation``). A new output
format always starts in the entity layer and flows automatically through the remaining two.

Relevant Modules and Files
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
     - All column names used as dictionary keys must be defined here; avoids hard-coded
       string literals scattered across asset files
   * - ``src/omotes_simulator_core/entities/assets/pipe.py``
     - Concrete asset — pipe
     - Practical reference implementation of ``write_to_output`` with multiple columns
       and per-port output
   * - ``src/omotes_simulator_core/entities/assets/demand_cluster.py``
     - Concrete asset — heat demand
     - Shows the minimal single-port ``write_to_output`` pattern using ``outputs[i][-1].update``
   * - ``src/omotes_simulator_core/entities/heat_network.py``
     - Network container
     - Calls ``write_standard_output`` and ``write_to_output`` on every asset each timestep
       via ``store_output``; collects results via ``gather_output``
   * - ``src/omotes_simulator_core/simulation/networksimulation.py``
     - Simulation orchestrator
     - Drives the per-timestep loop that calls ``store_output`` and exposes
       ``gather_output`` to the caller
   * - ``src/omotes_simulator_core/infrastructure/simulation_manager.py``
     - Top-level entry point
     - Calls ``worker.gather_output()`` and returns the combined ``pandas.DataFrame``
   * - ``unit_test/entities/test_pipe.py``
     - Unit tests for ``Pipe`` output
     - Reference test pattern for ``write_standard_output`` then ``write_to_output``
   * - ``unit_test/entities/test_heat_exchanger.py``
     - Unit tests for ``HeatExchanger`` output
     - Shows asserting on specific keys in ``outputs[i][-1]`` after both write calls
   * - ``unit_test/simulation/test_networksimulation.py``
     - Integration-level simulation test
     - Verifies the full pipeline from ``run`` through ``gather_output``

Extension Flow
--------------

The steps below cover the most common extension: adding one or more new output columns to an
existing or new asset. Steps 1–3 are always required. Step 4 applies only when you add a new
asset.

1. Define a named property constant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Open ``src/omotes_simulator_core/entities/assets/asset_defaults.py`` and add a module-level
constant for each new column name:

.. code-block:: python

    PROPERTY_MY_NEW_QUANTITY = "my_new_quantity"

Using a named constant prevents mismatched string literals between the writing side and any
downstream code that reads the ``DataFrame`` columns.

2. Implement or extend ``write_to_output``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the target asset class — for example
``src/omotes_simulator_core/entities/assets/my_asset.py`` — add or extend ``write_to_output``.
The method must:

- call ``self.write_standard_output()`` first if it has not already been called at this
  point in the per-timestep sequence (``HeatNetwork.store_output`` calls it separately,
  but individual asset unit tests often call both in order),
- call ``self.outputs[port_index][-1].update({...})`` to append new keys to the *most
  recent* output dictionary for the chosen port,
- not replace the entire dictionary; always use ``update`` to preserve the standard
  columns written by ``write_standard_output``.

Example — adding a single extra column to port 1 (the outlet port by convention):

.. code-block:: python

    from omotes_simulator_core.entities.assets.asset_defaults import PROPERTY_MY_NEW_QUANTITY

    def write_to_output(self) -> None:
        output_dict_temp = {
            PROPERTY_MY_NEW_QUANTITY: self._compute_my_quantity(),
        }
        self.outputs[1][-1].update(output_dict_temp)

For assets with two symmetric connection points — such as ``Pipe`` — iterate over all
ports and update each:

.. code-block:: python

    def write_to_output(self) -> None:
        for i in range(len(self.connected_ports)):
            self.outputs[i][-1].update(
                {PROPERTY_MY_NEW_QUANTITY: self._compute_my_quantity(i)}
            )

3. Verify the column appears in ``get_timeseries``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``AssetAbstract.get_timeseries`` converts ``self.outputs`` to a ``pandas.DataFrame`` with
multi-level columns ``(port_id, property_name)``. No changes to this method are required for
new columns; the new key is picked up automatically from the updated dictionary.

The assembled result flows through ``HeatNetwork.gather_output`` and is returned by
``SimulationManager.execute`` as a flat ``DataFrame`` with all asset timeseries concatenated
along the column axis.

4. Register new property constants (new asset only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are introducing a completely new asset, also ensure the asset is registered in the ESDL
mapper so that ``HeatNetwork.store_output`` can reach it. See :doc:`add_new_asset` for the
mapper registration workflow; nothing extra is required for output beyond the steps above.

Implementation Notes
--------------------

- ``write_standard_output`` is called by ``HeatNetwork.store_output`` before
  ``write_to_output`` for every asset each timestep. It appends a fresh dictionary to
  ``self.outputs[i]`` for each port. Because ``write_to_output`` calls
  ``self.outputs[i][-1].update``, the standard columns are always present in the same
  dictionary as the asset-specific columns.

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

Testing and Validation
----------------------

Follow the pattern established in ``unit_test/entities/test_pipe.py`` and
``unit_test/entities/test_heat_exchanger.py``:

1. Construct the asset under test and prime ``solver_asset.prev_sol`` with representative
   values.
2. Call ``asset.write_standard_output()`` to populate the standard columns.
3. Call ``asset.write_to_output()`` to add the asset-specific columns.
4. Assert that the expected keys exist in ``asset.outputs[port_index][-1]`` and that the
   computed values match.

Example assertion pattern:

.. code-block:: python

    def test_write_to_output(self) -> None:
        self.my_asset.write_standard_output()
        self.my_asset.write_to_output()
        self.assertAlmostEqual(
            self.my_asset.outputs[1][-1][PROPERTY_MY_NEW_QUANTITY],
            expected_value,
        )

For end-to-end coverage, refer to ``unit_test/simulation/test_networksimulation.py``, which
verifies that ``gather_output`` returns a non-empty ``DataFrame`` after a complete simulation
run. If your change affects the shape of the returned ``DataFrame`` (for example, adding
columns to every asset), add or update an assertion on the column index.

To run the unit tests:

.. code-block:: bash

    python -m pytest unit_test/

To validate the documentation build after updating this page:

.. code-block:: bash

    python -m sphinx -b html doc doc/_build/html

Common Pitfalls
---------------

- **Calling ``update`` on an empty list.** ``write_to_output`` must always be called
  *after* ``write_standard_output`` — or after any prior call that appended a dictionary
  to ``self.outputs[i]``. Calling ``self.outputs[i][-1].update(...)`` when the list is
  empty raises an ``IndexError``.

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

Related Documentation
---------------------

- :doc:`add_new_asset` — complete workflow for adding a new asset type, including
  entity-layer, solver-layer, ESDL mapper, and mapper registration steps that precede
  output implementation for a brand-new asset.
- :doc:`simulation_contributor_flow` — end-to-end code layout and execution flow from
  ``app.py`` through ``SimulationManager``, ``NetworkSimulation``, and ``HeatNetwork``.
- :doc:`testing` — test layout, how to run the full test suite, and the contributor
  checklist.
- :doc:`../network/network_main` — conceptual overview of how the network
  simulation coordinates assets, the solver, and the controller.
- For class-level details on ``AssetAbstract``, ``HeatNetwork``, and related types, consult
  the :doc:`api/omotes_simulator_core` root index.
