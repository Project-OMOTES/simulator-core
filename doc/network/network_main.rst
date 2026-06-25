Network layer
=========================
This section describes how assets are connected into a hydraulic network and how information is exchanged during simulation.
It focuses on connectivity, communication between nodes and assets, and how network behavior interacts with solver and controller flow.

The network model is configured from ESDL-derived assets and represented as connected components and nodes.
At each simulation step, setpoints from the controller are applied to assets, the network equations are assembled, and solver results are propagated back to entities.

Network layer pages
-------------------

.. toctree::
   :maxdepth: 1

   network_topology

Implementation reference
-------------------------

For solver-side network class details, see :doc:`../reference/solver_reference`. For
controller-side sub-network behavior, see :doc:`../reference/controller_reference`. For
network simulation orchestration, see :doc:`../reference/architecture_reference`.

See also :ref:`network-class` for the solver-side network class and :ref:`sub_network_class` for controller-side sub-network behavior.
