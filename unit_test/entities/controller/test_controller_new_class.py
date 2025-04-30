#  Copyright (c) 2024. Deltares & TNO
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
"""Test controller class."""
import datetime
import unittest
from unittest.mock import Mock
from omotes_simulator_core.entities.network_controller_new import NetworkControllerNew
from omotes_simulator_core.entities.assets.controller.controller_network import ControllerNetwork
from omotes_simulator_core.entities.assets.controller.controller_producer import ControllerProducer
from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_HEAT_DEMAND,
)


class ControllerTest(unittest.TestCase):
    """Testcase for Controller class."""

    def setUp(self):
        """Set up the test case."""
        self.network1 = Mock(spec=ControllerNetwork)
        self.network2 = Mock(spec=ControllerNetwork)
        self.network3 = Mock(spec=ControllerNetwork)
        self.network1.path = ["0"]
        self.network2.path = ["1", "0"]
        self.network3.path = ["2", "1", "0"]
        self.network1.heat_transfer_assets_prim = []
        self.network2.heat_transfer_assets_prim = []
        self.network3.heat_transfer_assets_prim = []
        self.network1.heat_transfer_assets_sec = []
        self.network2.heat_transfer_assets_sec = []
        self.network3.heat_transfer_assets_sec = []
        self.networks = [self.network1, self.network2, self.network3]
        self.controller = NetworkControllerNew(networks=self.networks)

    def test_init(self):
        # arrange

        # act

        # assert
        self.assertEqual(self.controller.networks, self.networks)

    def test_update_networks_factor_prim(self):
        # arrange
        mock_heat_trans_asset1 = Mock()
        mock_heat_trans_asset1.factor = 1
        mock_heat_trans_asset2 = Mock()
        mock_heat_trans_asset2.factor = 2
        mock_heat_trans_asset3 = Mock()
        mock_heat_trans_asset3.factor = 3
        self.network1.heat_transfer_assets_prim = [mock_heat_trans_asset1]
        self.network2.heat_transfer_assets_prim = [mock_heat_trans_asset2]
        self.network3.heat_transfer_assets_prim = [mock_heat_trans_asset3]
        # act
        self.controller.update_networks_factor()
        # assert
        self.assertEqual(self.network1.factor, 1)
        self.assertEqual(self.network2.factor, 2)
        self.assertEqual(self.network3.factor, 6)

    def test_update_networks_factor_sec(self):
        # arrange
        mock_heat_trans_asset1 = Mock()
        mock_heat_trans_asset1.factor = 1
        mock_heat_trans_asset2 = Mock()
        mock_heat_trans_asset2.factor = 2
        mock_heat_trans_asset3 = Mock()
        mock_heat_trans_asset3.factor = 3
        self.network1.heat_transfer_assets_sec = [mock_heat_trans_asset1]
        self.network2.heat_transfer_assets_sec = [mock_heat_trans_asset2]
        self.network3.heat_transfer_assets_sec = [mock_heat_trans_asset3]
        # act
        self.controller.update_networks_factor()
        # assert
        self.assertEqual(self.network1.factor, 1)
        self.assertEqual(self.network2.factor, 0.5)
        self.assertEqual(self.network3.factor, 0.16666666666666666)

    def test_update_setpoints(self):
        # arrange

        # act

        # assert
        pass

    def test__set_producers_to_max(self):
        # arrange
        self.controller.networks[0].set_supply_to_max = Mock(return_value={"test": 1})
        self.controller.networks[1].set_supply_to_max = Mock(return_value={"test1": 2})
        self.controller.networks[2].set_supply_to_max = Mock(return_value={"test2": 3})
        # act
        result = self.controller._set_producers_to_max()
        # assert
        self.assertEqual(
            result,
            {
                "test": 1,
                "test1": 2,
                "test2": 3,
            },
        )

    def test__set_all_storages_discharge_to_max(self):
        # arrange
        self.controller.networks[0].set_all_storages_discharge_to_max = Mock(
            return_value={"test": 1}
        )
        self.controller.networks[1].set_all_storages_discharge_to_max = Mock(
            return_value={"test1": 2}
        )
        self.controller.networks[2].set_all_storages_discharge_to_max = Mock(
            return_value={"test2": 3}
        )
        # act
        result = self.controller._set_all_storages_discharge_to_max()
        # assert
        self.assertEqual(
            result,
            {
                "test": 1,
                "test1": 2,
                "test2": 3,
            },
        )

    def test__set_all_storages_charge_to_max(self):
        # arrange
        self.controller.networks[0].set_all_storages_charge_to_max = Mock(return_value={"test": 1})
        self.controller.networks[1].set_all_storages_charge_to_max = Mock(return_value={"test1": 2})
        self.controller.networks[2].set_all_storages_charge_to_max = Mock(return_value={"test2": 3})
        # act
        result = self.controller._set_all_storages_charge_to_max()
        # assert
        self.assertEqual(
            result,
            {
                "test": 1,
                "test1": 2,
                "test2": 3,
            },
        )

    def test__set_consumer_to_demand(self):
        # arrange
        self.controller.networks[0].set_consumer_to_demand = Mock(return_value={"test": 1})
        self.controller.networks[1].set_consumer_to_demand = Mock(return_value={"test1": 2})
        self.controller.networks[2].set_consumer_to_demand = Mock(return_value={"test2": 3})
        # act
        result = self.controller._set_consumer_to_demand(time=datetime.datetime.now(), factor=1)
        # assert
        self.assertEqual(
            result,
            {
                "test": 1,
                "test1": 2,
                "test2": 3,
            },
        )

    def test__set_producers_based_on_priority(self):
        # arrange
        producer1 = ControllerProducer(
            name="producer1",
            identifier="producer1",
            temperature_supply=50,
            temperature_return=40,
            power=50,
            marginal_costs=1,
            priority=2,
        )
        producer2 = ControllerProducer(
            name="producer2",
            identifier="producer2",
            temperature_supply=50,
            temperature_return=40,
            power=40,
            marginal_costs=1,
            priority=3,
        )
        producer3 = ControllerProducer(
            name="producer3",
            identifier="producer3",
            temperature_supply=50,
            temperature_return=40,
            power=40,
            marginal_costs=1,
            priority=1,
        )
        producer4 = ControllerProducer(
            name="producer4",
            identifier="producer4",
            temperature_supply=50,
            temperature_return=40,
            power=20,
            marginal_costs=1,
            priority=3,
        )
        self.controller.networks[0] = ControllerNetwork(
            heat_transfer_assets_prim_in=[],
            heat_transfer_assets_sec_in=[],
            consumers_in=[],
            producers_in=[producer1, producer2],
            storages_in=[],
        )

        self.controller.networks[1] = ControllerNetwork(
            heat_transfer_assets_prim_in=[],
            heat_transfer_assets_sec_in=[],
            consumers_in=[],
            producers_in=[producer3],
            storages_in=[],
        )
        self.controller.networks[2] = ControllerNetwork(
            heat_transfer_assets_prim_in=[],
            heat_transfer_assets_sec_in=[],
            consumers_in=[],
            producers_in=[producer4],
            storages_in=[],
        )
        # act
        result = self.controller._set_producers_based_on_priority(120)

        # assert
        self.assertEqual(result["producer1"][PROPERTY_HEAT_DEMAND], 50)
        self.assertEqual(result["producer2"][PROPERTY_HEAT_DEMAND], 20)
        self.assertEqual(result["producer3"][PROPERTY_HEAT_DEMAND], 40)
        self.assertEqual(result["producer4"][PROPERTY_HEAT_DEMAND], 10)

    def test__get_total_supply_priority(self):
        # arrange
        producer1 = ControllerProducer(
            name="producer1",
            identifier="producer1",
            temperature_supply=50,
            temperature_return=40,
            power=50,
            marginal_costs=1,
            priority=2,
        )
        producer2 = ControllerProducer(
            name="producer2",
            identifier="producer2",
            temperature_supply=50,
            temperature_return=40,
            power=40,
            marginal_costs=1,
            priority=3,
        )
        producer3 = ControllerProducer(
            name="producer3",
            identifier="producer3",
            temperature_supply=50,
            temperature_return=40,
            power=40,
            marginal_costs=1,
            priority=1,
        )
        producer4 = ControllerProducer(
            name="producer4",
            identifier="producer4",
            temperature_supply=50,
            temperature_return=40,
            power=20,
            marginal_costs=1,
            priority=3,
        )
        self.controller.networks[0] = ControllerNetwork(
            heat_transfer_assets_prim_in=[],
            heat_transfer_assets_sec_in=[],
            consumers_in=[],
            producers_in=[producer1, producer2],
            storages_in=[],
        )

        self.controller.networks[1] = ControllerNetwork(
            heat_transfer_assets_prim_in=[],
            heat_transfer_assets_sec_in=[],
            consumers_in=[],
            producers_in=[producer3],
            storages_in=[],
        )
        self.controller.networks[2] = ControllerNetwork(
            heat_transfer_assets_prim_in=[],
            heat_transfer_assets_sec_in=[],
            consumers_in=[],
            producers_in=[producer4],
            storages_in=[],
        )
        # act
        result = self.controller._get_total_supply_priority(2)
        # assert
        self.assertEqual(result, 50)
