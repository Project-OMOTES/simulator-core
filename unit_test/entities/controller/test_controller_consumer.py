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
from datetime import datetime

import pandas as pd

from omotes_simulator_core.entities.assets.asset_defaults import (
    DEFAULT_TEMPERATURE,
    DEFAULT_TEMPERATURE_DIFFERENCE,
)
from omotes_simulator_core.entities.assets.controller.controller_consumer import (
    ControllerConsumer,
)


class ConsumerControllerTest(unittest.TestCase):
    """Testcase for ControllerConsumer class."""

    def setUp(self):
        """Set up the test case."""
        self.values = [100, 200]
        self.profile = pd.DataFrame(
            {
                "date": [datetime(2021, 1, 1, 0, 0, 0), datetime(2021, 1, 1, 1, 0, 0)],
                "values": self.values,
            }
        )
        self.consumer = ControllerConsumer(
            "consumer",
            "id",
            temperature_supply=DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE,
            temperature_return=DEFAULT_TEMPERATURE,
            max_power=20000,
            profile=self.profile,
        )

    def test_consumer_init(self):
        """Test to initialize the consumer."""
        # Act

        # Assert
        self.assertEqual(self.consumer.name, "consumer")
        self.assertEqual(self.consumer.id, "id")
        self.assertEqual(self.consumer.temperature_return, DEFAULT_TEMPERATURE)
        self.assertEqual(
            self.consumer.temperature_supply, DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE
        )
        self.assertEqual(self.consumer.start_index, 0)
        self.assertEqual(self.consumer.max_power, 20000)
        pd.testing.assert_frame_equal(self.consumer.profile, self.profile)

    def test_controller_consumer_get_heat_demand(self) -> None:
        """Test to get the heat demand of the consumer."""
        # Arrange

        # Act
        demand1 = self.consumer.get_heat_demand(datetime(2021, 1, 1, 0, 0, 0))
        demand2 = self.consumer.get_heat_demand(datetime(2021, 1, 1, 1, 0, 0))

        # Assert
        self.assertEqual(demand1, self.values[0])
        self.assertEqual(demand2, self.values[1])

    def test_consumer_set_to_max_power(self):
        """Test to set the consumer to the max power."""
        # Arrange
        self.consumer.max_power = 1.0
        # Act
        demand = self.consumer.get_heat_demand(datetime(2021, 1, 1, 0, 0, 0))
        # Assert
        self.assertEqual(demand, 1.0)

    def test_date_not_in_profile_consumer(self):
        """Test to get the heat demand when the date is not in the profile."""
        # Act
        demand = self.consumer.get_heat_demand(datetime(2021, 3, 2, 0, 0))
        # Assert
        self.assertEqual(demand, 0)
