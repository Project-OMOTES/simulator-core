Developer How-To Guides
=======================

Purpose
-------

This section contains step-by-step guides for common extension tasks. Each guide is
implementation-oriented and targeted at contributors who already understand the repository
structure. If you are new to the codebase, start with :doc:`architecture` and
:doc:`simulation_flow` first.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   AddEntityLayerAsset
   AddSolverAndEntityLayerAssets
   ControlExtension
   AddOutputFormat


Guide overview
--------------

:doc:`AddEntityLayerAsset`
    Add a new entity-layer asset class that wraps an existing solver-layer asset. Use this
    when a suitable solver-layer asset already exists and you only need to add entity-level
    state, setpoint handling, and output collection.

:doc:`AddSolverAndEntityLayerAssets`
    Add a completely new thermo-hydraulic asset type: solver layer, entity layer, ESDL
    mapper, and mapper registration. Use this when no suitable solver-layer asset exists.

:doc:`ControlExtension`
    Add a new controller type or extend existing dispatch logic. Covers asset-level
    controllers, network-level controller wiring, and mapper registration.

:doc:`AddOutputFormat`
    Add new output columns or datasets to existing assets. Covers ``write_to_output``,
    ``asset_defaults.py`` constants, and DataFrame shape expectations.
