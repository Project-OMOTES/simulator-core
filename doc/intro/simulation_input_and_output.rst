Simulation input and output
===========================

A simulation run is defined by a model description and a time configuration. The package then returns
structured time-series results for analysis and integration.

Input model
-----------

Simulation input is based on ESDL (Energy System Description Language). ESDL assets and topology are
mapped into simulator entities before execution.

Run configuration
-----------------

A run is configured with:

- Simulation start and stop datetime
- Timestep duration
- Simulation identifiers and metadata used by calling workflows

Output
------

Simulation output is provided as time-series data for relevant hydraulic and thermal quantities over
the configured period.

See also
--------

- Package usage examples in the repository README
- Solver and physics sections for interpretation of state variables and governing relations
