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
"""Test controller producer class."""
import unittest
from unittest.mock import Mock
from simulator_core.entities.assets.controller.controller_producer import ControllerProducer
from simulator_core.entities.assets.asset_defaults import (DEFAULT_TEMPERATURE,
                                                           DEFAULT_TEMPERATURE_DIFFERENCE)


class ControllerProducerTest(unittest.TestCase):
    """Testcase for ControllerProducer class."""

    def test_controller_producer_init(self) -> None:
        """Init test for ControllerProducer."""
        # Arrange
        producer = ControllerProducer("producer", "id")
        # Act

        # Assert
        self.assertEqual(producer.name, "producer")
        self.assertEqual(producer.id, "id")
        self.assertEqual(producer.temperature_return, DEFAULT_TEMPERATURE)
        self.assertEqual(producer.temperature_supply, DEFAULT_TEMPERATURE
                         + DEFAULT_TEMPERATURE_DIFFERENCE)
        self.assertEqual(producer.power, 1000)
        self.assertEqual(producer.priority, 1)

    def test_add_controller_data(self):
        """Test to add physical data to the controller."""
        # Arrange
        producer = ControllerProducer("producer", "id")
        esdl_asset_mock = Mock()
        esdl_asset_mock.get_property.return_value = (1.0, True)
        esdl_asset_mock.get_supply_temperature.return_value = 2.0
        esdl_asset_mock.get_return_temperature.return_value = 3.0
        # Act
        producer.set_controller_data(esdl_asset=esdl_asset_mock)
        # Assert
        self.assertEqual(producer.power, 1.0)
        self.assertEqual(producer.temperature_supply, 2.0)
        self.assertEqual(producer.temperature_return, 3.0)

    def test_add_power_error(self):
        """Test to add physical data to the controller resulting in error."""
        # Arrange
        producer = ControllerProducer("producer", "id")
        esdl_asset_mock = Mock()
        esdl_asset_mock.esdl_asset.name = "asset"
        esdl_asset_mock.get_property.return_value = (1.0, False)

        # Act
        with self.assertRaises(ValueError) as e:
            producer.set_controller_data(esdl_asset=esdl_asset_mock)

        # Assert
        self.assertEqual(str(e.exception), "No power found for asset: "
                         + esdl_asset_mock.esdl_asset.name)
