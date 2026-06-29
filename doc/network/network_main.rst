Network layer
==============

Overview
--------

This section describes:
- how assets are connected into a hydraulic network, 
- how that structure is represented and built from ESDL, 
- and how information is exchanged during simulation. 

It covers connectivity, communication between nodes and assets, and how network behavior interacts with solver and controller flow.

The network model is configured from ESDL-derived assets and represented as connected
components and nodes. At each simulation step, setpoints from the controller are applied
to assets, the network equations are assembled, and solver results are propagated back to
entities.

Representation
---------------

The network is represented as a graph of *assets* and *nodes*. Assets model (combined) physical
components (pipes, producers, consumers, heat exchangers, storage). Nodes model the
connection points between assets where hydraulic and thermal state is shared.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Component
     - Structural role
   * - ``Network``
     - Top-level graph container; holds all assets and nodes and provides connection
       logic.
   * - ``BaseAsset``
     - Solver-side asset element; carries one or more numbered connection points, each
       of which is linked to exactly one ``Node``.
   * - ``Node``
     - Solver-side node element; represents a shared hydraulic and thermal state point;
       records all (asset, connection-point) pairs attached to it.
   * - ``Junction``
     - Entity-level wrapper around a solver ``Node``; carries physical attributes such
       as nominal pressure, fluid temperature, and height.
   * - ``HeatNetwork``
     - Entity-level network container; owns a solver ``Network``, a list of asset
       entities, and a list of ``Junction`` objects.

For class and implementation details see :doc:`../reference/solver_reference`.

Each asset exposes a fixed number of connection points (typically two: inlet at index 0
and outlet at index 1). Each connection point maps to a single ``Node``; a node may be
shared by any number of asset connection points, representing a physical junction between
components.

Construction
------------

The network is built from an ESDL energy-system description during simulation
initialization. Construction proceeds in two steps.

**Step 1 — Asset conversion**

Each enabled ESDL asset is translated into an entity that carries a solver-side
representation and an ordered list of port identifiers that preserve ESDL connection
order. ESDL ``Joint`` elements are not converted in this step; they are resolved in
step 2.

**Step 2 — Junction creation and connectivity**

For each converted asset, every connection point is resolved against the ESDL
connectivity description to identify the neighbouring asset and port. If the connection
passes through a ``Joint``, the joint is absorbed and the two flanking assets are
connected directly; no solver node is created for the joint itself.

Nodes are created and shared as connections are wired:

- If neither side has a node yet, a new node is created and both sides are wired to it.
- If one side already has a node, the other side is wired to the same node.
- If both sides already have separate nodes, those nodes are merged into one and all
  existing connections are rewired accordingly.

Each resulting shared node is recorded as a ``Junction`` in the network.

Sub-network partitioning
-------------------------

The controller layer partitions the full asset graph into hydraulically independent
sub-networks. This partitioning is driven by the presence of heat transfer assets (heat
exchangers and heat pumps), which form the boundaries between primary and secondary
circuit sides.

An intermediate graph is constructed from the ESDL topology. Each non-heat-transfer
asset is represented as a single node in this graph; each heat transfer asset is
represented as two nodes reflecting the hydraulic separation of its primary and secondary
sides. ESDL port connections are translated into graph edges.

Assets are then assigned to sub-networks through graph reachability:

1. Heat transfer assets are grouped first; their primary and secondary sides anchor
   separate sub-network boundaries.
2. All remaining assets (producers, consumers, storage) are assigned to the sub-network
   whose boundary nodes are reachable from that asset.

When no heat transfer assets are present, all assets belong to a single sub-network.

The partitioning determines which producers, consumers, and storage devices share a
common hydraulic circuit. The controller dispatches setpoints per sub-network, and the
conversion factors across heat transfer assets relate thermal demands between connected
sub-networks. How those setpoints are computed and applied is the responsibility of the
controller; see :doc:`../reference/controller_reference`.

Node connectivity rules
------------------------

Each asset connection point is linked to at most one node. A node may be connected to
any number of asset connection points. The continuity and energy-balance equations
assembled at each node require at least one connected asset; isolated nodes are not
meaningful in the solved system.

At a node with :math:`n` connected asset ports, the solver enforces one mass-flow
continuity equation:

.. math::

   \sum_{i=1}^{n} \dot{m}_i = 0

This single constraint accounts for conservation at the junction. Connected assets
contribute their own pressure and thermal relations at that node. See
:doc:`../physics/junction_physics` for the full set of node equations.

Assumptions
-----------

- Only ESDL assets with state ``ENABLED`` are included in the network; disabled assets
  are silently skipped during construction.
- ESDL ``Joint`` elements are absorbed into junctions during construction; they do not
  produce standalone solver nodes or equation contributions.
- Heat transfer assets are the only structural boundaries between sub-networks; all
  other assets within a connected graph component belong to the same sub-network.
- Each asset connection point connects to exactly one node; fan-out at a single port is
  not directly supported and must be modelled via explicit junction assets.
- The partitioning into sub-networks is performed once at construction time and does not
  change during the simulation.

Limitations
-----------

- The sub-network partitioning uses undirected graph reachability and does not account
  for flow direction.
- Merging of solver nodes during construction may produce a network structure that differs
  from a naive one-node-per-ESDL-port interpretation when multiple ESDL connections share
  a port.
- ESDL assets not covered by a registered mapper raise ``NotImplementedError`` and
  cannot be included in the network.
- The graph used for sub-network detection is derived from the ESDL file topology, not
  from the solved hydraulic state; circuits that become hydraulically isolated at runtime
  (for example, due to zero-flow heat exchangers) are not reflected as separate
  sub-networks.

Implementation reference
-------------------------

For solver-side network class details, see :doc:`../reference/solver_reference`. For
controller-side sub-network behavior, see :doc:`../reference/controller_reference`. For
network simulation orchestration, see :doc:`../reference/architecture_reference`. For
node-level mass flow, energy, and pressure equations, see
:doc:`../physics/junction_physics`.

See also :ref:`network-class` for the solver-side network class and :ref:`sub_network_class` for controller-side sub-network behavior.
