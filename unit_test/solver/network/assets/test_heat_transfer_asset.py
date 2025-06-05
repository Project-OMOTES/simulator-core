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

import unittest
from unittest.mock import patch
from uuid import uuid4
from omotes_simulator_core.solver.matrix.index_core_quantity import index_core_quantity
from omotes_simulator_core.solver.network.assets.heat_transfer_asset import HeatTransferAsset
from omotes_simulator_core.solver.network.assets.node import Node


class HeatTransferTest(unittest.TestCase):
    """Testcase for Boundary class."""

    def setUp(self) -> None:
        self.asset = HeatTransferAsset(
            name=str(uuid4()),
            _id=str(uuid4()),
        )
        # Create supply, connection_point:0 and return node, connection_point:1
        self.prim_supply_node = Node(name=str(uuid4()), _id=str(uuid4()))
        self.prim_return_node = Node(name=str(uuid4()), _id=str(uuid4()))
        self.sec_supply_node = Node(name=str(uuid4()), _id=str(uuid4()))
        self.sec_return_node = Node(name=str(uuid4()), _id=str(uuid4()))
        # Connect the nodes to the asset
        self.asset.connect_node(node=self.prim_supply_node, connection_point=0)
        self.asset.connect_node(node=self.prim_return_node, connection_point=1)
        self.asset.connect_node(node=self.sec_supply_node, connection_point=2)
        self.asset.connect_node(node=self.sec_return_node, connection_point=3)

    @patch.object(HeatTransferAsset, "get_internal_energy_to_node_equation")
    @patch.object(HeatTransferAsset, "prescribe_temperature_at_connection_point")
    @patch.object(HeatTransferAsset, "prescribe_mass_flow_at_connection_point")
    @patch.object(HeatTransferAsset, "prescribe_pressure_at_connection_point")
    @patch.object(HeatTransferAsset, "get_press_to_node_equation")
    @patch.object(HeatTransferAsset, "add_continuity_equation")
    def test_get_equations(
        self,
        mock_add_continuity_equation,
        mock_get_press_to_node_equation,
        mock_prescribe_pressure_at_connection_point,
        mock_prescribe_mass_flow_at_connection_point,
        mock_prescribe_temperature_at_connection_point,
        mock_get_internal_energy_to_node_equation,
    ):
        # Arrange

        # Act
        equations = self.asset.get_equations()  # act

        # Assert
        self.assertEqual(len(equations), 12)
        self.assertEqual(mock_add_continuity_equation.call_count, 4)
        self.assertEqual(mock_get_press_to_node_equation.call_count, 4)
        self.assertEqual(mock_prescribe_pressure_at_connection_point.call_count, 4)
        self.assertEqual(mock_prescribe_mass_flow_at_connection_point.call_count, 4)
        self.assertEqual(mock_prescribe_temperature_at_connection_point.call_count, 0)
        self.assertEqual(mock_get_internal_energy_to_node_equation.call_count, 4)
