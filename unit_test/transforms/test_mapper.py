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
"""Test energy system mapper class."""
import unittest
from pathlib import Path
from typing import List, Tuple

from omotes_simulator_core.adapter.transforms.mappers import (
    EsdlEnergySystemMapper,
    replace_joint_in_connected_assets,
)
from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.junction import Junction
from omotes_simulator_core.entities.assets.utils import Port
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file
from omotes_simulator_core.solver.network.network import Network


class EsdlEnergySystemMapperTest(unittest.TestCase):
    """Class to test energy system mapper class."""

    def test_to_entity(self):
        """Method to test the to entity mapper class."""
        # act
        esdl_file_path = Path(__file__).parent / ".." / ".." / "testdata" / "test1.esdl"
        esdl_file_path = str(esdl_file_path)
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        network = Network()

        # arrange
        result = EsdlEnergySystemMapper(esdl_object).to_entity(network)

        # assert
        self.assertIsInstance(result, Tuple)
        self.assertIsInstance(result[0], List)
        self.assertIsInstance(result[0][0], AssetAbstract)
        self.assertIsInstance(result[1], List)
        self.assertIsInstance(result[1][0], Junction)
        self.assertEqual(len(result[0]), 4)
        self.assertEqual(len(result[1]), 4)

    def test_replace_joint_in_connected_assets(self):
        """Method to test the replace joint in connected assets method."""
        # act
        connected_py_assets = [("joint1", "Port1.In"), ("asset2", "Port2.Out")]
        py_joint_dict = {"joint1": [("asset1", "Port1.In"), ("asset3", "Port3.Out")]}
        py_asset_id = "joint1"

        # arrange
        new_py_assets = replace_joint_in_connected_assets(
            connected_py_assets, py_joint_dict, py_asset_id
        )
        new_py_assets.sort()

        # assert
        self.assertEqual(
            new_py_assets,
            [("asset1", "Port1.In"), ("asset2", "Port2.Out"), ("asset3", "Port3.Out")],
        )

    def test_replace_joint_in_connected_assets_error(self):
        """Method to test error handling of the replace."""
        # act
        connected_py_assets = [("joint1", "Port1.In"), ("asset1", "Port1.Out")]
        py_joint_dict = {
            "joint1": [("joint2", "Port2.In"), ("asset2", "Port2.Out")],
            "joint2": [("joint3", "Port3.In"), ("asset3", "Port3.Out")],
            "joint3": [("asset4", "Port4.In"), ("asset5", "Port5.Out")],
        }
        py_asset_id = "joint1"

        # arrange
        with self.assertRaises(RuntimeError) as cm:
            # ("Error in replacing joint in connected assets.")
            replace_joint_in_connected_assets(
                connected_py_assets=connected_py_assets,
                py_joint_dict=py_joint_dict,
                py_asset_id=py_asset_id,
                iteration_limit=1,
            )

        # assert
        self.assertIsInstance(cm.exception, RuntimeError)
        self.assertEqual(cm.exception.args[0], "Error in replacing joint in connected assets.")

    def test_component_with_4_connection_points(self):
        """Method to test the to entity mapper class with 4 connection points in a asset."""
        esdl_file_path = Path(__file__).parent / ".." / ".." / "testdata" / "simple_heat_pump.esdl"
        esdl_file_path = str(esdl_file_path)
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        network = Network()

        # arrange
        result = EsdlEnergySystemMapper(esdl_object).to_entity(network)

        # assert
        self.assertIsInstance(result[0][0], AssetAbstract)
        self.assertIsInstance(result[1], List)
        self.assertIsInstance(result[1][0], Junction)
        self.assertEqual(len(result[0]), 3)
        self.assertEqual(len(result[1]), 4)
