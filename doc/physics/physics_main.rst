Physics
=======

This section describes the physical model solved by OMOTES.SIMULATOR_CORE for thermal
networks. The solver computes hydraulic and thermal state variables at asset connection
points and network nodes for each simulation step.

The primary unknowns are:

#. Pressure :math:`p` [Pa]
#. Specific internal energy :math:`u` [J/kg] (IE)
#. Mass flow rate :math:`\dot{m}` [kg/s]

Specific internal energy is used as the thermal state variable. Temperature is obtained
through fluid-property relations :math:`u(T)` and :math:`T(u)`.

Basic governing relations
-------------------------

The network equations are built from mass, energy, and pressure relations.

Mass conservation at a node
~~~~~~~~~~~~~~~~~~~~~~~~~~~

At each node, incoming and outgoing mass flows balance:

.. math::

    \sum_i \dot{m}_i = 0

Energy conservation at a node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At each node, convective energy transport balances with local heat input or extraction:

.. math::

    \sum_i \dot{m}_i u_i + Q_{node} = 0

where :math:`Q_{node}` is net heat exchange associated with the node equation.

Pressure relation across an asset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Across each asset, pressure difference is related to driving and loss terms:

.. math::

    p_{out} - p_{in} + \Delta p_{asset} = 0

where :math:`\Delta p_{asset}` depends on the asset model (for example pipe friction,
minor losses, or prescribed boundary pressure).

Energy relation across an asset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Across each asset, transported thermal energy changes according to supplied or extracted heat:

.. math::

    \dot{m} (u_{out} - u_{in}) = Q_{asset}

where :math:`Q_{asset}` is positive for net heat addition to the fluid and negative for
net heat extraction.

These relations are combined with asset-specific constitutive equations in the pages below.

**Contents**

.. toctree::
    :maxdepth: 1
    :glob:

    junction_physics.rst
    producer_physics.rst
    consumer_physics.rst
    pipe_physics.rst
    heat_exchanger_physics.rst
    heat_pump_physics.rst
    air_to_water_heat_pump_physics.rst
    ideal_heat_storage_physics.rst
    ates_cluster_physics.rst





