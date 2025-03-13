Assets
=========================
Assets consist of different classes to model various assets in a district heating network.

Be aware, that some of the assets model multiple physical assets (e.g., a pumping station with multiple pumps and pipes).

The primary goal of these asset classes is to take the physical inputs 
of the assets (e.g., inner diameter, wall roughness) and translate 
them into linearized equations.

.. autoclass:: omotes_simulator_core.solver.network.assets.base_item.BaseItem
   :members:
   :show-inheritance:
.. autoclass:: omotes_simulator_core.solver.network.assets.base_asset.BaseAsset
   :members:
   :show-inheritance:
.. autoclass:: omotes_simulator_core.solver.network.assets.fall_type.FallType
   :members:
   :show-inheritance:
.. autoclass:: omotes_simulator_core.solver.network.assets.solver_pipe.SolverPipe
   :members:
   :show-inheritance:
.. autoclass:: omotes_simulator_core.solver.network.assets.node.Node
   :members:
   :show-inheritance: