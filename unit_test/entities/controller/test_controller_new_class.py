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

from omotes_simulator_core.entities.assets.asset_defaults import (
    PRIMARY,
    PROPERTY_HEAT_DEMAND,
    SECONDARY,
)
from omotes_simulator_core.entities.assets.controller.controller_consumer import (
    ControllerConsumer,
)
from omotes_simulator_core.entities.assets.controller.controller_heat_transfer import (
    ControllerHeatTransferAsset,
)
from omotes_simulator_core.entities.assets.controller.controller_network import (
    ControllerNetwork,
)
from omotes_simulator_core.entities.assets.controller.controller_producer import (
    ControllerProducer,
)
from omotes_simulator_core.entities.assets.controller.controller_storage import (
    ControllerStorage,
)
from omotes_simulator_core.entities.network_controller import NetworkControllerNew


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

    def setup_update_set_points(self):
        producer1 = ControllerProducer(
            name="producer1",
            identifier="producer1",
            temperature_out=50,
            temperature_in=40,
            power=50,
            marginal_costs=1,
            priority=2,
        )
        producer2 = ControllerProducer(
            name="producer2",
            identifier="producer2",
            temperature_out=50,
            temperature_in=40,
            power=40,
            marginal_costs=1,
            priority=3,
        )
        consumer1 = Mock(spec=ControllerConsumer)
        consumer1.id = "consumer1"
        consumer1.get_heat_demand = Mock(return_value=10)
        consumer1.temperature_in = 50
        consumer1.temperature_out = 40
        consumer2 = Mock(spec=ControllerConsumer)
        consumer2.id = "consumer2"
        consumer2.get_heat_demand = Mock(return_value=20)
        consumer2.temperature_in = 50
        consumer2.temperature_out = 40

        self.storage1 = Mock(spec=ControllerStorage)
        self.storage1.id = "storage1"
        self.storage1.max_discharge_power = 10
        self.storage1.max_charge_power = 20
        self.storage1.temperature_out = 50
        self.storage1.temperature_in = 40

        heatpump = ControllerHeatTransferAsset(name="heatpump1", identifier="heatpump1", factor=5.0)
        heatpump2 = ControllerHeatTransferAsset(
            name="heatpump2", identifier="heatpump2", factor=1.0
        )

        self.controller.networks[0] = ControllerNetwork(
            heat_transfer_assets_prim_in=[heatpump],
            heat_transfer_assets_sec_in=[],
            consumers_in=[],
            producers_in=[producer1],
            storages_in=[],
        )
        self.controller.networks[0].path = ["0"]

        self.controller.networks[1] = ControllerNetwork(
            heat_transfer_assets_prim_in=[heatpump2],
            heat_transfer_assets_sec_in=[heatpump],
            consumers_in=[consumer1],
            producers_in=[producer2],
            storages_in=[],
        )
        self.controller.networks[1].path = ["1", "0"]

        self.controller.networks[2] = ControllerNetwork(
            heat_transfer_assets_prim_in=[],
            heat_transfer_assets_sec_in=[heatpump2],
            consumers_in=[consumer2],
            producers_in=[],
            storages_in=[],
        )
        self.controller.networks[2].path = ["2", "1", "0"]

    def test_update_setpoints_one_source_off(self):
        # arrange
        self.setup_update_set_points()
        # act
        result = self.controller.update_setpoints(time=datetime.datetime.now())
        # assert
        self.assertEqual(result["producer1"][PROPERTY_HEAT_DEMAND], 6.0)
        self.assertEqual(result["producer2"][PROPERTY_HEAT_DEMAND], 0.0)
        self.assertEqual(result["consumer1"][PROPERTY_HEAT_DEMAND], 10.0)
        self.assertEqual(result["consumer2"][PROPERTY_HEAT_DEMAND], 20.0)
        self.assertEqual(result["heatpump1"][PRIMARY + PROPERTY_HEAT_DEMAND], 30.0)
        self.assertEqual(result["heatpump1"][SECONDARY + PROPERTY_HEAT_DEMAND], 150.0)
        self.assertEqual(result["heatpump2"][PRIMARY + PROPERTY_HEAT_DEMAND], 20.0)
        self.assertEqual(result["heatpump2"][SECONDARY + PROPERTY_HEAT_DEMAND], 20.0)

        # to test:
        # enough supply one source off : done
        # enough supply two sources on
        # Enough supply storage is charged.
        # not enough supply, storage needs to supply
        # not enough supply including storage.

    def test_update_setpoints_with_storage(self):
        self.setup_update_set_points()
        self.controller.networks[1].storages = [self.storage1]

        # act
        result = self.controller.update_setpoints(time=datetime.datetime.now())
        # assert
        self.assertAlmostEquals(result["producer1"][PROPERTY_HEAT_DEMAND], 10.0, places=3)
        self.assertAlmostEquals(result["producer2"][PROPERTY_HEAT_DEMAND], 0.0, places=3)
        self.assertAlmostEquals(result["consumer1"][PROPERTY_HEAT_DEMAND], 10.0, places=3)
        self.assertAlmostEquals(result["consumer2"][PROPERTY_HEAT_DEMAND], 20.0, places=3)
        self.assertAlmostEquals(result["heatpump1"][PRIMARY + PROPERTY_HEAT_DEMAND], 50.0, places=3)
        self.assertAlmostEquals(
            result["heatpump1"][SECONDARY + PROPERTY_HEAT_DEMAND], 250.0, places=3
        )
        self.assertAlmostEquals(result["heatpump2"][PRIMARY + PROPERTY_HEAT_DEMAND], 20.0, places=3)
        self.assertAlmostEquals(
            result["heatpump2"][SECONDARY + PROPERTY_HEAT_DEMAND], 20.0, places=3
        )
        self.assertAlmostEquals(result["storage1"][PROPERTY_HEAT_DEMAND], 20.0, places=3)

    def test_update_setpoints_two_source(self):
        self.setup_update_set_points()
        self.controller.networks[0].producers[0].power = 10.0
        self.controller.networks[0].heat_transfer_assets_prim[0].factor = 1
        # act
        result = self.controller.update_setpoints(time=datetime.datetime.now())
        # assert
        self.assertEqual(result["producer1"][PROPERTY_HEAT_DEMAND], 10.0)
        self.assertEqual(result["producer2"][PROPERTY_HEAT_DEMAND], 20.0)
        self.assertEqual(result["consumer1"][PROPERTY_HEAT_DEMAND], 10.0)
        self.assertEqual(result["consumer2"][PROPERTY_HEAT_DEMAND], 20.0)
        self.assertEqual(result["heatpump1"][PRIMARY + PROPERTY_HEAT_DEMAND], 10.0)
        self.assertEqual(result["heatpump1"][SECONDARY + PROPERTY_HEAT_DEMAND], 10.0)
        self.assertEqual(result["heatpump2"][PRIMARY + PROPERTY_HEAT_DEMAND], 20.0)
        self.assertEqual(result["heatpump2"][SECONDARY + PROPERTY_HEAT_DEMAND], 20.0)

    def test_update_setpoints_storage_discharge(self):
        # arrange
        self.setup_update_set_points()
        self.controller.networks[1].storages = [self.storage1]
        self.controller.networks[0].heat_transfer_assets_prim[0].factor = 1
        self.controller.networks[0].producers[0].power = 25.0
        self.controller.networks[1].producers = []

        # act
        result = self.controller.update_setpoints(time=datetime.datetime.now())
        # assert
        self.assertAlmostEquals(result["producer1"][PROPERTY_HEAT_DEMAND], 25.0, places=3)
        self.assertAlmostEquals(result["consumer1"][PROPERTY_HEAT_DEMAND], 10.0, places=3)
        self.assertAlmostEquals(result["consumer2"][PROPERTY_HEAT_DEMAND], 20.0, places=3)
        self.assertAlmostEquals(result["heatpump1"][PRIMARY + PROPERTY_HEAT_DEMAND], 25.0, places=3)
        self.assertAlmostEquals(
            result["heatpump1"][SECONDARY + PROPERTY_HEAT_DEMAND], 25.0, places=3
        )
        self.assertAlmostEquals(result["heatpump2"][PRIMARY + PROPERTY_HEAT_DEMAND], 20.0, places=3)
        self.assertAlmostEquals(
            result["heatpump2"][SECONDARY + PROPERTY_HEAT_DEMAND], 20.0, places=3
        )
        self.assertAlmostEquals(result["storage1"][PROPERTY_HEAT_DEMAND], -5.0, places=3)

    def test_update_stetpoints_cap_demand(self):
        # arrange
        self.setup_update_set_points()
        self.controller.networks[1].storages = [self.storage1]
        self.controller.networks[0].heat_transfer_assets_prim[0].factor = 1
        self.controller.networks[0].producers[0].power = 10.0
        self.controller.networks[1].producers[0].power = 10.0
        self.controller.networks[1].consumers[0].get_heat_demand = Mock(return_value=20)
        # act
        result = self.controller.update_setpoints(time=datetime.datetime.now())
        # assert
        self.assertAlmostEquals(result["producer1"][PROPERTY_HEAT_DEMAND], 10.0, places=3)
        self.assertAlmostEquals(result["producer2"][PROPERTY_HEAT_DEMAND], 10.0, places=3)
        self.assertAlmostEquals(result["consumer1"][PROPERTY_HEAT_DEMAND], 15, places=3)
        self.assertAlmostEquals(result["consumer2"][PROPERTY_HEAT_DEMAND], 15, places=3)
        self.assertAlmostEquals(result["heatpump1"][PRIMARY + PROPERTY_HEAT_DEMAND], 10, places=3)
        self.assertAlmostEquals(result["heatpump1"][SECONDARY + PROPERTY_HEAT_DEMAND], 10, places=3)
        self.assertAlmostEquals(result["heatpump2"][PRIMARY + PROPERTY_HEAT_DEMAND], 15, places=3)
        self.assertAlmostEquals(result["heatpump2"][SECONDARY + PROPERTY_HEAT_DEMAND], 15, places=3)
        self.assertAlmostEquals(result["storage1"][PROPERTY_HEAT_DEMAND], -10.0, places=3)

    def test_update_stetpoints_cap_storage(self):
        # arrange
        self.setup_update_set_points()
        self.storage1.max_charge_power = 100.0
        self.controller.networks[1].storages = [self.storage1]
        self.controller.networks[0].heat_transfer_assets_prim[0].factor = 1
        # act
        result = self.controller.update_setpoints(time=datetime.datetime.now())
        # assert
        self.assertAlmostEquals(result["producer1"][PROPERTY_HEAT_DEMAND], 50.0, places=3)
        self.assertAlmostEquals(result["producer2"][PROPERTY_HEAT_DEMAND], 40.0, places=3)
        self.assertAlmostEquals(result["consumer1"][PROPERTY_HEAT_DEMAND], 10, places=3)
        self.assertAlmostEquals(result["consumer2"][PROPERTY_HEAT_DEMAND], 20, places=3)
        self.assertAlmostEquals(result["heatpump1"][PRIMARY + PROPERTY_HEAT_DEMAND], 50, places=3)
        self.assertAlmostEquals(result["heatpump1"][SECONDARY + PROPERTY_HEAT_DEMAND], 50, places=3)
        self.assertAlmostEquals(result["heatpump2"][PRIMARY + PROPERTY_HEAT_DEMAND], 20, places=3)
        self.assertAlmostEquals(result["heatpump2"][SECONDARY + PROPERTY_HEAT_DEMAND], 20, places=3)
        self.assertAlmostEquals(result["storage1"][PROPERTY_HEAT_DEMAND], 60.0, places=3)

    def test_set_producers_to_max(self):
        # arrange
        self.controller.networks[0].set_supply_to_max = Mock(
            return_value={"id1": {"prop1": 3, "prop2": 5}}
        )
        self.controller.networks[1].set_supply_to_max = Mock(
            return_value={"id2": {"prop1": 10, "prop2": 75}}
        )
        self.controller.networks[2].set_supply_to_max = Mock(
            return_value={"id3": {"prop1": 9, "prop2": 15}}
        )
        # act
        result = self.controller._set_producers_to_max()
        # assert
        self.assertEqual(
            result,
            {
                "id1": {"prop1": 3, "prop2": 5},
                "id2": {"prop1": 10, "prop2": 75},
                "id3": {"prop1": 9, "prop2": 15},
            },
        )

    def test_set_all_storages_discharge_to_max(self):
        # arrange
        self.controller.networks[0].set_all_storages_discharge_to_max = Mock(
            return_value={"id1": {"prop1": 9, "prop2": 11}}
        )
        self.controller.networks[1].set_all_storages_discharge_to_max = Mock(
            return_value={"id2": {"prop1": 33, "prop2": 810}}
        )
        self.controller.networks[2].set_all_storages_discharge_to_max = Mock(
            return_value={"id3": {"prop1": 54, "prop2": 78}}
        )
        # act
        result = self.controller._set_all_storages_discharge_to_max()
        # assert
        self.assertEqual(
            result,
            {
                "id1": {"prop1": 9, "prop2": 11},
                "id2": {"prop1": 33, "prop2": 810},
                "id3": {"prop1": 54, "prop2": 78},
            },
        )

    def test_set_all_storages_charge_to_max(self):
        # arrange
        self.controller.networks[0].set_all_storages_charge_to_max = Mock(
            return_value={"id1": {"prop1": 54, "prop2": 423}}
        )
        self.controller.networks[1].set_all_storages_charge_to_max = Mock(
            return_value={"id2": {"prop1": 76, "prop2": 1324}}
        )
        self.controller.networks[2].set_all_storages_charge_to_max = Mock(
            return_value={"id3": {"prop1": 53, "prop2": 13}}
        )
        # act
        result = self.controller._set_all_storages_charge_to_max()
        # assert
        self.assertEqual(
            result,
            {
                "id1": {"prop1": 54, "prop2": 423},
                "id2": {"prop1": 76, "prop2": 1324},
                "id3": {"prop1": 53, "prop2": 13},
            },
        )

    def test_set_consumer_to_demand(self):
        # arrange
        self.controller.networks[0].set_consumer_to_demand = Mock(
            return_value={"id1": {"prop1": 432, "prop2": 23}}
        )
        self.controller.networks[1].set_consumer_to_demand = Mock(
            return_value={"id2": {"prop1": 543, "prop2": 654}}
        )
        self.controller.networks[2].set_consumer_to_demand = Mock(
            return_value={"id3": {"prop1": 56, "prop2": 56}}
        )
        # act
        result = self.controller._set_consumer_to_demand(time=datetime.datetime.now(), factor=1)
        # assert
        self.assertEqual(
            result,
            {
                "id1": {"prop1": 432, "prop2": 23},
                "id2": {"prop1": 543, "prop2": 654},
                "id3": {"prop1": 56, "prop2": 56},
            },
        )

    def test_set_producers_based_on_priority(self):
        # arrange
        producer1 = ControllerProducer(
            name="producer1",
            identifier="producer1",
            temperature_out=50,
            temperature_in=40,
            power=50,
            marginal_costs=1,
            priority=2,
        )
        producer2 = ControllerProducer(
            name="producer2",
            identifier="producer2",
            temperature_out=50,
            temperature_in=40,
            power=40,
            marginal_costs=1,
            priority=3,
        )
        producer3 = ControllerProducer(
            name="producer3",
            identifier="producer3",
            temperature_out=50,
            temperature_in=40,
            power=40,
            marginal_costs=1,
            priority=1,
        )
        producer4 = ControllerProducer(
            name="producer4",
            identifier="producer4",
            temperature_out=50,
            temperature_in=40,
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

    def test_get_total_supply_priority(self):
        # arrange
        producer1 = ControllerProducer(
            name="producer1",
            identifier="producer1",
            temperature_out=50,
            temperature_in=40,
            power=50,
            marginal_costs=1,
            priority=2,
        )
        producer2 = ControllerProducer(
            name="producer2",
            identifier="producer2",
            temperature_out=50,
            temperature_in=40,
            power=40,
            marginal_costs=1,
            priority=3,
        )
        producer3 = ControllerProducer(
            name="producer3",
            identifier="producer3",
            temperature_out=50,
            temperature_in=40,
            power=40,
            marginal_costs=1,
            priority=1,
        )
        producer4 = ControllerProducer(
            name="producer4",
            identifier="producer4",
            temperature_out=50,
            temperature_in=40,
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
