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

"""Test Heat Pump Solver Asset."""
import unittest
from uuid import uuid4

from simulator_core.solver.matrix.core_enum import NUMBER_CORE_QUANTITIES, IndexEnum
from simulator_core.solver.network.assets.heat_transfer_asset import (
    FlowDirection,
    HeatTransferAsset,
)
from simulator_core.solver.network.assets.node import Node
from simulator_core.solver.network.network import Network
from simulator_core.solver.solver import Solver
from simulator_core.solver.utils.fluid_properties import fluid_props


class HeatTransferAssetTest(unittest.TestCase):
    """Test Heat Transfer Asset."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Create a ProductionAsset object
        self.asset = HeatTransferAsset(
            name=str(uuid4()),
            _id=str(uuid4()),
        )
        # Create nodes
        self.primary_supply_node = Node(name=str(uuid4()), _id=str(uuid4()))
        self.primary_return_node = Node(name=str(uuid4()), _id=str(uuid4()))
        self.secondary_supply_node = Node(name=str(uuid4()), _id=str(uuid4()))
        self.secondary_return_node = Node(name=str(uuid4()), _id=str(uuid4()))
        # Connect the nodes to the asset
        self.asset.connect_node(node=self.primary_supply_node, connection_point=0)
        self.asset.connect_node(node=self.primary_return_node, connection_point=1)
        self.asset.connect_node(node=self.secondary_supply_node, connection_point=2)
        self.asset.connect_node(node=self.secondary_return_node, connection_point=3)

    def test_get_equation_insufficient_nodes(self) -> None:
        """Evaluate the retrieval of equations from the boundary object with insufficient nodes."""
        # Arrange
        self.asset.connected_nodes = {}

        # Act
        with self.assertRaises(ValueError) as cm:
            self.asset.get_equations()

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(str(cm.exception), "The number of connected nodes must be 4!")

    def test_get_equations_invalid_number_of_unknowns(self) -> None:
        """Evaluate the retrieval of equations from the object with non-matching number of unknowns."""
        # Arrange
        self.asset.number_of_unknowns = 14

        # Act
        with self.assertRaises(ValueError) as cm:
            self.asset.get_equations()

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(str(cm.exception), "The number of unknowns must be 12!")

    def test_get_flow_direction_positive_mass_flow(self) -> None:
        """Evaluate the retrieval of flow direction with positive mass flow."""
        # Arrange
        connection_point = 0
        mass_flow = +10.0
        self.asset.prev_sol[IndexEnum.discharge + connection_point * NUMBER_CORE_QUANTITIES] = (
            mass_flow
        )

        # Act
        flow_direction = self.asset.flow_direction(connection_point=connection_point)

        # Assert
        self.assertEqual(flow_direction, FlowDirection.POSITIVE)

    def test_get_flow_direction_negative_mass_flow(self) -> None:
        """Evaluate the retrieval of flow direction with negative mass flow."""
        # Arrange
        connection_point = 0
        mass_flow = -10.0
        self.asset.prev_sol[IndexEnum.discharge + connection_point * NUMBER_CORE_QUANTITIES] = (
            mass_flow
        )

        # Act
        flow_direction = self.asset.flow_direction(connection_point=connection_point)

        # Assert
        self.assertEqual(flow_direction, FlowDirection.NEGATIVE)

    def test_get_flow_direction_zero_mass_flow(self) -> None:
        """Evaluate the retrieval of flow direction with zero mass flow."""
        # Arrange
        connection_point = 0
        mass_flow = +0.0
        self.asset.prev_sol[IndexEnum.discharge + connection_point * NUMBER_CORE_QUANTITIES] = (
            mass_flow
        )

        # Act
        flow_direction = self.asset.flow_direction(connection_point=connection_point)

        # Assert
        self.assertEqual(flow_direction, FlowDirection.ZERO)

    def test_get_connection_point_list_positive_primary_negative_secondary(self) -> None:
        """Evaluate the retrieval of connection points.

        Flow direction primary: positive
        Flow direction secondary: negative
        """
        # Arrange
        flow_direction_primary = FlowDirection.POSITIVE
        flow_direction_secondary = FlowDirection.NEGATIVE

        # Act
        connection_points = self.asset.get_connection_point_list(
            flow_direction_primary=flow_direction_primary,
            flow_direction_secondary=flow_direction_secondary,
        )

        # Assert
        self.assertListEqual(connection_points, [1, 0, 3, 2])
