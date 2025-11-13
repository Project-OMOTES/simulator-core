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
"""Test profile interpolation module."""
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import pandas as pd

from omotes_simulator_core.entities.assets.controller.profile_interpolation import (
    ProfileInterpolationMethod,
    ProfileInterpolator,
    ProfileSamplingMethod,
    set_interpolation_timestep_and_simulation_start_time,
)


class ProfileInterpolationTest(unittest.TestCase):
    """Testcase for ProfileInterpolator class."""

    def setUp(self):
        """Set up the test case."""
        # Create a basic profile with hourly data
        self.start_time = datetime(2021, 1, 1, 0, 0, 0)
        self.profile_data = pd.DataFrame(
            {
                "date": [
                    self.start_time,
                    self.start_time + timedelta(hours=1),
                    self.start_time + timedelta(hours=2),
                    self.start_time + timedelta(hours=3),
                ],
                "values": [100.0, 400.0, 150.0, 300.0],
            }
        )

        # Set global configuration
        set_interpolation_timestep_and_simulation_start_time(3600.0, self.start_time)

        self.interpolator = ProfileInterpolator(
            profile=self.profile_data,
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )

    def test_profile_interpolator_init(self):
        """Test to initialize the profile interpolator."""
        # Act & Assert
        self.assertIsNotNone(self.interpolator.profile)
        self.assertEqual(self.interpolator.sampling_method, ProfileSamplingMethod.ACTUAL)
        self.assertEqual(self.interpolator.interpolation_method, ProfileInterpolationMethod.LINEAR)
        self.assertEqual(self.interpolator.simulation_timestep, 3600.0)
        self.assertEqual(self.interpolator.simulation_start_time, self.start_time)
        self.assertEqual(self.interpolator.start_index, 0)
        pd.testing.assert_frame_equal(self.interpolator.profile, self.profile_data)

    def test_get_value_actual_sampling(self):
        """Test getting values with actual sampling method."""
        # Arrange
        test_time = self.start_time

        # Act
        value = self.interpolator.get_value(test_time)

        # Assert
        self.assertEqual(value, 100.0)

    def test_get_value_linear_interpolation(self):
        """Test linear interpolation between data points."""
        # Arrange
        set_interpolation_timestep_and_simulation_start_time(1800.0, self.start_time)
        interpolator = ProfileInterpolator(
            profile=self.profile_data,
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )
        test_time = self.start_time + timedelta(minutes=30)  # Halfway between first two points

        # Act
        value = interpolator.get_value(test_time)

        # Assert
        expected_value = 250.0  # Linear interpolation between 100 and 400
        self.assertAlmostEqual(value, expected_value, places=1)

    def test_get_value_average_sampling(self):
        """Test getting values with average sampling method."""
        # Arrange
        set_interpolation_timestep_and_simulation_start_time(7200.0, self.start_time)
        interpolator = ProfileInterpolator(
            profile=self.profile_data,
            sampling_method=ProfileSamplingMethod.AVERAGE,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )
        test_time = self.start_time

        # Act
        value = interpolator.get_value(test_time)

        # Assert
        self.assertIsInstance(value, float)
        self.assertEqual(value, (100.0 + 400.0) / 2)

    def test_get_value_maximum_sampling(self):
        """Test getting values with maximum sampling method."""
        # Arrange
        set_interpolation_timestep_and_simulation_start_time(3600 * 3, self.start_time)
        interpolator = ProfileInterpolator(
            profile=self.profile_data,
            sampling_method=ProfileSamplingMethod.MAXIMUM,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )
        test_time = self.start_time

        # Act
        value = interpolator.get_value(test_time)

        # Assert
        self.assertIsInstance(value, float)
        self.assertEqual(value, 400.0)

    def test_get_value_minimum_sampling(self):
        """Test getting values with minimum sampling method."""
        # Arrange
        set_interpolation_timestep_and_simulation_start_time(3600 * 3, self.start_time)
        interpolator = ProfileInterpolator(
            profile=self.profile_data,
            sampling_method=ProfileSamplingMethod.MINIMUM,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )
        test_time = self.start_time

        # Act
        value = interpolator.get_value(test_time)

        # Assert
        # Should return minimum of values in the window
        self.assertIsInstance(value, float)
        self.assertEqual(value, 100.0)

    def test_get_value_time_not_found(self):
        """Test getting values for a time not in the profile."""
        # Arrange
        test_time = datetime(2022, 1, 1, 0, 0, 0)

        # Act
        value = self.interpolator.get_value(test_time)

        # Assert
        self.assertEqual(value, 0.0)

    def test_different_interpolation_methods(self):
        """Test different interpolation methods."""
        # Test zero-order interpolation
        zero_interpolator = ProfileInterpolator(
            profile=self.profile_data,
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.ZERO,
        )

        # Test quadratic interpolation
        quadratic_interpolator = ProfileInterpolator(
            profile=self.profile_data,
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.QUADRATIC,
        )

        # Test cubic interpolation
        cubic_interpolator = ProfileInterpolator(
            profile=self.profile_data,
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.CUBIC,
        )

        # Act & Assert - just verify they initialize without errors
        self.assertEqual(zero_interpolator.interpolation_method, ProfileInterpolationMethod.ZERO)
        self.assertEqual(
            quadratic_interpolator.interpolation_method, ProfileInterpolationMethod.QUADRATIC
        )
        self.assertEqual(cubic_interpolator.interpolation_method, ProfileInterpolationMethod.CUBIC)

    def test_empty_profile(self):
        """Test handling of empty profile."""
        # Arrange
        empty_profile = pd.DataFrame({"date": [], "values": []})

        # Act
        interpolator = ProfileInterpolator(
            profile=empty_profile,
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )

        # Assert
        self.assertEqual(len(interpolator.profile), 0)
        self.assertEqual(len(interpolator.resampled_profile), 0)

    def test_single_point_profile(self):
        """Test handling of profile with single data point."""
        # Arrange
        single_point_profile = pd.DataFrame(
            {
                "date": [self.start_time],
                "values": [100.0],
            }
        )

        # Act
        interpolator = ProfileInterpolator(
            profile=single_point_profile,
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )

        # Assert
        self.assertEqual(len(interpolator.profile), 1)
        # Should return original profile when less than 2 points
        pd.testing.assert_frame_equal(interpolator.resampled_profile, single_point_profile)

    def test_profile_with_matching_timestep(self):
        """Test profile that already matches the simulation timestep."""
        # Arrange - profile already has 1-hour timestep
        # Act
        value = self.interpolator.get_value(self.start_time)

        # Assert
        self.assertEqual(value, 100.0)
        # Should use original profile when timesteps match
        pd.testing.assert_frame_equal(self.interpolator.resampled_profile, self.profile_data)

    def test_set_global_configuration(self):
        """Test setting global configuration for interpolation."""
        # Arrange
        new_timestep = 1800.0  # 30 minutes
        new_start_time = datetime(2021, 2, 1, 0, 0, 0)

        # Act
        set_interpolation_timestep_and_simulation_start_time(new_timestep, new_start_time)

        # Create new interpolator after setting global config
        interpolator = ProfileInterpolator(
            profile=self.profile_data,
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )

        # Assert
        self.assertEqual(interpolator.simulation_timestep, new_timestep)
        self.assertEqual(interpolator.simulation_start_time, new_start_time)

    def test_profile_sampling_method_enums(self):
        """Test ProfileSamplingMethod enum values."""
        # Assert
        self.assertEqual(ProfileSamplingMethod.DEFAULT.value, "actual")
        self.assertEqual(ProfileSamplingMethod.ACTUAL.value, "actual")
        self.assertEqual(ProfileSamplingMethod.AVERAGE.value, "average")
        self.assertEqual(ProfileSamplingMethod.MAXIMUM.value, "maximum")
        self.assertEqual(ProfileSamplingMethod.MINIMUM.value, "minimum")

    def test_profile_interpolation_method_enums(self):
        """Test ProfileInterpolationMethod enum values."""
        # Assert
        self.assertEqual(ProfileInterpolationMethod.DEFAULT.value, "linear")
        self.assertEqual(ProfileInterpolationMethod.LINEAR.value, "linear")
        self.assertEqual(ProfileInterpolationMethod.ZERO.value, "zero")
        self.assertEqual(ProfileInterpolationMethod.SLINEAR.value, "slinear")
        self.assertEqual(ProfileInterpolationMethod.QUADRATIC.value, "quadratic")
        self.assertEqual(ProfileInterpolationMethod.CUBIC.value, "cubic")

    @patch("omotes_simulator_core.entities.assets.controller.profile_interpolation.logger")
    def test_unknown_sampling_method_logs_error_and_raises_exception(self, mock_logger):
        """Test that an unknown sampling method logs an error and raises ValueError."""
        # Arrange
        interpolator = ProfileInterpolator(
            profile=self.profile_data,
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )

        # Create a mock sampling method with unknown value
        class MockSamplingMethod:
            value = "unknown_method"

        # Directly assign the mock sampling method
        interpolator.sampling_method = MockSamplingMethod()  # type: ignore

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            interpolator.get_value(self.start_time)

        # Assert the exception message
        self.assertEqual(str(context.exception), "Unknown sampling method: unknown_method")

        # Assert the error was logged
        mock_logger.error.assert_called_once_with("Unknown sampling method: unknown_method")

    @patch("omotes_simulator_core.entities.assets.controller.profile_interpolation.logger")
    def test_no_simulation_timestep_logs_warning(self, mock_logger):
        """Test that missing simulation timestep logs a warning."""
        # Arrange - Temporarily set global configuration to None by directly modifying module vars
        import omotes_simulator_core.entities.assets.controller.profile_interpolation as pi_module

        original_timestep = pi_module._simulation_timestep
        pi_module._simulation_timestep = None

        # Act
        ProfileInterpolator(
            profile=self.profile_data,
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )

        # Restore original value
        pi_module._simulation_timestep = original_timestep

        # Assert
        mock_logger.warning.assert_called_once_with(
            "No simulation timestep provided, using default of 3600 seconds (1 hour)"
        )

    @patch("omotes_simulator_core.entities.assets.controller.profile_interpolation.logger")
    def test_no_simulation_start_time_logs_warning(self, mock_logger):
        """Test that missing simulation start time logs a warning during interpolation."""
        # Arrange - Create profile that needs interpolation (different timestep)
        profile_30min = pd.DataFrame(
            {
                "date": [
                    self.start_time,
                    self.start_time + timedelta(minutes=30),
                    self.start_time + timedelta(hours=1),
                ],
                "values": [100.0, 150.0, 200.0],
            }
        )

        # Temporarily set start time to None by directly modifying module vars
        import omotes_simulator_core.entities.assets.controller.profile_interpolation as pi_module

        original_start_time = pi_module._simulation_start_time
        pi_module._simulation_start_time = None

        # Act
        interpolator = ProfileInterpolator(
            profile=profile_30min,
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )

        # Restore original value
        pi_module._simulation_start_time = original_start_time

        # Assert
        mock_logger.warning.assert_called_with(
            "Could not interpolate because simulation start time not available, "
            "using original profile"
        )
        # Should use original profile when interpolation fails
        pd.testing.assert_frame_equal(interpolator.resampled_profile, profile_30min)
