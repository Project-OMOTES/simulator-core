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
from unittest.mock import Mock, patch

import pandas as pd

from omotes_simulator_core.entities.assets.asset_defaults import (
    DEFAULT_TEMPERATURE,
    DEFAULT_TEMPERATURE_DIFFERENCE,
    PROPERTY_FILL_LEVEL,
    PROPERTY_TIMESTEP,
    PROPERTY_VOLUME,
)
from omotes_simulator_core.entities.assets.controller.controller_storage import (
    ControllerAtestStorage,
    ControllerIdealHeatStorage,
    ControllerStorageAbstract,
)
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props

PROFILE_VALUES = [100000, -200000]
PROFILE = pd.DataFrame(
    {
        "date": [datetime(2021, 1, 1, 0, 0, 0), datetime(2021, 1, 1, 1, 0, 0)],
        "values": PROFILE_VALUES,
    }
)


# Abstract class
class ControllerStorageAbstractTest(unittest.TestCase):
    """Testcase for ControllerStorageAbstract class."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.storage = ControllerStorageAbstract(
            name="storage",
            identifier="storage_id",
            temperature_in=DEFAULT_TEMPERATURE,
            temperature_out=DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE,
            max_charge_power=1e6,
            max_discharge_power=-1e6,
            profile=PROFILE,
        )

    def test_storage_abstract_init(self):
        """Test to initialize the abstract storage."""
        # Act

        # Assert
        self.assertEqual(self.storage.name, "storage")
        self.assertEqual(self.storage.id, "storage_id")
        self.assertEqual(self.storage.temperature_in, DEFAULT_TEMPERATURE)
        self.assertEqual(
            self.storage.temperature_out, DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE
        )
        self.assertEqual(self.storage.start_index, 0)
        self.assertEqual(self.storage.max_charge_power, 1e6)
        self.assertEqual(self.storage.max_discharge_power, -1e6)
        self.assertEqual(self.storage.effective_max_charge_power, 1e6)
        self.assertEqual(self.storage.effective_max_discharge_power, -1e6)
        pd.testing.assert_frame_equal(self.storage.profile, PROFILE)


class ControllerAtestStorageTest(unittest.TestCase):
    """Testcase for ControllerAtestStorage."""

    def setUp(self):
        """Set up the test case."""

        self.storage = ControllerAtestStorage(
            "storage",
            "id",
            temperature_out=DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE,
            temperature_in=DEFAULT_TEMPERATURE,
            max_charge_power=1000000,
            max_discharge_power=-1000000,
            profile=PROFILE,
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
        pd.testing.assert_frame_equal(self.storage.profile, PROFILE)

    def test_controller_storage_get_heat_power(self) -> None:
        """Test to get the heat power of the storage."""
        # Arrange

        # Act
        heatpower1 = self.storage.get_heat_power(datetime(2021, 1, 1, 0, 0, 0))
        heatpower2 = self.storage.get_heat_power(datetime(2021, 1, 1, 1, 0, 0))

        # Assert
        self.assertEqual(heatpower1, PROFILE_VALUES[0])
        self.assertEqual(heatpower2, PROFILE_VALUES[1])

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
        self.assertEqual(heatpower, 0)


class ControllerIdealHeatStorageTest(unittest.TestCase):
    """Testcase for ControllerIdealHeatStorage."""

    def setUp(self):
        """Set up the test case."""

        self.storage = ControllerIdealHeatStorage(
            "storage",
            "id",
            temperature_out=DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE,
            temperature_in=DEFAULT_TEMPERATURE,
            max_charge_power=1000000,
            max_discharge_power=-1000000,
            fill_level=0.5,
            volume=1000,
            profile=PROFILE,
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
        pd.testing.assert_frame_equal(self.storage.profile, PROFILE)
        self.assertEqual(self.storage.fill_level, 0.5)
        self.assertEqual(self.storage.volume, 1000)
        self.assertEqual(self.storage.current_volume, 0.5 * 1000)

    def test_controller_storage_get_heat_power(self) -> None:
        """Test to get the heat power of the storage."""
        # Arrange

        # Act
        heatpower1 = self.storage.get_heat_power(datetime(2021, 1, 1, 0, 0, 0))
        heatpower2 = self.storage.get_heat_power(datetime(2021, 1, 1, 1, 0, 0))

        # Assert
        self.assertEqual(heatpower1, PROFILE_VALUES[0])
        self.assertEqual(heatpower2, PROFILE_VALUES[1])

    def test_controller_storage_get_heat_power_not_in_profile(self) -> None:
        """Test to get the heat power of the storage when date not in profile."""
        # Arrange

        # Act
        with self.assertLogs(level="WARNING") as log:
            heatpower = self.storage.get_heat_power(datetime(2021, 3, 2, 0, 0, 0))
            # Assert
            self.assertIn(
                "No profile value found for storage storage at time 2021-03-02 00:00:00. "
                "Returning 0.0 power.",
                log.output[0],
            )
            self.assertEqual(heatpower, 0)

    def test_controller_storage_get_heat_power(self) -> None:
        """Test to get the heat power of the storage."""
        # Arrange

        # Act
        heatpower = self.storage.get_heat_power(datetime(2021, 1, 1, 0, 0, 0))

        # Assert
        self.assertEqual(heatpower, PROFILE_VALUES[0])

    def test_storage_set_to_max_charge_power(self):
        """Test to set the storage to the max charge power."""
        # Arrange
        self.storage.max_charge_power = 1.0
        self.storage.effective_max_charge_power = 0.5
        # Act
        with self.assertLogs(level="WARNING") as log:
            heatpower = self.storage.get_heat_power(datetime(2021, 1, 1, 0, 0, 0))
            # Assert
            self.assertEqual(heatpower, 0.5)
            self.assertIn(
                (
                    "Supply to storage storage is higher than maximum charge power of asset at time "
                    + "2021-01-01 00:00:00."
                ),
                log.output[0],
            )

    def test_storage_set_to_max_discharge_power(self):
        """Test to set the storage to the max discharge power."""
        # Arrange
        self.storage.max_discharge_power = -1.0
        self.storage.effective_max_discharge_power = -0.5
        # Act
        with self.assertLogs(level="WARNING") as log:
            heatpower = self.storage.get_heat_power(datetime(2021, 1, 1, 1, 0, 0))
            # Assert
            self.assertEqual(heatpower, -0.5)
            self.assertIn(
                (
                    "Demand from storage storage is higher than maximum discharge power of asset at time "
                    + "2021-01-01 01:00:00."
                ),
                log.output[0],
            )

    @patch.object(fluid_props, "get_density")
    @patch.object(fluid_props, "get_heat_capacity")
    def test_storage_get_max_discharge_power_not_empty(self, patch_cp, patch_rho):
        """Test to get the max discharge power of the storage."""
        # Arrange
        patch_cp.return_value = 1.0  # J/kg.K
        patch_rho.return_value = 1.0  # kg/m3
        self.storage.current_volume = 1.0  # m3
        self.storage._delta_temperature = 1.0
        self.storage.timestep = 1.0
        self.storage.max_discharge_power = -1e9

        # Act
        max_discharge_power = self.storage.get_max_discharge_power()

        # Assert
        self.assertEqual(max_discharge_power, -1.0)  # W

    def test_storage_get_max_discharge_power_empty(self):
        """Test to get the max discharge power of the storage."""
        # Arrange
        self.storage.current_volume = 0.0  # m3

        # Act
        max_discharge_power = self.storage.get_max_discharge_power()

        # Assert
        self.assertEqual(max_discharge_power, 0.0)  # W

    @patch.object(fluid_props, "get_density")
    @patch.object(fluid_props, "get_heat_capacity")
    def test_storage_get_max_charge_power_not_filled(self, patch_cp, patch_rho):
        """Test to get the max charge power of the storage."""
        # Arrange
        patch_cp.return_value = 1.0  # J/kg.K
        patch_rho.return_value = 1.0  # kg/m3
        self.storage.volume = 1.0  # m3
        self.storage.current_volume = 0.0  # m3
        self.storage._delta_temperature = 1.0
        self.storage.timestep = 1.0
        self.storage.max_charge_power = 1e9

        # Act
        max_charge_power = self.storage.get_max_charge_power()

        # Assert
        self.assertEqual(max_charge_power, 1.0)  # W

    def test_storage_get_max_charge_power_filled(self):
        """Test to get the max charge power of the storage."""
        # Arrange
        self.storage.volume = 1.0  # m3
        self.storage.current_volume = 1.0  # m3

        # Act
        max_charge_power = self.storage.get_max_charge_power()

        # Assert
        self.assertEqual(max_charge_power, 0.0)  # W

    def test_set_state_missing_keys(self):
        """Test to set the state of the storage."""
        # Arrange
        required_keys = {PROPERTY_FILL_LEVEL, PROPERTY_TIMESTEP}

        # Act
        for missing_key in required_keys:
            state = {
                PROPERTY_FILL_LEVEL: 0.5,
                PROPERTY_TIMESTEP: 3600,
            }
            del state[missing_key]

            # Assert
            with self.assertRaises(KeyError) as cm:
                self.storage.set_state(state)
                self.assertEqual(
                    f"State keys [{missing_key}] are missing for storage {self.storage.name}.",
                    str(cm.exception),
                )

    @patch.object(ControllerIdealHeatStorage, "get_max_charge_power")
    @patch.object(ControllerIdealHeatStorage, "get_max_discharge_power")
    def test_set_state(self, patch_max_discharge_power, patch_max_charge_power):
        """Test to set the state of the storage."""
        # Arrange
        state = {
            PROPERTY_FILL_LEVEL: 1.0,
            PROPERTY_TIMESTEP: 3600,
        }
        patch_max_charge_power.return_value = 1.0
        patch_max_discharge_power.return_value = -1.0
        self.storage.volume = 2000

        # Act
        self.storage.set_state(state)

        # Assert
        self.assertEqual(self.storage.fill_level, 1.0)
        self.assertEqual(self.storage.current_volume, 2000)
        self.assertEqual(self.storage.timestep, 3600)
        self.assertEqual(self.storage.effective_max_charge_power, 1.0)
        self.assertEqual(self.storage.effective_max_discharge_power, -1.0)

    def test_set_fill_level_out_of_bounds(self):
        """Test to set the fill level of the storage."""
        # Arrange

        # Act / Assert
        with self.assertRaises(ValueError) as cm_low:
            self.storage._set_fill_level(-0.1)
            self.assertEqual(
                f"Fill level -0.1 for storage {self.storage.name} is out of bounds [0, 1].",
                str(cm_low.exception),
            )

        with self.assertRaises(ValueError) as cm_high:
            self.storage._set_fill_level(1.1)
            self.assertEqual(
                f"Fill level 1.1 for storage {self.storage.name} is out of bounds [0, 1].",
                str(cm_high.exception),
            )

    def test_set_fill_level(self):
        """Test to set the fill level of the storage."""
        # Arrange
        self.storage.volume = 2000

        # Act
        self.storage._set_fill_level(0.75)

        # Assert
        self.assertEqual(self.storage.fill_level, 0.75)
        self.assertEqual(self.storage.current_volume, 1500)
