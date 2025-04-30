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

from omotes_simulator_core.entities.assets.controller.controller_network import ControllerNetwork
from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_TEMPERATURE_SUPPLY,
    PROPERTY_TEMPERATURE_RETURN,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_SET_PRESSURE,
)


class TestControllerNetwork(unittest.TestCase):

    def setUp(self):
        """Set up the test case."""
        self.heat_transfer_assets_prim = []
        self.heat_transfer_assets_sec = []
        self.consumers = []
        self.producers = []
        self.storages = []
        self.factor = 1.0
        self.controller_network = ControllerNetwork(
            heat_transfer_assets_prim_in=self.heat_transfer_assets_prim,
            heat_transfer_assets_sec_in=self.heat_transfer_assets_sec,
            consumers_in=self.consumers,
            producers_in=self.producers,
            storages_in=self.storages,
            factor=self.factor,
        )

    def test_init(self):
        """Test the initialization of the ControllerNetwork class."""
        # arrange

        # act

        # assert
        self.assertEqual(
            self.controller_network.heat_transfer_assets_prim, self.heat_transfer_assets_prim
        )
        self.assertEqual(
            self.controller_network.heat_transfer_assets_sec, self.heat_transfer_assets_sec
        )
        self.assertEqual(self.controller_network.consumers, self.consumers)
        self.assertEqual(self.controller_network.producers, self.producers)
        self.assertEqual(self.controller_network.storages, self.storages)
        self.assertEqual(self.controller_network.factor, self.factor)
        self.assertEqual(self.controller_network.path, [])

    def test_exists(self):
        # arrange
        consumer = Mock()
        consumer.id = "test_consumer"
        self.controller_network.consumers.append(consumer)
        # act
        res = self.controller_network.exists("test_consumer")

        # assert
        self.assertTrue(res)

    def test_exists_false(self):
        # arrange

        # act
        res = self.controller_network.exists("test_consumer2")

        # assert
        self.assertFalse(res)

    def test_get_total_heat_demand(self):
        # arrange
        consumer1 = Mock()
        consumer1.get_heat_demand = Mock(return_value=10)
        consumer2 = Mock()
        consumer2.get_heat_demand = Mock(return_value=20)
        self.controller_network.consumers = [consumer1, consumer2]
        # act
        res = self.controller_network.get_total_heat_demand(datetime.datetime.now())
        # assert
        self.assertEqual(res, 30)

    def test_get_total_discharge_storage(self):
        # arrange
        storage1 = Mock()
        storage1.max_discharge_power = 10
        storage2 = Mock()
        storage2.max_discharge_power = 20
        self.controller_network.storages = [storage1, storage2]
        # act
        res = self.controller_network.get_total_discharge_storage()
        # assert
        self.assertEqual(res, 30)

    def test_get_total_charge_storage(self):
        # arrange
        storage1 = Mock()
        storage1.max_charge_power = 10
        storage2 = Mock()
        storage2.max_charge_power = 20
        self.controller_network.storages = [storage1, storage2]
        # act
        res = self.controller_network.get_total_charge_storage()
        # assert
        self.assertEqual(res, 30)

    def test_get_total_supply(self):
        # arrange
        producer1 = Mock()
        producer1.power = 10
        producer2 = Mock()
        producer2.power = 20
        self.controller_network.factor = 2.0
        self.controller_network.producers = [producer1, producer2]
        # act
        res = self.controller_network.get_total_supply()
        # assert
        self.assertEqual(res, 60)

    def test_set_supply_to_max_priority(self):
        # arrange
        producer1 = Mock()
        producer1.id = "producer1"
        producer1.power = 10
        producer1.temperature_supply = 50
        producer1.temperature_return = 40
        producer1.priority = 1
        producer2 = Mock()
        producer2.id = "producer2"
        producer2.power = 20
        producer2.priority = 2
        self.controller_network.producers = [producer1, producer2]
        # act
        res = self.controller_network.set_supply_to_max(priority=1)
        # assert
        self.assertEqual(
            res,
            {
                producer1.id: {
                    PROPERTY_HEAT_DEMAND: 10,
                    PROPERTY_TEMPERATURE_RETURN: 40,
                    PROPERTY_TEMPERATURE_SUPPLY: 50,
                    PROPERTY_SET_PRESSURE: False,
                }
            },
        )

    def test_set_supply_to_max_priority_zero(self):
        # arrange
        producer1 = Mock()
        producer1.id = "producer1"
        producer1.power = 10
        producer1.temperature_supply = 50
        producer1.temperature_return = 40
        producer1.priority = 1
        producer2 = Mock()
        producer2.id = "producer2"
        producer2.power = 20
        producer2.priority = 2
        producer2.temperature_supply = 80
        producer2.temperature_return = 100
        self.controller_network.producers = [producer1, producer2]
        # act
        res = self.controller_network.set_supply_to_max(priority=0)
        # assert
        self.assertEqual(
            res,
            {
                producer1.id: {
                    PROPERTY_HEAT_DEMAND: 10,
                    PROPERTY_TEMPERATURE_RETURN: 40,
                    PROPERTY_TEMPERATURE_SUPPLY: 50,
                    PROPERTY_SET_PRESSURE: False,
                },
                producer2.id: {
                    PROPERTY_HEAT_DEMAND: 20,
                    PROPERTY_TEMPERATURE_RETURN: 100,
                    PROPERTY_TEMPERATURE_SUPPLY: 80,
                    PROPERTY_SET_PRESSURE: False,
                },
            },
        )

    def test_set_supply(self):
        # arrange
        producer1 = Mock()
        producer1.id = "producer1"
        producer1.power = 10
        producer1.temperature_supply = 50
        producer1.temperature_return = 40
        producer1.priority = 1
        producer2 = Mock()
        producer2.id = "producer2"
        producer2.power = 20
        producer2.priority = 2
        self.controller_network.producers = [producer1, producer2]
        # act
        res = self.controller_network.set_supply(priority=1, factor=0.5)
        # assert
        self.assertEqual(
            res,
            {
                producer1.id: {
                    PROPERTY_HEAT_DEMAND: 5,
                    PROPERTY_TEMPERATURE_RETURN: 40,
                    PROPERTY_TEMPERATURE_SUPPLY: 50,
                    PROPERTY_SET_PRESSURE: False,
                }
            },
        )

    def test_set_all_storages_discharge_to_max(self):
        # arrange

        # act

        # assert
        pass

    def test_set_all_storages_charge_to_max(self):
        # arrange

        # act

        # assert
        pass

    def test_set_set_consumer_to_demand(self):
        # arrange

        # act

        # assert
        pass

    def test_get_total_supply_priority(self):
        # arrange

        # act

        # assert
        pass
