General architecture
=========================
In this section we will describe the general architecture of the simulator.
The main class is the simulation manager. This class is responsible for setting up the simulation and running it.
This class is described in more detail in the :ref:`simulation manager` section.
The simulation manager has as input an ESDL object, which is a wrapper class around pyesdl, for more detail see :ref:`esdl_object`.
The second input is a configuration object, which contains the configuration for the simulation.
This class is described in more detail in the :ref:`configuration_class` section.
When the simulation is executed is sets up a heat network class and a heat network controller class.
Both of these classes use factories methods to create the assets needed. These are described here: :ref:`asset_factory`.
Both the heat network object and the controller object are used to create a network simulation object, which basically tuns the simulation.


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   asset_factories
   configuration
   esdl_object
   simulation_manager





