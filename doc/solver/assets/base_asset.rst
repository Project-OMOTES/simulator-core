.. _base-asset:

Base asset class
++++++++++++++++++++++++
Base asset class, which is used to add the first basic equations for the general assets.
This are equation to set the temperature or pressure or an equation to set the pressure or
temperature equal to the pressure of the connected node. This class is split from the 
base item class to avoid import errors. This class needs to import the node class for the 
type checking, while the node class needs to import the asset class. This resulted in a 
circular import  error. By splitting this class this is avoided.

.. autoclass:: simulator_core.solver.network.assets.base_asset.BaseAsset
    :members:
