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
import unittest
from unittest.mock import Mock
from datetime import datetime

from omotes_simulator_core.entities.assets.controller.controller_consumer import ControllerConsumer
from omotes_simulator_core.entities.assets.controller.controller_producer import ControllerProducer
from omotes_simulator_core.entities.assets.controller.controller_storage import ControllerStorage
from omotes_simulator_core.entities.network_controller import NetworkController
from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_HEAT_DEMAND,
    PROPERTY_TEMPERATURE_RETURN,
    PROPERTY_TEMPERATURE_SUPPLY,
    PROPERTY_SET_PRESSURE,
)


class ControllerTest(unittest.TestCase):
    """Testcase for Controller class."""

    def setUp(self):
        """Set up the test case."""
        self.producer1 = Mock()
        self.producer1.id = "producer1"
        self.producer1.power = 1.0
        self.producer1.priority = 1
        self.producer1.temperature_return = 20.0
        self.producer1.temperature_supply = 30.0
        self.producer2 = Mock()
        self.producer2.id = "producer2"
        self.producer2.power = 4.0
        self.producer2.priority = 2
        self.producer2.temperature_return = 40.0
        self.producer2.temperature_supply = 50.0
        self.consumer1 = Mock()
        self.consumer1.id = "consumer1"
        self.consumer1.get_heat_demand.return_value = 1.0
        self.consumer1.temperature_return = 20.0
        self.consumer1.temperature_supply = 30.0
        self.consumer2 = Mock()
        self.consumer2.id = "consumer2"
        self.consumer2.get_heat_demand.return_value = 2.0
        self.consumer2.temperature_return = 40.0
        self.consumer2.temperature_supply = 50.0
        self.storage1 = Mock()
        self.storage1.id = "storage1"
        self.storage1.max_charge_power = 1.0
        self.storage1.max_discharge_power = -1.0
        self.storage1.temperature_return = 20.0
        self.storage1.temperature_supply = 40.0
        self.controller = NetworkController(
            [self.producer1, self.producer2], [self.consumer1, self.consumer2], [self.storage1]
        )

    def test_controller_init(self):
        """Test to initialize the controller."""
        consumer = ControllerConsumer(
            name="consumer",
            identifier="id",
            temperature_supply=20.0,
            temperature_return=30.0,
            max_power=1.0,
            profile=Mock(),
        )
        producer = ControllerProducer(
            "producer",
            "id",
            temperature_return=20.0,
            temperature_supply=30.0,
            power=1.0,
            priority=1,
        )
        storage = ControllerStorage(
            name="storage",
            identifier="id",
            temperature_supply=80.0,
            temperature_return=30.0,
            max_charge_power=0.0,
            max_discharge_power=0.0,
            profile=Mock(),
        )
        controller = NetworkController([producer], [consumer], [storage])
        # Act

        # Assert
        self.assertEqual(controller.consumers, [consumer])
        self.assertEqual(controller.producers, [producer])
        self.assertEqual(controller.storages, [storage])

    def test_get_total_demand(self):
        """Test to get the total demand of the network."""
        # Arrange
        # Act
        total_demand = self.controller.get_total_demand(datetime.now())

        # Assert
        self.assertEqual(total_demand, 3.0)

    def test_get_total_supply(self):
        """Test to get the total supply of the network."""
        # Act
        total_supply = self.controller.get_total_supply()
        # Assert
        self.assertEqual(total_supply, 5.0)

    def test_get_total_supply_priority(self):
        """Test to get the total supply of the network for a certain priority."""
        # Act
        total_supply = self.controller.get_total_supply_priority(1)
        # Assert
        self.assertEqual(total_supply, 1.0)

    def test_get_total_charge_storage(self):
        """Test to get the total charge storage of the network."""
        # Act
        total_charge = self.controller.get_total_charge_storage()
        # Assert
        self.assertEqual(total_charge, 1.0)

    def test_get_total_discharge_storage(self):
        """Test to get the total discharge storage of the network."""
        # Act
        total_discharge = self.controller.get_total_discharge_storage()
        # Assert
        self.assertEqual(total_discharge, -1.0)

    def test__set_producers_to_max(self):
        """Test to set the producers to the max power."""
        # Act
        producers = self.controller._set_producers_to_max()
        # Assert
        self.assertEqual(producers[self.producer1.id][PROPERTY_HEAT_DEMAND], 1.0)
        self.assertEqual(producers[self.producer1.id][PROPERTY_TEMPERATURE_RETURN], 20.0)
        self.assertEqual(producers[self.producer1.id][PROPERTY_TEMPERATURE_SUPPLY], 30.0)
        self.assertTrue(producers[self.producer1.id][PROPERTY_SET_PRESSURE])

        self.assertEqual(producers[self.producer2.id][PROPERTY_HEAT_DEMAND], 4.0)
        self.assertEqual(producers[self.producer2.id][PROPERTY_TEMPERATURE_RETURN], 40.0)
        self.assertEqual(producers[self.producer2.id][PROPERTY_TEMPERATURE_SUPPLY], 50.0)
        self.assertFalse(producers[self.producer2.id][PROPERTY_SET_PRESSURE])

    def test__set_consumer_capped(self):
        """Test to set the consumer to the capped power."""
        self.controller.producers[1].power = 0.5
        # Act
        consumers = self.controller._set_consumer_capped(datetime.now())
        # Assert
        self.assertEqual(consumers[self.consumer1.id][PROPERTY_HEAT_DEMAND], 1.0 * 1.5 / 3.0)
        self.assertEqual(consumers[self.consumer2.id][PROPERTY_HEAT_DEMAND], 2.0 * 1.5 / 3.0)

    def test__set_consumer_to_demand(self):
        """Test to set the consumer to the demand."""
        # Act
        consumers = self.controller._set_consumer_to_demand(datetime.now())
        # Assert
        self.assertEqual(consumers[self.consumer1.id][PROPERTY_HEAT_DEMAND], 1.0)
        self.assertEqual(consumers[self.consumer1.id][PROPERTY_TEMPERATURE_RETURN], 20.0)
        self.assertEqual(consumers[self.consumer1.id][PROPERTY_TEMPERATURE_SUPPLY], 30.0)

        self.assertEqual(consumers[self.consumer2.id][PROPERTY_HEAT_DEMAND], 2.0)
        self.assertEqual(consumers[self.consumer2.id][PROPERTY_TEMPERATURE_RETURN], 40.0)
        self.assertEqual(consumers[self.consumer2.id][PROPERTY_TEMPERATURE_SUPPLY], 50.0)

    def test__set_producers_based_on_priority(self):
        """Test to set the producers based on priority."""
        self.controller.consumers[0].get_heat_demand.return_value = 0.5
        self.controller.storages[0].max_charge_power = 0
        # Act
        producers = self.controller._set_producers_based_on_priority(datetime.now())
        # Assert
        self.assertEqual(producers[self.producer1.id][PROPERTY_HEAT_DEMAND], 1.0)
        self.assertEqual(producers[self.producer2.id][PROPERTY_HEAT_DEMAND], 1.5)

    def test_run_time_step(self):
        """Test to run the time step."""
        # Act
        result = self.controller.update_setpoints(datetime.now())

        # Assert
        self.assertIn(self.producer1.id, result)
        self.assertIn(self.producer2.id, result)
        self.assertIn(self.consumer1.id, result)
        self.assertIn(self.consumer2.id, result)

    def test_controller_capped_demand(self):
        """Test total supply and storage > demand."""
        # Arrange
        self.controller.consumers[0].get_heat_demand.return_value = 5
        self.controller.consumers[1].get_heat_demand.return_value = 5

        # Act
        result = self.controller.update_setpoints(datetime.now())

        # Assert
        self.assertEqual(result['consumer1']['heat_demand'], 2.5)
        self.assertEqual(result['consumer2']['heat_demand'], 2.5)

    def test_controller_charge_storage_max(self):
        """Test total supply able to charge storage to max."""
        # Arrange

        # Act
        result = self.controller.update_setpoints(datetime.now())

        # Assert
        self.assertEqual(result['storage1']['heat_demand'], 1)

    def test_controller_charge_storage_based_on_surplus(self):
        """Test total supply able to charge storage based on surplus."""
        # Arrange
        self.controller.producers[1].power = 2.7

        # Act
        result = self.controller.update_setpoints(datetime.now())

        # Assert
        self.assertAlmostEqual(result['storage1']['heat_demand'], 0.7, delta=0.01)

    def test_controller_discharge_storage_based_on_deficit(self):
        """Test total supply able to discharge storage based on deficit."""
        # Arrange
        self.controller.producers[1].power = 1.7

        # Act
        result = self.controller.update_setpoints(datetime.now())

        # Assert
        self.assertAlmostEqual(result['storage1']['heat_demand'], -0.3, delta=0.01)
