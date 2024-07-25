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
        producer = ControllerProducer("producer", "id",
                                      temperature_supply=DEFAULT_TEMPERATURE
                                                         + DEFAULT_TEMPERATURE_DIFFERENCE,
                                      temperature_return=DEFAULT_TEMPERATURE,
                                      power=1000,
                                      priority=1)
        # Act

        # Assert
        self.assertEqual(producer.name, "producer")
        self.assertEqual(producer.id, "id")
        self.assertEqual(producer.temperature_return, DEFAULT_TEMPERATURE)
        self.assertEqual(producer.temperature_supply, DEFAULT_TEMPERATURE
                         + DEFAULT_TEMPERATURE_DIFFERENCE)
        self.assertEqual(producer.power, 1000)
        self.assertEqual(producer.priority, 1)
