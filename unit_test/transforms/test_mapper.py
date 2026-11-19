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

from esdl import esdl

from omotes_simulator_core.adapter.transforms.mappers import (
    EsdlEnergySystemMapper,
    replace_joint_in_connected_assets,
)
from omotes_simulator_core.adapter.transforms.string_to_esdl import OmotesAssetLabels
from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.asset_defaults import DEFAULT_TEMPERATURE
from omotes_simulator_core.entities.assets.junction import Junction
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
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][0], AssetAbstract)
        self.assertIsInstance(result[1], list)
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
        # arrange
        esdl_file_path = Path(__file__).parent / ".." / ".." / "testdata" / "simple_heat_pump.esdl"
        esdl_file_path = str(esdl_file_path)
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        network = Network()

        # act
        asset_list, junction_list = EsdlEnergySystemMapper(esdl_object).to_entity(network)

        # assert
        self.assertIsInstance(asset_list, list)
        self.assertTrue(all(isinstance(item, AssetAbstract) for item in asset_list))

        self.assertIsInstance(junction_list, list)
        self.assertTrue(all(isinstance(item, Junction) for item in junction_list))

        self.assertEqual(len(asset_list), 3)
        self.assertEqual(len(junction_list), 4)


class JunctionTemperatureTest(unittest.TestCase):
    """Class to test setting the initial junction temperature from the esdl carriers."""

    consumer_id = "48f3e425-2143-4dcd-9101-c7e22559e82b"
    consumer_in = "af0904f7-ba1f-4e79-9040-71e08041601b"
    consumer_out = "e890f65f-80e7-46fa-8c52-5385324bf686"
    producer_id = "cf3d4b5e-437f-4c1b-a7f9-7fd7e8a269b4"
    producer_in = "9c258b9d-3149-4720-8931-f4bef1080ec1"
    producer_out = "2d818e3d-8a39-4cec-afa0-f6dbbfd50696"

    def setUp(self):
        """Load the test1 esdl file."""
        esdl_file_path = Path(__file__).parent / ".." / ".." / "testdata" / "test1.esdl"
        self.esdl_object = EsdlObject(pyesdl_from_file(str(esdl_file_path)))

    def _set_single_carrier(self, carrier: esdl.HeatCommodity) -> None:
        """Assign the given carrier to all ports in the energy system."""
        energy_system = self.esdl_object.energy_system_handler.energy_system
        energy_system.energySystemInformation.carriers.carrier.append(carrier)
        for asset in self.esdl_object.get_all_assets_of_type(OmotesAssetLabels.ASSET):
            for port in asset.esdl_asset.port:
                port.carrier = carrier

    def _get_node_temperatures(self) -> dict[str, float]:
        """Run the mapper and return the node temperature per (asset id, port id)."""
        network = Network()
        asset_list, junction_list = EsdlEnergySystemMapper(self.esdl_object).to_entity(network)
        temperatures = {}
        for asset in asset_list:
            for con_point, port_id in enumerate(asset.connected_ports):
                node = asset.solver_asset.get_connected_node(con_point)
                temperatures[port_id] = node.initial_temperature
        for junction in junction_list:
            self.assertEqual(junction.tfluid_k, junction.solver_junction.initial_temperature)
        return temperatures

    def test_separate_supply_and_return_carriers(self):
        """Nodes get the temperature of the only temperature set on their carrier."""
        # act
        temperatures = self._get_node_temperatures()

        # assert
        self.assertAlmostEqual(temperatures[self.producer_out], 80.0 + 273.15)
        self.assertAlmostEqual(temperatures[self.consumer_in], 80.0 + 273.15)
        self.assertAlmostEqual(temperatures[self.consumer_out], 40.0 + 273.15)
        self.assertAlmostEqual(temperatures[self.producer_in], 40.0 + 273.15)

    def test_single_carrier_with_both_temperatures(self):
        """Nodes get the supply or return temperature based on the side of the network."""
        # arrange
        self._set_single_carrier(
            esdl.HeatCommodity(id="both", supplyTemperature=70.0, returnTemperature=30.0)
        )

        # act
        temperatures = self._get_node_temperatures()

        # assert
        self.assertAlmostEqual(temperatures[self.producer_out], 70.0 + 273.15)
        self.assertAlmostEqual(temperatures[self.consumer_in], 70.0 + 273.15)
        self.assertAlmostEqual(temperatures[self.consumer_out], 30.0 + 273.15)
        self.assertAlmostEqual(temperatures[self.producer_in], 30.0 + 273.15)

    def test_carrier_without_temperatures(self):
        """Nodes keep the default temperature when no temperature is set on the carrier."""
        # arrange
        self._set_single_carrier(esdl.HeatCommodity(id="empty"))

        # act
        temperatures = self._get_node_temperatures()

        # assert
        for temperature in temperatures.values():
            self.assertAlmostEqual(temperature, DEFAULT_TEMPERATURE)

    def test_undetermined_side_uses_supply_temperature(self):
        """When the side can not be determined the supply temperature is used with a warning."""
        # arrange
        self._set_single_carrier(
            esdl.HeatCommodity(id="both", supplyTemperature=70.0, returnTemperature=30.0)
        )
        mapper = EsdlEnergySystemMapper(self.esdl_object)

        # act
        with self.assertLogs(level="WARNING"):
            temperature = mapper._determine_node_temperature(
                [(self.consumer_id, self.consumer_out)], {}
            )

        # assert
        self.assertAlmostEqual(temperature, 70.0 + 273.15)
