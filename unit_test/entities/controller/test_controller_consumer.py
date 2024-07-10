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
import numpy as np
import pandas as pd
from datetime import datetime
from simulator_core.entities.assets.controller.controller_consumer import ControllerConsumer
from simulator_core.entities.assets.asset_defaults import (DEFAULT_TEMPERATURE,
                                                           DEFAULT_TEMPERATURE_DIFFERENCE)


class ConsumerControllerTest(unittest.TestCase):
    """Testcase for ControllerConsumer class."""

    def setUp(self):
        """Set up the test case."""
        self.consumer = ControllerConsumer("consumer", "id")

    def test_consumer_init(self):
        """Test to initialize the consumer."""
        # Act

        # Assert
        self.assertEqual(self.consumer.name, "consumer")
        self.assertEqual(self.consumer.id, "id")
        self.assertEqual(self.consumer.temperature_return, DEFAULT_TEMPERATURE)
        self.assertEqual(self.consumer.temperature_supply, DEFAULT_TEMPERATURE
                         + DEFAULT_TEMPERATURE_DIFFERENCE)
        self.assertEqual(self.consumer.start_index, 0)
        self.assertEqual(self.consumer.max_power, np.inf)

    def test_set_controller_data(self):
        """Test to set the controller data."""
        esdl_asset_mock = Mock()
        esdl_asset_mock.get_property.return_value = (1.0, True)
        esdl_asset_mock.get_supply_temperature.return_value = 2.0
        esdl_asset_mock.get_return_temperature.return_value = 3.0
        # Act
        self.consumer.set_controller_data(esdl_asset=esdl_asset_mock)
        # Assert
        self.assertEqual(self.consumer.max_power, 1.0)
        self.assertEqual(self.consumer.temperature_supply, 3.0)
        self.assertEqual(self.consumer.temperature_return, 2.0)

    def test_set_power_error(self):
        """Test to set the power to infinite when no power attribute is in the esdl asset."""
        esdl_asset_mock = Mock()
        esdl_asset_mock.get_property.return_value = (1.0, False)
        # Act
        self.consumer.set_controller_data(esdl_asset=esdl_asset_mock)
        # Assert
        self.assertEqual(self.consumer.max_power, np.inf)

    def test_set_power_zero(self):
        """Test to set the power to infinite when the power attribute is 0."""
        esdl_asset_mock = Mock()
        esdl_asset_mock.get_property.return_value = (0, True)
        # Act
        self.consumer.set_controller_data(esdl_asset=esdl_asset_mock)
        # Assert
        self.assertEqual(self.consumer.max_power, np.inf)

    def test_add_profile(self) -> None:
        """Test to add a profile to the consumer."""
        # Arrange
        profile = pd.DataFrame({"date": [datetime(2021, 1, 1, 0, 0, 0),
                                         datetime(2021, 1, 1, 1, 0, 0)],
                                "value": [100, 200]})
        # Act
        self.consumer.add_profile(profile)
        # Assert
        pd.testing.assert_frame_equal(self.consumer.profile, profile)

    def test_controller_consumer_get_heat_demand(self) -> None:
        """Test to get the heat demand of the consumer."""
        # Arrange
        values = [100, 200]
        profile = pd.DataFrame({"date": [datetime(2021, 1, 1,
                                                  0, 0, 0),
                                         datetime(2021, 1, 1,
                                                  1, 0, 0)],
                                "values": values})
        # Act
        self.consumer.add_profile(profile)
        # Act
        demand1 = self.consumer.get_heat_demand(datetime(2021, 1, 1,
                                                         0, 0, 0))
        demand2 = self.consumer.get_heat_demand(datetime(2021, 1, 1,
                                                         1, 0, 0))

        # Assert
        self.assertEqual(demand1, values[0])
        self.assertEqual(demand2, values[1])

    def test_consumer_set_to_max_power(self):
        """Test to set the consumer to the max power."""
        # Arrange
        self.consumer.max_power = 1.0
        values = [100, 200]
        profile = pd.DataFrame({"date": [datetime(2021, 1, 1,
                                                  0, 0, 0),
                                         datetime(2021, 1, 1,
                                                  1, 0, 0)],
                                "values": values})
        self.consumer.add_profile(profile)
        # Act
        demand = self.consumer.get_heat_demand(datetime(2021, 1, 1, 0, 0, 0))
        # Assert
        self.assertEqual(demand, 1.0)

    def test_date_not_in_profile_consumer(self):
        """Test to get the heat demand when the date is not in the profile."""
        values = [100, 200]
        profile = pd.DataFrame({"date": [datetime(2021, 1, 1,
                                                  0, 0, 0),
                                         datetime(2021, 1, 1,
                                                  1, 0, 0)],
                                "values": values})
        self.consumer.add_profile(profile)
        # Act
        demand = self.consumer.get_heat_demand(datetime(2021, 3, 2, 0, 0))
        # Assert
        self.assertEqual(demand, 0)
