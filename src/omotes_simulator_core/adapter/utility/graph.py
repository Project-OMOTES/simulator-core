#  Copyright (c) 2023. Deltares & TNO
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Module of simple graph class to help detect connectivity of the network."""


class Graph:
    """Main class for the graph."""

    def __init__(self):
        """Constructor of the class.

        The graph is stored as a dictionary of nodes and a list of edges.
        Both are initialised empty.
        """
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []

    def add_node(self, node: str) -> None:
        """Method to add a node to the graph.

        When the node already exists in the graph, an error is raised.
        :param str node: Name of the node to add.
        """
        if node in self.nodes:
            raise ValueError(f"Node {node} already exists in the graph.")
        self.nodes[node] = Node(node)

    def connect(self, node1: str, node2: str) -> None:
        """Method to connect two nodes in the graph.

        When the nodes are not in the graph, an error is raised.
        When the nodes are already connected, nothing happens,
        Otherwise a new edge is created and added to the graph.

        :param str node1: Name of the first node.
        :param str node2: Name of the second node.
        """
        if not self.node_exists(node1):
            raise ValueError(f"Node {node1} does not exist in the graph.")
        if not self.node_exists(node2):
            raise ValueError(f"Node {node2} does not exist in the graph.")
        if self.is_directly_connected(node1, node2):
            return
        self.edges.append(Edge(self.nodes[node1], self.nodes[node2]))
        self.nodes[node1].add_edge(self.edges[-1])
        self.nodes[node2].add_edge(self.edges[-1])

    def node_exists(self, node: str) -> bool:
        """Method to check if a node exists in the graph.

        :param str node: Name of the node to check.
        """
        return node in self.nodes

    def is_directly_connected(self, node1: str, node2: str) -> bool:
        """Method to check if two nodes are connected in the graph.

        Directly connected means that the nodes are connected by via a single edge.

        When the nodes are not in the graph, an error is raised.
        :param str node1: Name of the first node.
        :param str node2: Name of the second node.
        """
        if not self.node_exists(node1):
            raise ValueError(f"Node {node1} does not exist in the graph.")
        if not self.node_exists(node2):
            raise ValueError(f"Node {node2} does not exist in the graph.")
        for edge in self.nodes[node1].edges:
            # this looks a bit weir, but we need to also check the other edges, so we cannot simply
            # return the value of the first edge which is checked.
            if edge.connected(node2):
                return True
        return False

    def is_connected(self, node1: str, node2: str) -> bool:
        """Method to check if two nodes are connected in the graph.

        When the nodes are not in the graph, an error is raised.
        The method uses a breadth-first search to check if the nodes are connected.
        If the nodes are connected, the method returns True, otherwise False.

        :param str node1: Name of the first node.
        :param str node2: Name of the second node.
        """
        if not self.node_exists(node1):
            raise ValueError(f"Node {node1} does not exist in the graph.")
        if not self.node_exists(node2):
            raise ValueError(f"Node {node2} does not exist in the graph.")
        node_to_check = [self.nodes[node1]]
        nodes_checked = []
        while node_to_check:
            node = node_to_check.pop(0)
            nodes_checked.append(node)
            for edge in node.edges:
                for node in edge.nodes:
                    if node == self.nodes[node2]:
                        return True
                    if node not in nodes_checked and node not in node_to_check:
                        node_to_check.append(node)
        return False


class Edge:
    """Class for the edges in the graph."""

    def __init__(self, node1, node2):
        """Constructor of the class.

        An edge can only be connected to two nodes. The nodes are stored in a list.
        Node1 and node2 need to be different nodes, otherwise an error is raised.

        :param Node node1: First node connected to the edge.
        :param Node node2: Second node connected to the edge.
        """
        if node1 == node2:
            raise ValueError("An edge cannot connect a node to itself.")
        self.nodes = [node1, node2]  # list of nodes connected to the edge

    def connected(self, node_name: str) -> bool:
        """Method to check if a node is connected to the edge.

        If the node is connected to the edge, the method returns True, otherwise False.
        :param str node: Name of the node to check.
        """
        return any([node_name == node.node_name for node in self.nodes])


class Node:
    """Class for the nodes in the graph."""

    def __init__(self, node: str):
        """Constructor of the class.

        :param str node: Name of the node.
        """
        self.node_name = node
        self.edges: list[Edge] = []  # list of edges connected to the node

    def add_edge(self, edge: Edge) -> None:
        """Method to add an edge to the node.

        There is no limit to amount fo edges connected to one node.
        The edge is only added when it is not already in the list.
        No error is given when the edge is already in the list.

        :param Edge edge: Edge to add to the node.
        """
        if edge not in self.edges:
            self.edges.append(edge)


if __name__ == "__main__":
    graph = Graph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_node("C")
    graph.add_node("D")
    graph.add_node("E")
    graph.add_node("F")

    graph.connect("A", "B")
    graph.connect("B", "C")
    graph.connect("C", "D")
    graph.connect("E", "F")
    print(graph.is_directly_connected("A", "B"))
    print(graph.is_directly_connected("B", "A"))
    print(graph.is_connected("A", "E"))
