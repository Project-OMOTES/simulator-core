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

"""Test Boundary entities."""
import unittest
from unittest.mock import patch
from uuid import uuid4

from simulator_core.solver.matrix.core_enum import IndexEnum
from simulator_core.solver.network.assets.base_asset import BaseAsset
from simulator_core.solver.network.assets.boundary import BaseBoundary
from simulator_core.solver.network.assets.node import Node


class BaseBoundaryTest(unittest.TestCase):
    """Testcase for Boundary class."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Create a BaseBoundary object
        self.asset = BaseBoundary(
            name=uuid4(),
        )
        # Create supply, connection_point:0 and return node, connection_point:1
        self.supply_node = Node(name=uuid4())
        # Connect the nodes to the asset
        self.asset.connect_node(node=self.supply_node, connection_point=0)

    def test_boundary_create(self) -> None:
        """Evaluate the creation of a boundary object."""
        # Arrange

        # Act

        # Assert
        self.assertIsInstance(self.asset, BaseBoundary)
        self.assertEqual(self.asset.number_of_connection_point, 1)
        self.assertEqual(self.asset.number_of_unknowns, 3)

    def test_add_pressure_equation(self) -> None:
        """Evaluate the addition of a pressure equation to the boundary object."""
        # Arrange
        self.asset.initial_pressure = 50000.0

        # Act
        equation_object = self.asset.add_pressure_equation()

        # Assert
        self.assertEqual(equation_object.indices, [self.asset.matrix_index + IndexEnum.pressure])
        self.assertEqual(equation_object.coefficients, [1.0])
        self.assertEqual(equation_object.rhs, 50000.0)

    @patch.object(BaseAsset, "add_thermal_equations")
    @patch.object(BaseAsset, "add_press_to_node_equation")
    def test_get_equations(self, thermal_patch, press_to_node_patch) -> None:
        """Evaluate the retrieval of equations from the boundary object."""
        # Arrange

        # Act
        equations = self.asset.get_equations()

        # Assert
        thermal_patch.assert_called_once()
        press_to_node_patch.assert_called_once()
        self.assertEqual(len(equations), 3)
