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
import networkx as nx


class Graph:
    """Main class for the graph."""

    def __init__(self) -> None:
        """Constructor of the class.

        The graph is stored as a dictionary of nodes and a list of edges.
        Both are initialised empty.
        """
        self.graph = nx.Graph()

    def add_node(self, node: str) -> None:
        """Method to add a node to the graph.

        When the node already exists in the graph, an error is raised.
        :param str node: Name of the node to add.
        """
        if self.node_exists(node):
            raise ValueError(f"Node {node} already exists in the graph.")
        self.graph.add_node(node)

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
        self.graph.add_edge(node1, node2)

    def node_exists(self, node: str) -> bool:
        """Method to check if a node exists in the graph.

        :param str node: Name of the node to check.
        """
        return bool(self.graph.has_node(node))

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
        for node in self.graph.neighbors(node1):
            if node == node2:
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
        if not self.get_path(node1=node1, node2=node2):
            return False
        else:
            return True

    def get_path(self, node1: str, node2: str) -> list[str]:
        """Method to get the path between two nodes in the graph.

        First it is checked if the nodes are in the graph. Then the shortest path algorithms is
        used. If no path is found an empty list is returned.
        :param str node1: Name of the first node.
        :param str node2: Name of the second node.
        """
        if not self.node_exists(node1):
            raise ValueError(f"Node {node1} does not exist in the graph.")
        if not self.node_exists(node2):
            raise ValueError(f"Node {node2} does not exist in the graph.")
        try:
            # Method to look up the shortest path between two nodes, using
            # Dijkstra's algorithm. The method only returns a single
            # shortest path, so it is not guaranteed to return all paths.
            return nx.shortest_path(self.graph, node1, node2)  # type: ignore
        except nx.NetworkXNoPath:
            return []

    def is_tree(self) -> bool:
        """Method to check if the graph is a tree.

        This check is needed since we cannot handle cycles.

        :return: True if the graph is tree, False otherwise.
        """
        return bool(nx.is_tree(self.graph))
