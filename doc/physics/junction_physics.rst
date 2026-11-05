Junction
========

Description
-----------

The ``Junction`` asset represents a connection point where two or more thermal-network assets meet.
In simulation, it acts as a mixing and continuity node: incoming and outgoing flows are balanced,
and the node state provides a common pressure and thermal state that connected assets use at their
connection points.
The junction is created from ESDL connectivity (for example ``Joint`` connections) during network
mapping and is represented internally by a solver node.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 40 20 30

   * - Parameter
     - Description
     - Unit
     - ESDL Asset Property
   * - ``pn_bar``
     - Junction pressure set value used as nominal/initial node pressure
     - Pa
     - derived from mapped network settings
   * - ``tfluid_k``
     - Junction fluid temperature set value used as nominal/initial node temperature
     - K
     - derived from mapped network settings

     
Physics and Assumptions
-----------------------

The junction enforces local conservation and state consistency between connected assets. It does not
model component behavior on its own; instead, it provides the coupling equations that connect asset
ports.

Mass flow
~~~~~~~~~

The junction enforces continuity of mass flow. The algebraic sum of node discharge and all connected
port mass flows is zero:

.. math::

   \dot{m}_{node} + \sum_i \dot{m}_i = 0

where :math:`\dot{m}_{node}` is the node discharge variable and :math:`\dot{m}_i` are mass flows at
all connected asset ports.

Energy and mixing
~~~~~~~~~~~~~~~~~

When connected flows indicate mixing at the node, the junction enforces a flow-weighted energy
balance:

.. math::

   \dot{m}_{node} u_{node} + \sum_i \dot{m}_i u_i = 0

where :math:`u` is specific internal energy. This relation determines the node thermal state and,
through fluid properties, the effective mixed temperature seen by connected assets.

For special flow situations (all connected flows with the same sign or near-zero flow), the node
temperature is prescribed to its configured initial value to keep the system well posed.

Pressure
~~~~~~~~

The junction acts as a common hydraulic state for connected ports. Connected assets use this shared
node pressure in their coupling equations. The node can also be operated with a fixed pressure value:

.. math::

   p_{node} = p_{set}

This is used when pressure must be prescribed at the junction.

.. _junction-physics-assumptions:

Assumptions
-----------

- The junction has no thermal capacity and no dynamic storage of mass or energy.
- Mixing at the junction is ideal and instantaneous within a timestep.
- Pressure losses and heat losses inside the junction are neglected.
- Node discharge is represented as an algebraic balancing variable.

.. _junction-physics-limitations:

Limitations
-----------

- The model does not represent detailed geometry-driven mixing effects.
- No local pressure-drop model is included for fittings or manifolds at the junction.
- No transient stratification or delay effects are represented at the node.

See Also
--------

- :doc:`pipe_physics` — Network piping and transport
- :doc:`producer_physics` — Heat supply boundaries
- :doc:`consumer_physics` — Heat demand boundaries

References
----------

.. rubric:: References

*(No references listed.)*