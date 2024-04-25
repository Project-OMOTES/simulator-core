.. _main-assets:

Asset classes
+++++++++++++++++
The main purpose of the asset classes is to translate the physics into linearized equation, which can be passed to the matrix to be solved.
This is done in an iterative way via the Newton-Raphson approach. Independent on the asset type there are several equation which always need to be solved.
These are:

#. Setting the pressure of connection points equal to the pressure of the node.
#. Setting the internal specific energy of the asset equal to it of the node, when the flow is into the asset.

Next tot his an asset will need at least two equations to specify the relation between the pressure at the connection points and the mass flow rate.
Also the internal continuity needs to be pre-described. Finally also an internal energy balance needs to be included. Internal meaning a relation between the connection points of the asset.

These equations are asset specific and detailed in there respective sections. At the moment we support the following assets:

#. :ref:`solver-pipe`: Class representing a pipe in a heating network.
#. :ref:`solver-producer`: Class representing a producer and also a consumer in a heating network.

**Contents**

.. toctree::
    :maxdepth: 1
    :glob:

    assets/solver_pipe.rst
    assets/solver_producer.rst
    assets/solver_node.rst