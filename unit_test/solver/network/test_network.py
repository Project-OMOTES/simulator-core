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


class NetworkTest(unittest.TestCase):
    """Class to test network class."""

    def test_init(self):
        """Test the constructor of the network class."""
        # arrange

        # act
        network = Network()

        # assert
        self.assertEqual(network.assets, {})
        self.assertEqual(network.nodes, {})

    def test_add_asset_name(self):
        """Test adding an asset with a name."""
        # arrange
        network = Network()
        asset = "Pipe"
        asset_name = uuid.uuid4()

        # act
        name = network.add_asset(asset, asset_name)

        # assert
        self.assertEqual(name, asset_name)
        self.assertTrue(isinstance(network.assets[name], SolverPipe))

    def test_add_asset_no_name(self):
        """Test adding an asset without a name."""
        # arrange
        network = Network()
        asset = "Pipe"

        # act
        name = network.add_asset(asset)

        # assert
        self.assertTrue(isinstance(network.assets[name], SolverPipe))

    def test_add_asset_unkown_asset(self):
        """Test adding an unknown asset."""
        # arrange
        network = Network()
        asset = "unknown asset"

        # act
        with self.assertRaises(ValueError):
            network.add_asset(asset)

    def test_add_existing_asset(self):
        """Test adding an existing asset."""
        # arrange
        network = Network()
        asset = SolverPipe(uuid.uuid4())

        # act
        network.add_existing_asset(asset)

        # assert
        self.assertTrue(asset.name in network.assets)
        self.assertEqual(network.assets[asset.name], asset)

    def test_connect_assets_not_connected(self):
        """Test connecting assets."""
        # arrange
        network = Network()
        asset1 = SolverPipe(uuid.uuid4())
        asset2 = SolverPipe(uuid.uuid4())
        network.add_existing_asset(asset1)
        network.add_existing_asset(asset2)

        # act
        node = network.connect_assets(asset1.name, 0, asset2.name, 1)

        # assert
        self.assertTrue(node in network.nodes)
        self.assertTrue(asset1.is_connected(0))
        self.assertTrue(asset2.is_connected(1))

    def test_connect_assets_already_connected(self):
        """Test connecting assets that are already connected."""
        # arrange
        network = Network()
        asset1 = SolverPipe(uuid.uuid4())
        asset2 = SolverPipe(uuid.uuid4())
        asset3 = SolverPipe(uuid.uuid4())
        network.add_existing_asset(asset1)
        network.add_existing_asset(asset2)
        network.add_existing_asset(asset3)
        node1 = network.connect_assets(asset1.name, 0,
                                       asset2.name, 1)

        # act
        node2 = network.connect_assets(asset1.name, 0,
                                       asset3.name, 1)

        # assert
        self.assertEqual(node1, node2)
