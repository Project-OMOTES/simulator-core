.. _Pipe-asset:

Pipe asset
+++++++++++++++++++++++++++++++++++++++++++++

The **Pipe Asset** represents a pipe within the simulator, responsible for transporting fluids between 
different assets in the network.

This asset is stored within the `Pipe` class in the 
`omotes_simulator_core.entities.assets.pipe` module.

A pipe asset is initialized with an asset name, a unique asset ID, and a list of connected port IDs. It is 
characterized by various parameters such as length, inner diameter, roughness, heat transfer properties, and 
external temperature.

The `set_setpoints` method allows for defining necessary operational parameters before a simulation, while the 
`write_to_output` method stores the computed outputs for each timestep.

The pipe creates an instance of SolverPipe and assigns it to the solver_asset, which can be used for further
calculations in the simulation based on the pipe's defined properties.

.. autoclass:: omotes_simulator_core.entities.assets.pipe.Pipe
   :members: