.. _main-assets:

Asset classes
+++++++++++++++++
The main purpose of the asset classes is to translate the physics into linearized equations, which 
can be passed to the matrix to be solved. This is done iteratively via the Newton-Raphson approach. 
Independent of the asset type, there are several equations that always need to be solved. These are:

#. Setting the pressure of connection points equal to the pressure of the node.
#. Setting the internal specific energy of the asset equal to that of the node when the flow is into 
   the asset.

Additionally, an asset will need at least two equations to specify the relation between the pressure 
at the connection points and the mass flow rate. Also, the internal continuity needs to be pre-
described. Finally, an internal energy balance needs to be included. Internal means a relation 
between the connection points of the asset.

These equations are asset-specific and detailed in their respective sections. At the moment, we 
support the following assets:

#. :ref:`solver-pipe`: Class representing a pipe in a heating network.
#. :ref:`solver-producer`: Class representing a producer and also a consumer in a heating network.

All these assets have been derived from three base classes:

#. :ref:`base-item`: Base class for all items in the network.
#. :ref:`base-asset`: Base class for all assets in the network.
#. :ref:`fall-type`: Base class for components implementing a pressure loss equation.

**Contents**

.. toctree::
    :maxdepth: 1
    :glob:

    assets/base_item.rst
    assets/base_asset.rst
    assets/fall_type.rst
    assets/solver_pipe.rst
    assets/solver_producer.rst
    assets/solver_node.rst