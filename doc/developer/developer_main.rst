Developer Documentation
=======================

This section contains contributor-facing guides for OMOTES.SIMULATOR_CORE.

Use this section when you need implementation-oriented guidance — how the code is organized,
how to extend the package, how to test your changes, and how to navigate the generated API
reference.

For system-level conceptual behavior and governing relations, consult the Intro, Solver,
Network, Physics, and Control sections instead.

How to use this section
-----------------------

- Read :doc:`developer_navigation` first to choose the right path for your task.
- Use :doc:`simulation_contributor_flow` to understand the full code layout and execution
  flow before making any change.
- Use :doc:`add_new_asset` when implementing a new thermo-hydraulic asset type.
- Use :doc:`add_new_output_format` when adding new output columns, output datasets, or changing how output is assembled.
- Use :doc:`control_extension` when modifying or extending controller behavior.
- Use :doc:`testing` for guidance on test structure, running tests, and validation.
- Use :doc:`writing_documentation_with_ai` when writing or reviewing documentation with the
  AI agent workflow.
- Use the :doc:`api/omotes_simulator_core` root index for exhaustive package, module, and
  class lookup.

**Contents**

.. toctree::
   :maxdepth: 1
   :titlesonly:

   developer_navigation
   simulation_contributor_flow
   add_new_asset
   add_new_output_format
   control_extension
   testing
   writing_documentation_with_ai
   api/omotes_simulator_core
