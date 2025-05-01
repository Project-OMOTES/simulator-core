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
    PROPERTY_FILL_LEVEL,
    PROPERTY_TIMESTEP,
    PROPERTY_VOLUME,
)
from omotes_simulator_core.entities.assets.controller.controller_storage import (
    ControllerStorage,
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
            temperature_supply=DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE,
            temperature_return=DEFAULT_TEMPERATURE,
            max_charge_power=1000000,
            max_discharge_power=-1000000,
            fill_level=0.5,
            max_volume=1.0,
            profile=self.profile,
        )
        # Set effective storage and discharge
        self.storage.effective_max_charge_power = self.storage.max_charge_power
        self.storage.effective_max_discharge_power = self.storage.max_discharge_power

    def test_storage_init(self):
        """Test to initialize the storage."""
        # Act

        # Assert
        self.assertEqual(self.storage.name, "storage")
        self.assertEqual(self.storage.id, "id")
        self.assertEqual(self.storage.temperature_return, DEFAULT_TEMPERATURE)
        self.assertEqual(
            self.storage.temperature_supply, DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE
        )
        self.assertEqual(self.storage.start_index, 0)
        self.assertEqual(self.storage.max_charge_power, 1000000)
        pd.testing.assert_frame_equal(self.storage.profile, self.profile)

    def test_controller_set_state(self):
        """Test to set the state of the storage."""
        # Arrange
        state = {
            PROPERTY_FILL_LEVEL: 0.5,
            PROPERTY_VOLUME: 0.5,
            PROPERTY_TIMESTEP: 3600,
        }

        # Act
        self.storage.set_state(state)

        # Assert
        self.assertEqual(self.storage.fill_level, 0.5)
        self.assertEqual(self.storage.current_volume, 0.5)
        self.assertEqual(self.storage.timestep, 3600)
        self.assertAlmostEqual(self.storage.effective_max_charge_power * 1e-3, 188.8, 1)
        self.assertAlmostEqual(self.storage.effective_max_discharge_power * 1e-3, -188.8, 1)

    def test_controller_state_error(self):
        """Error in state variables supplied."""
        # Arrange
        state = {
            PROPERTY_FILL_LEVEL: 0.5,
            PROPERTY_VOLUME: 0.5,
        }

        # Act
        with self.assertRaises(ValueError) as cm:
            self.storage.set_state(state)

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            str(cm.exception),
            f"State keys ['{PROPERTY_TIMESTEP}'] are missing.",
        )

    def test_storage_set_to_max_charge_power(self):
        """Test to set the storage to the max charge power."""
        # Arrange
        self.storage.max_charge_power = 1.0
        self.storage.effective_max_charge_power = 1.0
        # Act
        heatpower = self.storage.get_heat_power(datetime(2021, 1, 1, 0, 0, 0))
        # Assert
        self.assertEqual(heatpower, 1.0)

    def test_storage_set_to_max_discharge_power(self):
        """Test to set the storage to the max discharge power."""
        # Arrange
        self.storage.max_discharge_power = -1.0
        self.storage.effective_max_discharge_power = -1.0
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

    def test_set_effective_max_charge_power(self):
        """Test to set the effective max charge power."""
        # Arrange
        self.storage.effective_max_charge_power = 1.0
        # Act
        heatpower = self.storage.get_heat_power(datetime(2021, 1, 1, 0, 0, 0))
        # Assert
        self.assertEqual(heatpower, 1.0)

    def test_controller_storage_get_heat_power(self) -> None:
        """Test to get the heat power of the storage, not empty or completely full."""
        # Arrange

        # Act
        heatpower1 = self.storage.get_heat_power(datetime(2021, 1, 1, 0, 0, 0))
        heatpower2 = self.storage.get_heat_power(datetime(2021, 1, 1, 1, 0, 0))

        # Assert
        self.assertEqual(heatpower1, self.values[0])
        self.assertEqual(heatpower2, self.values[1])

    def test_get_max_discharge_power_sufficient_capacity(self):
        """Test to get the max discharge power with sufficient capacity.

        The storage is not drained, so the max discharge power is not limited by the volume.
        """
        # Arrange
        self.storage.max_discharge_power = -100.0e3  # 100 kW

        # Act
        max_discharge_power = self.storage.get_max_discharge_power()

        # Assert
        self.assertEqual(max_discharge_power, -100.0e3)

    def test_get_max_discharge_power_insufficient_capacity(self):
        """Test to get the max discharge power with insufficient capacity.

        The storage is drained, so the max discharge power is limited by the volume.
        """
        # Arrange
        self.storage.max_discharge_power = -200.0e3  # 200 kW

        # Act
        max_discharge_power = self.storage.get_max_discharge_power()

        # Assert
        self.assertAlmostEqual(max_discharge_power * 1e-3, -188.8, 1)

    def test_get_max_charge_power_sufficient_capacity(self):
        """Test to get the max charge power with sufficient capacity.

        The storage is not full, so the max charge power is not limited by the volume.
        """
        # Arrange
        self.storage.max_charge_power = 100.0e3  # 100 kW

        # Act
        max_charge_power = self.storage.get_max_charge_power()

        # Assert
        self.assertEqual(max_charge_power, 100.0e3)

    def test_get_max_charge_power_insufficient_capacity(self):
        """Test to get the max charge power with insufficient capacity.

        The storage will be full, so the max charge power is limited by the volume.
        """
        # Arrange
        self.storage.max_discharge_power = 200.0e3  # 200 kW

        # Act
        max_discharge_power = self.storage.get_max_charge_power()

        # Assert
        self.assertAlmostEqual(max_discharge_power * 1e-3, 188.8, 1)

    def test_calculate_heatpower_full(self):
        """Test to calculate the effective max charge power when storage is full."""
        # Arrange
        self.storage.current_volume = self.storage.max_volume
        self.storage.effective_max_charge_power = self.storage.get_max_charge_power()

        # Act
        heatpower = self.storage.get_heat_power(datetime(2021, 1, 1, 0, 0, 0))

        # Assert
        self.assertEqual(heatpower, 0.0)

    def test_calculate_heatpower_empty(self):
        """Test to calculate the effective max discharge power when storage is empty."""
        # Arrange
        self.storage.current_volume = 0.0
        self.storage.effective_max_discharge_power = self.storage.get_max_discharge_power()

        # Act
        heatpower = self.storage.get_heat_power(datetime(2021, 1, 1, 1, 0, 0))

        # Assert
        self.assertEqual(heatpower, 0.0)
