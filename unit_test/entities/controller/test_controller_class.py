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
from pathlib import Path
from unittest.mock import Mock
from datetime import datetime, timezone

from simulator_core.adapter.transforms.mappers import EsdlControllerMapper
from simulator_core.entities.assets.controller.controller_consumer import ControllerConsumer
from simulator_core.entities.assets.controller.controller_producer import ControllerProducer
from simulator_core.entities.esdl_object import EsdlObject
from simulator_core.entities.network_controller import NetworkController
from simulator_core.entities.assets.asset_defaults import (PROPERTY_HEAT_DEMAND,
                                                           PROPERTY_TEMPERATURE_RETURN,
                                                           PROPERTY_TEMPERATURE_SUPPLY,
                                                           PROPERTY_SET_PRESSURE)
from simulator_core.infrastructure.utils import pyesdl_from_file


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
        self.producer2.power = 2.0
        self.producer2.priority = 2
        self.producer2.temperature_return = 40.0
        self.producer2.temperature_supply = 50.0
        self.consumer1 = Mock()
        self.consumer1.get_heat_demand.return_value = 1.0
        self.consumer1.temperature_return = 20.0
        self.consumer1.temperature_supply = 30.0
        self.consumer2 = Mock()
        self.consumer2.get_heat_demand.return_value = 2.0
        self.consumer2.temperature_return = 40.0
        self.consumer2.temperature_supply = 50.0
        self.controller = NetworkController(consumers=[self.consumer1, self.consumer2],
                                            producers=[self.producer1, self.producer2])

    def test_controller_init(self):
        """Test to initialize the controller."""
        consumer = ControllerConsumer("consumer", "id")
        producer = ControllerProducer("producer", "id")
        controller = NetworkController(consumers=[consumer], producers=[producer])
        # Act

        # Assert
        self.assertEqual(controller.consumers, [consumer])
        self.assertEqual(controller.producers, [producer])

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
        self.assertEqual(total_supply, 3.0)

    def test_get_total_supply_priority(self):
        """Test to get the total supply of the network for a certain priority."""
        # Act
        total_supply = self.controller.get_total_supply_priority(1)
        # Assert
        self.assertEqual(total_supply, 1.0)

    def test__set_producers_to_max(self):
        """Test to set the producers to the max power."""
        # Act
        producers = self.controller._set_producers_to_max()
        # Assert
        self.assertEqual(producers[self.producer1.id][PROPERTY_HEAT_DEMAND], 1.0)
        self.assertEqual(producers[self.producer1.id][PROPERTY_TEMPERATURE_RETURN], 20.0)
        self.assertEqual(producers[self.producer1.id][PROPERTY_TEMPERATURE_SUPPLY], 30.0)
        self.assertTrue(producers[self.producer1.id][PROPERTY_SET_PRESSURE])

        self.assertEqual(producers[self.producer2.id][PROPERTY_HEAT_DEMAND], 2.0)
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
        # Act
        producers = self.controller._set_producers_based_on_priority(datetime.now())
        # Assert
        self.assertEqual(producers[self.producer1.id][PROPERTY_HEAT_DEMAND], 1.0)
        self.assertEqual(producers[self.producer2.id][PROPERTY_HEAT_DEMAND], 1.5)

    def test_run_time_step(self):
        """Test to run the time step."""
        # Act
        result = self.controller.run_time_step(datetime.now())

        # Assert
        self.assertIn(self.producer1.id, result)
        self.assertIn(self.producer2.id, result)
        self.assertIn(self.consumer1.id, result)
        self.assertIn(self.consumer2.id, result)

    def test_esdl_loading(self):
        """Test to load the controller data from the esdl object."""
        # Arrange
        esdl_file = Path(__file__).parent / ".." / ".." / ".." / "testdata" / "test1.esdl"
        esdl_file = str(esdl_file)
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file))
        controller = EsdlControllerMapper().to_entity(esdl_object)
        start = datetime.strptime("2019-01-01T00:00:00",
                                  "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)

        # Act
        results = controller.run_time_step(start)

        # Assert
        self.assertIn("cf3d4b5e-437f-4c1b-a7f9-7fd7e8a269b4", results)
        self.assertIn("48f3e425-2143-4dcd-9101-c7e22559e82b", results)
        self.assertEqual(results["cf3d4b5e-437f-4c1b-a7f9-7fd7e8a269b4"]
                         [PROPERTY_HEAT_DEMAND], 360800.0)
        self.assertEqual(results["cf3d4b5e-437f-4c1b-a7f9-7fd7e8a269b4"]
                         [PROPERTY_TEMPERATURE_RETURN], 313.15)
        self.assertEqual(results["cf3d4b5e-437f-4c1b-a7f9-7fd7e8a269b4"]
                         [PROPERTY_TEMPERATURE_SUPPLY], 353.15)
        self.assertTrue(results["cf3d4b5e-437f-4c1b-a7f9-7fd7e8a269b4"]
                        [PROPERTY_SET_PRESSURE])
        self.assertEqual(results["48f3e425-2143-4dcd-9101-c7e22559e82b"]
                         [PROPERTY_HEAT_DEMAND], 360800.0)
        self.assertEqual(results["48f3e425-2143-4dcd-9101-c7e22559e82b"]
                         [PROPERTY_TEMPERATURE_RETURN], 353.15)
        self.assertEqual(results["48f3e425-2143-4dcd-9101-c7e22559e82b"]
                         [PROPERTY_TEMPERATURE_SUPPLY], 313.15)
