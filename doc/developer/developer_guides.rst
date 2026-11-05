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
   AddSolverAndEntityLayerAssets
   ControlExtension
   AddOutputFormat

Execution or extension flow
---------------------------

Pick the guide that matches the smallest change that does the job:

:doc:`AddEntityLayerAsset`
    Add an entity asset that reuses an existing solver asset, for example a new producer
    type that subclasses ``ProductionCluster`` like ``GasHeater`` and ``ElecBoiler``. Covers
    the entity class, ESDL mapping, controller mapping, and tests.

:doc:`AddSolverAndEntityLayerAssets`
    Add an asset type whose equations no existing solver asset provides: a solver asset,
    an entity asset, an ESDL mapper, registration, and tests at solver and entity level.

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
