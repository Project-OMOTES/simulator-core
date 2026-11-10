Developer how-to guides
=======================

Purpose
-------

This section contains step-by-step guides for common extension tasks. Each guide is
implementation-oriented and targeted at contributors who already know the repository
layout. If you are new to this repository, read :doc:`developer_navigation`,
:doc:`architecture`, and :doc:`simulation_flow` first.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   AddEntityLayerAsset
   AddSolverLayerAssets
   ControlExtension
   AddOutputFormat

Execution or extension flow
---------------------------

Pick the guide that matches the smallest change that does the job:

:doc:`AddEntityLayerAsset`
    Add an entity asset that reuses an existing solver asset, for example a new producer
    type that subclasses ``ProductionCluster`` like ``GasHeater`` and ``ElecBoiler``. Covers
    the entity class, ESDL mapping, controller mapping, and tests.

:doc:`AddSolverLayerAssets`
    Add a solver asset when no existing one provides the equations you need: base class
    choice, unknowns, ``EquationObject`` rows, and unit and solver-level integration tests.
    Then continue with :doc:`AddEntityLayerAsset` to wrap it in an entity asset.

:doc:`ControlExtension`
    Change how setpoints are computed: asset controllers, ``ControllerNetwork``,
    ``NetworkController``, controller mappers, and the setpoint dictionary keys.

:doc:`AddOutputFormat`
    Add output columns to an asset: ``PROPERTY_*`` constants, ``write_to_output``, and the
    layout of the result ``DataFrame``.

Related documentation
---------------------

- :doc:`testing_strategy` — test levels and commands used by every guide.
- :doc:`api/omotes_simulator_core` — generated class and module reference.
