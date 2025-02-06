.. _Consumer-asset:

Consumer asset
+++++++++++++++++++++++++++++++++++++++++++++
The **Consumer Asset** represents components that consume energy.

This asset is stored within the `DemandCluster` class in the 
`omotes_simulator_core.entities.assets.demand_cluster` module.

A consumer asset is initialized with an asset name, a unique asset ID, and a list of connected port IDs. 
Values are set for different parameters that include as internal diameter, supply and return temperatures, 
pressure input, thermal power allocation, and mass flow rate.

The `set_setpoints` method ensures that required setpoints—supply temperature, return temperature, and heat 
demand—are provided before adjusting the thermal power allocation and computing the mass flow rate accordingly. 
This calculated data is then passed to the `solver_asset` instance for further use in simulations.


.. autoclass:: omotes_simulator_core.entities.assets.demand_cluster.DemandCluster
   :members:

