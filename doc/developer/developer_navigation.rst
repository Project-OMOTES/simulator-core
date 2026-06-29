Developer Navigation
====================

Purpose
-------

Use this page to quickly choose the right developer documentation path.

Start here
----------

- Need to understand how the code is organized and how simulation runs end-to-end: go to
  :doc:`simulation_contributor_flow`.
- Need to add a new physics asset: go to :doc:`add_new_asset`.
- Need to add or modify output columns or output format: go to :doc:`add_new_output_format`.
- Need to modify or extend controller behavior: go to :doc:`control_extension`.
- Need to understand where tests live and how to run them: go to :doc:`testing`.
- Need exhaustive package, module, or class lookup: go to :doc:`api/omotes_simulator_core`.
- Need to write or review documentation using the AI agent workflow: go to :doc:`writing_documentation_with_ai`.

Contributor guides
------------------

- :doc:`simulation_contributor_flow` — code layout, package structure, and the full
  simulation execution flow from entrypoint to solver.
- :doc:`add_new_asset` — step-by-step workflow for adding a new thermo-hydraulic asset
  type (entity layer, solver layer, ESDL mapper, registry).
- :doc:`add_new_output_format` — step-by-step workflow for adding new output columns,
  output datasets, or changing how the assembled output ``DataFrame`` is constructed.
- :doc:`control_extension` — step-by-step workflow for adding or modifying controller
  classes, mappers, and dispatch logic.
- :doc:`testing` — test layout, how to run the suite, unit and integration test patterns,
  and the contributor checklist.
- :doc:`writing_documentation_with_ai` — which AI agents exist, how to invoke them, and
  how to write, review, and validate documentation using the agent workflow.

For exhaustive package, module, and class lookup beyond these guides, consult the
:doc:`api/omotes_simulator_core` root index.
