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
from omotes_simulator_core.entities.assets.controller.controller_producer import ControllerProducer


class ControllerProducerTest(unittest.TestCase):
    """Testcase for ControllerProducer class."""

    def setUp(self):
        """Set up the test case."""
        self.values = [100, 200]
        self.profile = pd.DataFrame(
            {
                "date": [datetime(2021, 1, 1, 0, 0, 0), datetime(2021, 1, 1, 1, 0, 0)],
                "values": self.values,
            }
        )
        self.producer = ControllerProducer(
            "producer",
            "id",
            temperature_out=DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE,
            temperature_in=DEFAULT_TEMPERATURE,
            power=1000,
            marginal_costs=0.1,
            priority=1,
            profile=self.profile,
        )

    def test_controller_producer_init(self) -> None:
        """Init test for ControllerProducer."""

        # Assert
        self.assertEqual(self.producer.name, "producer")
        self.assertEqual(self.producer.id, "id")
        self.assertEqual(self.producer.temperature_in, DEFAULT_TEMPERATURE)
        self.assertEqual(
            self.producer.temperature_out, DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE
        )
        self.assertEqual(self.producer.power, 1000)
        self.assertEqual(self.producer.marginal_costs, 0.1)
        self.assertEqual(self.producer.priority, 1)

    def test_controller_producer_none_priority(self) -> None:
        """Test to ensure a None priority does not break the CotrollerProducer.

        A None priority can be generated when an esdl with a priority control strategy has a
        producer with no priority assigned to it.
        """
        # Arrange
        self.producer.priority = None

        # Assert
        self.assertEqual(self.producer.priority, None)

    def test_get_max_power_profile(self) -> None:
        """Test to check if get_max_power returns the profile value or the power esdl value if
        no profile is present.
        """

        # Arrange
        time = datetime(2021, 1, 1, 0, 0, 0)

        # Act
        self.producer.profile = pd.DataFrame()
        max_power_1 = self.producer.get_max_power(time)  # No constraint profile present.
        self.producer.profile = self.profile.set_index("date")
        max_power_2 = self.producer.get_max_power(time)

        # Assert
        self.assertEqual(max_power_1, self.producer.power)
        self.assertEqual(max_power_2, self.values[0])
