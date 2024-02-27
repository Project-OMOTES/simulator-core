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

from simulator_core.solver.network.network import Network
from simulator_core.solver.network.assets.solver_pipe import SolverPipe
from simulator_core.solver.network.assets.node import Node


class NetworkTest(unittest.TestCase):
    """Class to test network class."""

    def setUp(self) -> None:
        """Set up for the tests."""
        self.network = Network()
        self.asset = SolverPipe(uuid.uuid4())
        self.node = Node(uuid.uuid4())

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
        name = self.network.add_asset(asset, asset_name)  # act

        # assert
        self.assertEqual(name, asset_name)
        self.assertIsInstance(self.network.assets[name], SolverPipe)

    def test_add_asset_no_name(self) -> None:
        """Test adding an asset without a name."""
        # arrange
        asset = "Pipe"

        # act
        name = self.network.add_asset(asset)  # act

        # assert
        self.assertIsInstance(self.network.assets[name], SolverPipe)

    def test_add_asset_unknown_asset(self) -> None:
        """Test adding an unknown asset."""
        # arrange
        asset = "unknown asset"

        # act
        with self.assertRaises(ValueError) as cm:
            self.network.add_asset(asset)

        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(str(cm.exception), f"{asset} not recognized")

    def test_add_existing_asset(self) -> None:
        """Test adding an existing asset."""
        # arrange

        # act
        self.network.add_existing_asset(self.asset)  # act

        # assert
        self.assertTrue(self.asset.name in self.network.assets)
        self.assertEqual(self.network.assets[self.asset.name], self.asset)

    def test_connect_assets_not_connected(self) -> None:
        """Test connecting assets, which are initially both not connected."""
        # arrange
        asset2 = SolverPipe(uuid.uuid4())
        self.network.add_existing_asset(self.asset)
        self.network.add_existing_asset(asset2)

        # act
        node = self.network.connect_assets(self.asset.name, 0, asset2.name, 1)  # act

        # assert
        self.assertTrue(node in self.network.nodes)
        self.assertTrue(self.asset.is_connected(0))
        self.assertTrue(asset2.is_connected(1))

    def test_connect_assets_one_already_connected(self) -> None:
        """Test connecting assets that are both already connected."""
        # arrange
        asset2 = SolverPipe(uuid.uuid4())
        asset3 = SolverPipe(uuid.uuid4())
        self.network.add_existing_asset(self.asset)
        self.network.add_existing_asset(asset2)
        self.network.add_existing_asset(asset3)
        node1 = self.network.connect_assets(self.asset.name, 0,
                                            asset2.name, 1)

        # act
        node2 = self.network.connect_assets(self.asset.name, 0,
                                            asset3.name, 1)  # act

        # assert
        self.assertEqual(node1, node2)
        self.assertTrue(self.asset.is_connected(0))
        self.assertTrue(asset3.is_connected(1))

    def test_connect_assets_both_already_connected(self) -> None:
        """Test connecting assets that are both already connected."""
        # arrange
        self.network = Network()
        asset2 = SolverPipe(uuid.uuid4())
        asset3 = SolverPipe(uuid.uuid4())
        asset4 = SolverPipe(uuid.uuid4())
        self.network.add_existing_asset(self.asset)
        self.network.add_existing_asset(asset2)
        self.network.add_existing_asset(asset3)
        self.network.add_existing_asset(asset4)
        node1 = self.network.connect_assets(self.asset.name, 0,
                                            asset2.name, 1)
        node2 = self.network.connect_assets(asset3.name, 0,
                                            asset4.name, 1)

        # act
        node3 = self.network.connect_assets(self.asset.name, 0,
                                            asset3.name, 0)  # act

        # assert
        self.assertFalse(self.network.exists_node(node2))
        self.assertEqual(node1, node3)

    def test_connecting_assets_error(self) -> None:
        """Test connect asset method raise value since asset does not exist in network."""
        # arrange
        asset2 = SolverPipe(uuid.uuid4())

        # act
        with self.assertRaises(ValueError) as cm:
            self.network.connect_assets(self.asset.name, 0, asset2.name, 1)

        # assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(str(cm.exception), f"{self.asset} +  does not exists in network.")

    def test_exists_asset(self) -> None:
        """Test exists asset method."""
        # arrange
        self.network.add_existing_asset(self.asset)

        # act
        result = self.network.exists_asset(self.asset.name)

        # assert
        self.assertTrue(result)

    def test_exists_node(self) -> None:
        """Test exist node method."""
        # arrange
        node = Node(uuid.uuid4())
        self.network.nodes[node.name] = node

        # act
        result = self.network.exists_node(node.name)

        # assert
        self.assertTrue(result)

    def test_get_asset(self) -> None:
        """Test get asset method."""
        # arrange
        self.network.add_existing_asset(self.asset)

        # act
        result = self.network.get_asset(self.asset.name)

        # assert
        self.assertEqual(result, self.asset)

    def test_get_node(self) -> None:
        """Test get node method."""
        # arrange
        self.network.nodes[self.node.name] = self.node

        # act
        result = self.network.get_node(self.node.name)

        # assert
        self.assertEqual(result, self.node)

    def test_get_asset_error(self) -> None:
        """Test get asset method raise value error."""
        # arrange

        # act
        with self.assertRaises(ValueError) as cm:
            self.network.get_asset(self.asset.name)

        # assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(str(cm.exception), f"{self.asset.name} Not a valid asset id")

    def test_get_node_error(self) -> None:
        """Test get node method raise value error."""
        # arrange

        # act
        with self.assertRaises(ValueError) as cm:
            self.network.get_node(self.node.name)

        # assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(str(cm.exception), f"{self.node.name} Not a valid node id")
        pass

    def test_set_result_asset(self) -> None:
        """Test set result asset method."""
        # arrange
        solution = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        asset2 = SolverPipe(uuid.uuid4())
        self.network.add_existing_asset(self.asset)
        self.network.add_existing_asset(asset2)
        self.asset.matrix_index = 0
        asset2.matrix_index = 6

        # act
        self.network.set_result_asset(solution)  # act

        # assert
        self.assertEqual(self.asset.prev_sol, solution[:6])
        self.assertEqual(asset2.prev_sol, solution[6:])

    def test_set_results_node(self) -> None:
        """Test set result node method."""
        # arrange
        solution = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        node = Node(uuid.uuid4())
        self.network.nodes[self.node.name] = self.node
        self.network.nodes[node.name] = node
        self.node.matrix_index = 0
        node.matrix_index = 9

        # act
        self.network.set_result_node(solution)  # act

        # assert
        self.assertEqual(self.node.prev_sol, solution[:3])
        self.assertEqual(node.prev_sol, solution[9:12])
