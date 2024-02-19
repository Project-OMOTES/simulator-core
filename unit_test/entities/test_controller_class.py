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

import pandas as pd
from datetime import datetime

from simulator_core.entities.assets.controller_classes import ControllerConsumer, ControllerSource


class ControllerTest(unittest.TestCase):
    """Testcase for Controller class."""

    def test_controller_producer(self) -> None:
        """Generic/template test for Controller."""
        # Arrange
        producer = ControllerSource("consumer", "id")
        # Act

        # Assert
        self.assertEqual(producer.name, "consumer")
        self.assertEqual(producer.id, "id")

    def test_controller_consumer(self) -> None:
        """Generic/template test for Controller."""
        # Arrange
        consumer = ControllerConsumer("consumer", "id")

        # Act

        # Assert
        self.assertEqual(consumer.name, "consumer")
        self.assertEqual(consumer.id, "id")

    def test_controller_consumer_add_profile(self) -> None:
        """Test to add a profile to the consumer."""
        # Arrange
        consumer = ControllerConsumer("consumer", "id")
        profile = pd.DataFrame({"date": [datetime(2021, 1, 1, 0, 0, 0),
                                         datetime(2021, 1, 1, 1, 0, 0)],
                                "value": [100, 200]})
        # Act
        consumer.add_profile(profile)
        # Assert
        self.assertEqual(len(consumer.profile), 2)

    def test_controller_consumer_get_heat_demand(self) -> None:
        """Test to get the heat demand of the consumer."""
        # Arrange
        consumer = ControllerConsumer("consumer", "id")
        values = [100, 200]
        profile = pd.DataFrame({"date": [datetime(2021, 1, 1,
                                                  0, 0, 0),
                                         datetime(2021, 1, 1,
                                                  1, 0, 0)],
                                "values": values})
        # Act
        consumer.add_profile(profile)
        # Act
        demand1 = consumer.get_heat_demand(datetime(2021, 1, 1,
                                                    0, 0, 0))
        demand2 = consumer.get_heat_demand(datetime(2021, 1, 1,
                                                    1, 0, 0))

        # Assert
        self.assertEqual(demand1, values[0])
        self.assertEqual(demand2, values[1])
