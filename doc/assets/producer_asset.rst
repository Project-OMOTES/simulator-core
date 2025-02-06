.. _Producer-asset:

Producer asset
+++++++++++++++++++++++++++++++++++++++++++++

The **Producer Asset** represents all components that generate thermal energy.

This asset is stored within the `ProductionCluster` class in the 
`omotes_simulator_core.entities.assets.production_cluster` module.

A producer asset is initialized with an asset name, a unique asset ID, and a list of connected port IDs. It 
manages different operational parameters that include supply and return temperatures, pressure supply, and mass flow 
control. The producer ensures that the thermal production meets the given setpoints.

The `set_setpoints` method ensures that all necessary setpoints that includes supply temperature, return temperature, heat 
demand, and supply pressure are provided in order to compute the mass flow rate. 


.. autoclass:: omotes_simulator_core.entities.assets.production_cluster.ProductionCluster
   :members: