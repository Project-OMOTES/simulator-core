Network layer
=========================
This section describes how assets are connected into a hydraulic network and how information is exchanged during simulation.
It focuses on connectivity, communication between nodes and assets, and how network behavior interacts with solver and controller flow.

The network model is configured from ESDL-derived assets and represented as connected components and nodes.
At each simulation step, setpoints from the controller are applied to assets, the network equations are assembled, and solver results are propagated back to entities.

The following pages are useful when working with the network layer:

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   ../solver/network
   ../architecture/network_simulation
   ../controller/sub_network_class

See also :ref:`network-class` for the solver-side network class and :ref:`sub_network_class` for controller-side sub-network behavior.
