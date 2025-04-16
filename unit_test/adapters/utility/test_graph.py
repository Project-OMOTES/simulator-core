#  Copyright (c) 2025. Deltares & TNO
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

"""Test ates mapper."""

import unittest
from omotes_simulator_core.adapter.utility.graph import Graph


class TestGraph(unittest.TestCase):
    """Test class for graph."""

    def setUp(self) -> None:
        """Set up test case."""
        self.graph = Graph()

    def test_node_exists(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("node1")
        # Act
        result = self.graph.node_exists("node1")
        # Assert
        self.assertTrue(result)

    def test_adding_node_twice(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("node1")
        # Act
        with self.assertRaises(ValueError):
            self.graph.add_node("node1")

    def test_is_directly_connected(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.connect("A", "B")

        # Act
        res = self.graph.is_directly_connected("A", "B")

        # Assert
        self.assertTrue(res)

    def test_is_directly_connected_false(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("A")
        self.graph.add_node("B")

        # Act
        res = self.graph.is_directly_connected("A", "B")

        # Assert
        self.assertFalse(res)

    def test_is_directly_connected_error_node1(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("A")
        self.graph.add_node("B")

        # Act
        with self.assertRaises(ValueError):
            self.graph.is_directly_connected("D", "A")

    def test_is_directly_connected_error_node2(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("A")
        self.graph.add_node("B")

        # Act
        with self.assertRaises(ValueError):
            self.graph.is_directly_connected("A", "D")

    def test_connect_error(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("A")
        self.graph.add_node("B")

        # Act
        with self.assertRaises(ValueError):
            self.graph.connect("C", "D")

    def test_connect_error_node2(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("A")
        self.graph.add_node("B")

        # Act
        with self.assertRaises(ValueError):
            self.graph.connect("A", "D")

    def test_is_connected(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_node("D")
        self.graph.add_node("E")
        self.graph.add_node("F")
        self.graph.connect("B", "C")
        self.graph.connect("C", "E")
        self.graph.connect("E", "F")
        # Act
        res = self.graph.is_connected("B", "F")

        # Assert
        self.assertTrue(res)

    def test_is_connected_false(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_node("D")
        self.graph.add_node("E")
        self.graph.add_node("F")
        self.graph.connect("B", "C")
        self.graph.connect("C", "D")
        self.graph.connect("E", "F")
        # Act
        res = self.graph.is_connected("B", "F")

        # Assert
        self.assertFalse(res)

    def test_is_connected_error_node1(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("B")

        # Act
        with self.assertRaises(ValueError):
            self.graph.is_connected("A", "B")

    def test_is_connected_error_node2(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("B")

        # Act
        with self.assertRaises(ValueError):
            self.graph.is_connected("B", "A")

    def test_get_path(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_node("D")
        self.graph.add_node("E")
        self.graph.add_node("F")
        self.graph.connect("B", "C")
        self.graph.connect("C", "E")
        self.graph.connect("E", "F")

        # Act
        res = self.graph.get_path("B", "F")

        # Assert
        self.assertEqual(res, ["B", "C", "E", "F"])

    def test_get_path_error_node1(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("B")

        # Act
        with self.assertRaises(ValueError):
            self.graph.get_path("A", "B")

    def test_get_path_error_node2(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("B")

        # Act
        with self.assertRaises(ValueError):
            self.graph.get_path("B", "A")

    def test_get_path_not_possible(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_node("D")
        self.graph.add_node("E")
        self.graph.add_node("F")
        self.graph.connect("B", "C")
        self.graph.connect("C", "D")
        self.graph.connect("E", "F")

        # Act
        res = self.graph.get_path("B", "F")

        # Assert
        self.assertEqual(res, [])

    def test_is_tree_true(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_node("D")
        self.graph.connect("A", "B")
        self.graph.connect("A", "C")
        self.graph.connect("B", "D")

        # Act
        res = self.graph.is_tree()

        # Assert
        self.assertTrue(res)

    def test_is_tree_false(self):
        """Test for graph."""
        # Arrange
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_node("D")
        self.graph.connect("A", "B")
        self.graph.connect("A", "C")
        self.graph.connect("B", "D")
        self.graph.connect("C", "D")

        # Act
        res = self.graph.is_tree()

        # Assert
        self.assertFalse(res)
