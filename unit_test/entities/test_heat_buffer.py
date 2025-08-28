#  Copyright (c) 2023. Deltares & TNO
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

"""Test Heat Buffer entities."""
import unittest

from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_HEAT_DEMAND,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
)
from omotes_simulator_core.entities.assets.heat_buffer import HeatBuffer


class HeatBufferTest(unittest.TestCase):
    """Testcase for HeatBuffer class."""

    def setUp(self) -> None:
        """Set up before each test case."""
        # Create a production cluster object
        self.heat_buffer = HeatBuffer(
            asset_name="heat_buffer",
            asset_id="heat_buffer_id",
            port_ids=["test1", "test2"],
            volume=1,
        )

    def test_injection(self) -> None:
        """Test injection to Heat Buffer."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: 1e4,
            PROPERTY_TEMPERATURE_IN: 363,
            PROPERTY_TEMPERATURE_OUT: 283,
        }

        # Act
        # charging for 1 day
        for _ii in range(0, 24):
            self.heat_buffer.first_time_step = True
            self.heat_buffer.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertAlmostEqual(self.heat_buffer.layer_temperature[2], 350.49, delta=0.01)

    def test_production(self) -> None:
        """Test production from Heat Buffer."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: -1e3,
            PROPERTY_TEMPERATURE_IN: 363,
            PROPERTY_TEMPERATURE_OUT: 283,
        }

        # Act
        # discharging for 1 day
        for _ii in range(0, 24):
            self.heat_buffer.first_time_step = True
            self.heat_buffer.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertAlmostEqual(self.heat_buffer.layer_temperature[2], 297.54, delta=0.01)
