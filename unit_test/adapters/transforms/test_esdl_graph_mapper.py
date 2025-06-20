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
from pathlib import Path
from omotes_simulator_core.adapter.transforms.esdl_graph_mapper import EsdlGraphMapper
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file
from omotes_simulator_core.adapter.utility.graph import Graph


class TestEsdlGraphMapper(unittest.TestCase):
    """Test class for EsdlGraphMapper."""

    def setUp(self) -> None:
        """Set up test case."""
        self.mapper = EsdlGraphMapper()

    def test_to_entity_method(self):
        """Test for to_entity method."""
        # Arrange
        esdl_file_path = (
            Path(__file__).parent / ".." / ".." / ".." / "testdata" / "heat_transfers_test.esdl"
        )
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))

        # Act
        graph = self.mapper.to_entity(esdl_object)

        # Assert
        self.assertIsInstance(graph, Graph)
        self.assertEqual(len(graph.graph.nodes), 19)
        self.assertEqual(len(graph.graph.edges), 20)
