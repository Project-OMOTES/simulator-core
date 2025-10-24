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
"""Test controller storage class."""
import unittest
from datetime import datetime

import pandas as pd

from omotes_simulator_core.entities.assets.asset_defaults import (
    DEFAULT_TEMPERATURE,
    DEFAULT_TEMPERATURE_DIFFERENCE,
)
from omotes_simulator_core.entities.assets.controller.controller_storage import (
    ControllerStorage,
)
from omotes_simulator_core.entities.assets.controller.profile_interpolation import (
    ProfileInterpolationMethod,
    ProfileSamplingMethod,
)


class StorageControllerTest(unittest.TestCase):
    """Testcase for StorageConsumer class."""

    def setUp(self):
        """Set up the test case."""
        self.values = [100000, -200000]
        self.profile = pd.DataFrame(
            {
                "date": [datetime(2021, 1, 1, 0, 0, 0), datetime(2021, 1, 1, 1, 0, 0)],
                "values": self.values,
            }
        )
        self.storage = ControllerStorage(
            "storage",
            "id",
            temperature_out=DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE,
            temperature_in=DEFAULT_TEMPERATURE,
            max_charge_power=1000000,
            max_discharge_power=-1000000,
            profile=self.profile,
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )

    def test_storage_init(self):
        """Test to initialize the storage."""
        # Act

        # Assert
        self.assertEqual(self.storage.name, "storage")
        self.assertEqual(self.storage.id, "id")
        self.assertEqual(self.storage.temperature_in, DEFAULT_TEMPERATURE)
        self.assertEqual(
            self.storage.temperature_out, DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE
        )
        self.assertEqual(self.storage.start_index, 0)
        self.assertEqual(self.storage.max_charge_power, 1000000)
        pd.testing.assert_frame_equal(self.storage.profile, self.profile)

    def test_controller_storage_get_heat_power(self) -> None:
        """Test to get the heat power of the storage."""
        # Arrange

        # Act
        heatpower1 = self.storage.get_heat_power(datetime(2021, 1, 1, 0, 0, 0))
        heatpower2 = self.storage.get_heat_power(datetime(2021, 1, 1, 1, 0, 0))

        # Assert
        self.assertEqual(heatpower1, self.values[0])
        self.assertEqual(heatpower2, self.values[1])

    def test_storage_set_to_max_charge_power(self):
        """Test to set the storage to the max charge power."""
        # Arrange
        self.storage.max_charge_power = 1.0
        # Act
        heatpower = self.storage.get_heat_power(datetime(2021, 1, 1, 0, 0, 0))
        # Assert
        self.assertEqual(heatpower, 1.0)

    def test_storage_set_to_max_discharge_power(self):
        """Test to set the storage to the max discharge power."""
        # Arrange
        self.storage.max_discharge_power = -1.0
        # Act
        heatpower = self.storage.get_heat_power(datetime(2021, 1, 1, 1, 0, 0))
        # Assert
        self.assertEqual(heatpower, -1.0)

    def test_date_not_in_profile_storage(self):
        """Test to get the heat power when the date is not in the profile."""
        # Act
        heatpower = self.storage.get_heat_power(datetime(2021, 3, 2, 0, 0))
        # Assert
        self.assertEqual(heatpower, 0)
