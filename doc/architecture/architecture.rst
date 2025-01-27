General architecture
=========================
In this section we will describe the general architecture of the simulator.

The simulation manager manages model configuration and simulation execution, see section :ref:`simulation manager`.
The simulation manager uses ESDL as input. 
The project contains a wrapper class around pyesdl, see :ref:`esdl_object`.

In addtion, a configuration object is required, that contains the configuration for the simulation, see section :ref:`configuration_class`.

When the simulation is executed it creates a heat network class and a heat network controller class.
Both of these classes use factories methods to create the assets needed, see :ref:`asset_factory`.
Both the heat network object and the controller object are used to create a network simulation object,
which runs the simulation and passes back the results.


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   asset_factories
   configuration
   esdl_object
   simulation_manager





