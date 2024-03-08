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

"""Test network class."""
import unittest
import uuid
from io import StringIO
from unittest.mock import patch

from simulator_core.solver.network.assets.node import Node
from simulator_core.solver.network.assets.solver_pipe import SolverPipe
from simulator_core.solver.network.network import Network


class NetworkTest(unittest.TestCase):
    """Class to test network class."""

    def setUp(self) -> None:
        """Set up for the tests."""
        self.network = Network()
        self.asset = SolverPipe(name=uuid.uuid4())
        self.asset2 = SolverPipe(name=uuid.uuid4())
        self.node = Node(name=uuid.uuid4())

    def test_init(self) -> None:
        """Test the constructor of the network class."""
        # arrange

        # act
        network = Network()  # act

        # assert
        self.assertEqual(network.assets, {})
        self.assertEqual(network.nodes, {})

    def test_add_asset_name(self) -> None:
        """Test adding an asset with a name."""
        # arrange
        asset = "Pipe"
        asset_name = uuid.uuid4()

        # act
        name = self.network.add_asset(asset_type=asset, name=asset_name)  # act

        # assert
        self.assertEqual(name, asset_name)
        self.assertIsInstance(self.network.assets[name], SolverPipe)

    def test_add_asset_no_name(self) -> None:
        """Test adding an asset without a name."""
        # arrange
        asset = "Pipe"

        # act
        name = self.network.add_asset(asset_type=asset)  # act

        # assert
        self.assertIsInstance(self.network.assets[name], SolverPipe)

    def test_add_asset_unknown_asset(self) -> None:
        """Test adding an unknown asset."""
        # arrange
        asset = "unknown asset"

        # act
        with self.assertRaises(ValueError) as cm:
            self.network.add_asset(asset_type=asset)

        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(str(cm.exception), f"{asset} not recognized.")

    def test_add_existing_asset(self) -> None:
        """Test adding an existing asset."""
        # arrange
        self.network.assets[self.asset.name] = self.asset

        # act
        with self.assertRaises(ValueError) as cm:
            self.network.add_existing_asset(asset=self.asset)  # act

        # assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(str(cm.exception), f"{self.asset.name} already exists in network.")

    def test_connect_single_asset_at_node(self) -> None:
        """Test connecting a single asset at a node."""
        # arrange
        self.network.nodes[self.node.name] = self.node
        self.network.add_existing_asset(asset=self.asset)
        self.network.add_existing_asset(asset=self.asset2)
        self.network.assets[self.asset.name].connect_node(node=self.node, connection_point=0)

        # act
        node_name = self.network._connect_single_asset_at_node(
            asset_id_connected=self.asset.name,
            connection_point_connected=0,
            asset_id_unconnected=self.asset2.name,
            connection_point_unconnected=1,
        )

        # assert
        self.assertEqual(node_name, self.node.name)

    def test_connect_both_assets_at_node(self) -> None:
        """Test connecting both assets by creating a node."""
        # arrange
        self.network.add_existing_asset(asset=self.asset)
        self.network.add_existing_asset(asset=self.asset2)

        # act
        node_name = self.network._connect_both_assets_at_node(
            asset1_id=self.asset.name,
            connection_point_1=0,
            asset2_id=self.asset2.name,
            connection_point_2=1,
        )  # act

        # assert
        self.assertIsInstance(node_name, uuid.UUID)
        self.assertEqual(
            self.network.assets[self.asset.name].get_connected_node(connection_point=0).name,
            node_name,
        )
        self.assertEqual(
            self.network.assets[self.asset2.name].get_connected_node(connection_point=1).name,
            node_name,
        )
        self.assertEqual(len(self.network.nodes), 1)
        self.assertEqual(
            self.network.nodes[node_name].connected_assets,
            [(self.asset, 0), (self.asset2, 1)],
        )

    def test_connect_both_assets_and_replace_node(self) -> None:
        """Test connecting both assets and replacing the node."""
        # arrange
        node = Node(name=uuid.uuid4())
        node2 = Node(name=uuid.uuid4())
        asset3 = SolverPipe(name=uuid.uuid4())
        self.network.nodes[node.name] = node
        self.network.nodes[node2.name] = node2
        self.network.add_existing_asset(asset=self.asset)
        self.network.add_existing_asset(asset=self.asset2)
        self.network.add_existing_asset(asset=asset3)
        self.network.assets[self.asset.name].connect_node(node=node, connection_point=0)
        self.network.assets[self.asset2.name].connect_node(node=node2, connection_point=1)
        self.network.assets[asset3.name].connect_node(node=node, connection_point=0)
        node.connect_asset(asset=self.asset, connection_point=0)
        node.connect_asset(asset=asset3, connection_point=0)
        node2.connect_asset(asset=self.asset2, connection_point=1)

        # act
        node_name = self.network._connect_both_assets_and_replace_node(
            asset1_id=self.asset.name,
            connection_point_1=0,
            asset2_id=self.asset2.name,
            connection_point_2=1,
        )  # act

        # assert
        self.assertIsInstance(node_name, uuid.UUID)
        self.assertEqual(node_name, node.name)
        self.assertEqual(len(self.network.nodes), 1)
        self.assertEqual(self.asset.get_connected_node(connection_point=0).name, node.name)
        self.assertEqual(self.asset2.get_connected_node(connection_point=1).name, node.name)
        self.assertEqual(asset3.get_connected_node(connection_point=0).name, node.name)
        self.assertEqual(
            self.network.nodes[node_name].connected_assets,
            [(self.asset, 0), (asset3, 0), (self.asset2, 1)],
        )

    def test_connect_both_assets_and_replace_node_with_additional_assets(self) -> None:
        """Test connecting both assets and replacing the node."""
        # arrange
        node = Node(name=uuid.uuid4())
        node2 = Node(name=uuid.uuid4())
        asset3 = SolverPipe(name=uuid.uuid4())
        self.network.nodes[node.name] = node
        self.network.nodes[node2.name] = node2
        self.network.add_existing_asset(asset=self.asset)
        self.network.add_existing_asset(asset=self.asset2)
        self.network.add_existing_asset(asset=asset3)
        self.network.assets[self.asset.name].connect_node(node=node, connection_point=0)
        self.network.assets[self.asset2.name].connect_node(node=node2, connection_point=1)
        self.network.assets[asset3.name].connect_node(node=node2, connection_point=0)
        node.connect_asset(asset=self.asset, connection_point=0)
        node2.connect_asset(asset=asset3, connection_point=0)
        node2.connect_asset(asset=self.asset2, connection_point=1)

        # act
        node_name = self.network._connect_both_assets_and_replace_node(
            asset1_id=self.asset.name,
            connection_point_1=0,
            asset2_id=self.asset2.name,
            connection_point_2=1,
        )  # act

        # assert
        self.assertIsInstance(node_name, uuid.UUID)
        self.assertEqual(node_name, node.name)
        self.assertEqual(len(self.network.nodes), 1)
        self.assertEqual(self.asset.get_connected_node(connection_point=0).name, node.name)
        self.assertEqual(self.asset2.get_connected_node(connection_point=1).name, node.name)
        self.assertEqual(asset3.get_connected_node(connection_point=0).name, node.name)
        self.assertEqual(
            self.network.nodes[node_name].connected_assets,
            [(self.asset, 0), (asset3, 0), (self.asset2, 1)]
        )

    def test_connect_both_assets_and_replace_node_same_node(self) -> None:
        """Test connecting both assets and replacing the node with the same node."""
        # arrange
        node = Node(name=uuid.uuid4())
        self.network.nodes[node.name] = node
        self.network.add_existing_asset(asset=self.asset)
        self.network.add_existing_asset(asset=self.asset2)
        self.network.assets[self.asset.name].connect_node(node=node, connection_point=0)
        self.network.assets[self.asset2.name].connect_node(node=node, connection_point=1)
        node.connect_asset(asset=self.asset, connection_point=0)
        node.connect_asset(asset=self.asset2, connection_point=1)

        # act
        node_name = self.network._connect_both_assets_and_replace_node(
            asset1_id=self.asset.name,
            connection_point_1=0,
            asset2_id=self.asset2.name,
            connection_point_2=1,
        )  # act

        # assert
        self.assertIsInstance(node_name, uuid.UUID)
        self.assertEqual(node_name, node.name)
        self.assertEqual(len(self.network.nodes), 1)
        self.assertEqual(self.asset.get_connected_node(connection_point=0).name, node.name)
        self.assertEqual(self.asset2.get_connected_node(connection_point=1).name, node.name)
        self.assertEqual(
            self.network.nodes[node_name].connected_assets,
            [(self.asset, 0), (self.asset2, 1)],
        )

    @patch.object(Network, "_connect_both_assets_and_replace_node")
    @patch.object(Network, "_connect_single_asset_at_node")
    @patch.object(Network, "_connect_both_assets_at_node")
    def test_decision_tree_both_not_connected(
        self,
        mock_connect_both_assets_at_node,
        mock_connect_single_asset_at_node,
        mock_connect_both_assets_and_replace_node,
    ) -> None:
        """Test connecting assets that are not connected."""
        # arrange

        # act
        self.network.connect_assets_decision_tree(
            connected_1=False,
            connected_2=False,
            asset1_id=self.asset.name,
            connection_point_1=0,
            asset2_id=self.asset2.name,
            connection_point_2=1,
        )

        # assert
        self.assertEqual(mock_connect_both_assets_at_node.call_count, 1)
        self.assertEqual(mock_connect_single_asset_at_node.call_count, 0)
        self.assertEqual(mock_connect_both_assets_and_replace_node.call_count, 0)
        self.assertEqual(
            list(mock_connect_both_assets_at_node.call_args[1].values()),
            [self.asset.name, 0, self.asset2.name, 1],
        )

    @patch.object(Network, "_connect_both_assets_and_replace_node")
    @patch.object(Network, "_connect_single_asset_at_node")
    @patch.object(Network, "_connect_both_assets_at_node")
    def test_decision_tree_both_connected(
        self,
        mock_connect_both_assets_at_node,
        mock_connect_single_asset_at_node,
        mock_connect_both_assets_and_replace_node,
    ) -> None:
        """Test connecting assets that are connected."""
        # arrange

        # act
        self.network.connect_assets_decision_tree(
            connected_1=True,
            connected_2=True,
            asset1_id=self.asset.name,
            connection_point_1=0,
            asset2_id=self.asset2.name,
            connection_point_2=1,
        )

        # assert
        self.assertEqual(mock_connect_both_assets_at_node.call_count, 0)
        self.assertEqual(mock_connect_single_asset_at_node.call_count, 0)
        self.assertEqual(mock_connect_both_assets_and_replace_node.call_count, 1)
        self.assertEqual(
            list(mock_connect_both_assets_and_replace_node.call_args[1].values()),
            [self.asset.name, 0, self.asset2.name, 1],
        )

    @patch.object(Network, "_connect_both_assets_and_replace_node")
    @patch.object(Network, "_connect_single_asset_at_node")
    @patch.object(Network, "_connect_both_assets_at_node")
    def test_decision_tree_asset1_connected_asset2_not_connected(
        self,
        mock_connect_both_assets_at_node,
        mock_connect_single_asset_at_node,
        mock_connect_both_assets_and_replace_node,
    ) -> None:
        """Test connecting assets where asset 1 is connected and asset 2 is not connected."""
        # arrange

        # act
        self.network.connect_assets_decision_tree(
            connected_1=True,
            connected_2=False,
            asset1_id=self.asset.name,
            connection_point_1=0,
            asset2_id=self.asset2.name,
            connection_point_2=1,
        )

        # assert
        self.assertEqual(mock_connect_both_assets_at_node.call_count, 0)
        self.assertEqual(mock_connect_single_asset_at_node.call_count, 1)
        self.assertEqual(mock_connect_both_assets_and_replace_node.call_count, 0)
        self.assertEqual(
            list(mock_connect_single_asset_at_node.call_args[1].values()),
            [self.asset.name, 0, self.asset2.name, 1],
        )

    @patch.object(Network, "_connect_both_assets_and_replace_node")
    @patch.object(Network, "_connect_single_asset_at_node")
    @patch.object(Network, "_connect_both_assets_at_node")
    def test_decision_tree_asset1_not_connected_asset2_connected(
        self,
        mock_connect_both_assets_at_node,
        mock_connect_single_asset_at_node,
        mock_connect_both_assets_and_replace_node,
    ) -> None:
        """Test connecting assets where asset 1 is not connected and asset 2 is connected."""
        # arrange

        # act
        self.network.connect_assets_decision_tree(
            connected_1=False,
            connected_2=True,
            asset1_id=self.asset.name,
            connection_point_1=0,
            asset2_id=self.asset2.name,
            connection_point_2=1,
        )

        # assert
        self.assertEqual(mock_connect_both_assets_at_node.call_count, 0)
        self.assertEqual(mock_connect_single_asset_at_node.call_count, 1)
        self.assertEqual(mock_connect_both_assets_and_replace_node.call_count, 0)
        self.assertEqual(
            list(mock_connect_single_asset_at_node.call_args[1].values()),
            [self.asset2.name, 1, self.asset.name, 0],
        )

    def test_exists_asset(self) -> None:
        """Test exists asset method."""
        # arrange
        self.network.add_existing_asset(asset=self.asset)

        # act
        result = self.network.exists_asset(asset_id=self.asset.name)

        # assert
        self.assertTrue(result)

    def test_exist_asset_raise_error(self) -> None:
        """Test exist asset method raise value error."""
        # arrange

        # act
        with self.assertRaises(ValueError) as cm:
            self.network.exists_asset(asset_id=self.asset.name)

        # assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            str(cm.exception), f"Asset with id:{self.asset.name} does not exist in network."
        )

    def test_exists_node(self) -> None:
        """Test exist node method."""
        # arrange
        node = Node(name=uuid.uuid4())
        self.network.nodes[node.name] = node

        # act
        result = self.network.exists_node(node_id=node.name)

        # assert
        self.assertTrue(result)

    def test_exists_node_raise_error(self) -> None:
        """Test exist node method raise value error."""
        # arrange

        # act
        with self.assertRaises(ValueError) as cm:
            self.network.exists_node(node_id=self.node.name)

        # assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            str(cm.exception), f"Node with id:{self.node.name} does not exist in network."
        )

    def test_get_asset(self) -> None:
        """Test get asset method."""
        # arrange
        self.network.add_existing_asset(asset=self.asset)

        # act
        result = self.network.get_asset(asset_id=self.asset.name)

        # assert
        self.assertEqual(result, self.asset)

    def test_get_node(self) -> None:
        """Test get node method."""
        # arrange
        self.network.nodes[self.node.name] = self.node

        # act
        result = self.network.get_node(node_id=self.node.name)

        # assert
        self.assertEqual(result, self.node)

    def test_set_result_asset(self) -> None:
        """Test set result asset method."""
        # arrange
        solution = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        asset2 = SolverPipe(name=uuid.uuid4())
        self.network.add_existing_asset(asset=self.asset)
        self.network.add_existing_asset(asset=asset2)
        self.asset.matrix_index = 0
        asset2.matrix_index = 6

        # act
        self.network.set_result_asset(solution=solution)  # act

        # assert
        self.assertEqual(self.asset.prev_sol, solution[:6])
        self.assertEqual(asset2.prev_sol, solution[6:])

    def test_set_results_node(self) -> None:
        """Test set result node method."""
        # arrange
        solution = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        node = Node(name=uuid.uuid4())
        self.network.nodes[self.node.name] = self.node
        self.network.nodes[node.name] = node
        self.node.matrix_index = 0
        node.matrix_index = 9

        # act
        self.network.set_result_node(solution=solution)  # act

        # assert
        self.assertEqual(self.node.prev_sol, solution[:3])
        self.assertEqual(node.prev_sol, solution[9:12])

    def test_connectivity_assets(self) -> None:
        """Test connectivity assets method."""
        # arrange
        node = Node(name=uuid.uuid4())
        self.network.add_existing_asset(asset=self.asset)
        self.network.add_existing_asset(asset=self.asset2)
        self.network.nodes[self.node.name] = self.node
        self.asset.connect_node(node=self.node, connection_point=0)
        self.asset2.connect_node(node=self.node, connection_point=1)
        self.asset.connect_node(node=node, connection_point=1)
        self.asset2.connect_node(node=node, connection_point=0)

        # act
        result = self.network.check_connectivity_assets()

        # assert
        self.assertTrue(result)

    def test_connectivity_assets_false(self) -> None:
        """Test connectivity assets method."""
        # arrange
        self.network.add_existing_asset(asset=self.asset)
        self.network.add_existing_asset(asset=self.asset2)
        self.asset.connect_node(node=self.node, connection_point=0)
        self.asset2.connect_node(node=self.node, connection_point=1)

        # act
        result = self.network.check_connectivity_assets()

        # assert
        self.assertFalse(result)

    def test_connectivity_nodes(self) -> None:
        """Test connectivity nodes method."""
        # arrange
        self.network.add_existing_asset(asset=self.asset)
        self.network.add_existing_asset(asset=self.asset2)
        self.network.nodes[self.node.name] = self.node
        self.asset.connect_node(node=self.node, connection_point=0)
        self.asset2.connect_node(node=self.node, connection_point=1)
        self.node.connect_asset(asset=self.asset, connection_point=0)
        self.node.connect_asset(asset=self.asset2, connection_point=1)

        # act
        result = self.network.check_connectivity_nodes()

        # assert
        self.assertTrue(result)

    def test_connectivity_nodes_false(self) -> None:
        """Test connectivity nodes method."""
        # arrange
        self.network.add_existing_asset(asset=self.asset)
        self.network.add_existing_asset(asset=self.asset2)
        self.network.nodes[self.node.name] = self.node
        self.asset.connect_node(node=self.node, connection_point=0)
        self.asset2.connect_node(node=self.node, connection_point=1)

        # act
        result = self.network.check_connectivity_nodes()

        # assert
        self.assertFalse(result)

    @patch.object(Network, "check_connectivity_nodes")
    @patch.object(Network, "check_connectivity_assets")
    def test_check_connectivity(
        self, mock_check_connectivity_assets, mock_check_connectivity_nodes
    ) -> None:
        """Test check connectivity method."""
        # arrange
        mock_check_connectivity_assets.return_value = True
        mock_check_connectivity_nodes.return_value = True

        # act
        result = self.network.check_connectivity()

        # assert
        self.assertTrue(result)

    @patch.object(Network, "check_connectivity_nodes")
    @patch.object(Network, "check_connectivity_assets")
    def test_check_connectivity_false(
        self, mock_check_connectivity_assets, mock_check_connectivity_nodes
    ) -> None:
        """Test check connectivity method."""
        # arrange
        mock_check_connectivity_assets.return_value = False
        mock_check_connectivity_nodes.return_value = False

        # act
        result = self.network.check_connectivity()

        # assert
        self.assertFalse(result)

    @patch.object(Network, "check_connectivity_nodes")
    @patch.object(Network, "check_connectivity_assets")
    def test_check_connectivity_false_assets(
        self, mock_check_connectivity_assets, mock_check_connectivity_nodes
    ) -> None:
        """Test check connectivity method."""
        # arrange
        mock_check_connectivity_assets.return_value = False
        mock_check_connectivity_nodes.return_value = True

        # act
        result = self.network.check_connectivity()

        # assert
        self.assertFalse(result)

    @patch.object(SolverPipe, "get_result")
    @patch("sys.stdout", new_callable=StringIO)
    def test_print_result(self, mock_stdout, mock_get_result) -> None:
        """Test get results method."""
        # arrange
        mock_get_result.return_value = [1, 2, 3, 4, 5, 6]
        self.network.add_existing_asset(asset=self.asset)

        # act
        self.network.print_result()  # act

        # assert
        self.assertEqual(
            mock_stdout.getvalue(), f"{type(self.asset)}\n{mock_get_result.return_value}\n"
        )
