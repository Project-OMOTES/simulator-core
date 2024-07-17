.. _network-class:

Network class
++++++++++++++++++++
This class stores the information on the network. This is divided into:

#. Assets, these are the physical assets present in the heating network. For more info see :ref:`main-assets`
#. Nodes, these are connection between assets. For more information see

They main responsibility of this class is to stores these and to enable the user to add assets, and connect them.
For this purpose several methods have been implemented.

.. autoclass:: simulator_core.solver.network.network.Network
   :members: