#  Copyright (c) 2025. Deltares & TNO
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

import pandas as pd

from omotes_simulator_core.entities.assets.controller.profile_interpolation import (
    ProfileInterpolationMethod,
    ProfileInterpolator,
    ProfileSamplingMethod,
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

        self.interpolator = ProfileInterpolator(
            profile=self.profile_data,
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
            timestep=3600,
        )

        self.resampled_profile = self.interpolator.get_resampled_profile().set_index("date")

    def test_profile_interpolator_init(self):
        """Test to initialize the profile interpolator."""
        # Assert
        self.assertIsNotNone(self.interpolator.profile)
        self.assertEqual(self.interpolator.sampling_method, ProfileSamplingMethod.ACTUAL)
        self.assertEqual(self.interpolator.interpolation_method, ProfileInterpolationMethod.LINEAR)
        self.assertEqual(self.interpolator.simulation_timestep, 3600)
        pd.testing.assert_frame_equal(self.interpolator.profile, self.profile_data)

    def test_get_value_actual_sampling(self):
        """Test getting values with actual sampling method."""
        # Arrange
        test_time = self.start_time

        # Act
        value = float(self.resampled_profile.loc[test_time, "values"])

        # Assert
        self.assertEqual(value, 100.0)

    def test_get_value_linear_interpolation(self):
        """Test linear interpolation between data points."""
        # Arrange
        interpolator = ProfileInterpolator(
            profile=self.profile_data,
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
            timestep=1800,
        )
        test_time = self.start_time + timedelta(minutes=30)
        resampled_profile = interpolator.get_resampled_profile().set_index("date")

        # Act
        value = float(resampled_profile.loc[test_time, "values"])  # type: ignore[call-overload]

        # Assert
        self.assertAlmostEqual(value, 250.0, places=1)

    def test_all_interpolation_methods(self):
        """Test all interpolation methods against pandas interpolation."""
        # Arrange
        timestep = 600
        test_methods = [
            ProfileInterpolationMethod.LINEAR,
            ProfileInterpolationMethod.ZERO,
            ProfileInterpolationMethod.SLINEAR,
            ProfileInterpolationMethod.QUADRATIC,
            ProfileInterpolationMethod.CUBIC,
        ]

        for interpolation_method in test_methods:
            with self.subTest(method=interpolation_method.value):
                # Act - Create ProfileInterpolator with 10-minute timestep
                interpolator = ProfileInterpolator(
                    profile=self.profile_data,
                    sampling_method=ProfileSamplingMethod.ACTUAL,
                    interpolation_method=interpolation_method,
                    timestep=timestep,
                )
                resampled_profile = interpolator.get_resampled_profile().set_index("date")
                profile_indexed = self.profile_data.set_index("date")
                freq = pd.Timedelta(seconds=timestep)
                expected_index = pd.date_range(
                    start=self.profile_data["date"].iloc[0],
                    end=self.profile_data["date"].iloc[-1],
                    freq=freq,
                )
                expected_profile = profile_indexed.reindex(expected_index).interpolate(
                    method=interpolation_method.value
                )
                expected_profile.index.name = "date"

                # Assert
                pd.testing.assert_frame_equal(
                    resampled_profile,
                    expected_profile,
                    check_dtype=False,
                    check_freq=False,
                    check_exact=True,
                )

    def test_all_sampling_methods(self):
        """Test all sampling methods with appropriate window sizes."""
        # Arrange
        test_time = self.start_time

        test_cases = [
            (ProfileSamplingMethod.ACTUAL, 3600, 100.0, "testing actual value at time step"),
            (ProfileSamplingMethod.AVERAGE, 7200, 250.0, "testing average in 2-hour window"),
            (ProfileSamplingMethod.MAXIMUM, 10800, 400.0, "testing maximum in 3-hour window"),
            (ProfileSamplingMethod.MINIMUM, 10800, 100.0, "testing minimum in 3-hour window"),
        ]
        # Act
        for sampling_method, timestep, expected_value, description in test_cases:
            with self.subTest(method=sampling_method.value, description=description):

                interpolator = ProfileInterpolator(
                    profile=self.profile_data,
                    sampling_method=sampling_method,
                    interpolation_method=ProfileInterpolationMethod.LINEAR,
                    timestep=timestep,
                )
                resampled_profile = interpolator.get_resampled_profile().set_index("date")
                value = float(resampled_profile.loc[test_time, "values"])

                # Assert
                self.assertIsInstance(value, float)
                self.assertEqual(value, expected_value)

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
        resampled_profile = interpolator.get_resampled_profile()

        # Assert
        self.assertEqual(len(interpolator.profile), 0)
        self.assertEqual(len(resampled_profile), 0)

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
        resampled_profile = interpolator.get_resampled_profile()

        # Assert
        self.assertEqual(len(interpolator.profile), 1)
        pd.testing.assert_frame_equal(resampled_profile, single_point_profile)

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

    def test_default_sampling_method_logs_info(self):
        """Test that missing sampling method logs info and uses default."""
        # Arrange

        # Act
        with self.assertLogs(
            "omotes_simulator_core.entities.assets.controller.profile_interpolation",
            level="INFO",
        ) as log_context:
            interpolator = ProfileInterpolator(
                profile=self.profile_data,
                sampling_method=None,
                interpolation_method=ProfileInterpolationMethod.LINEAR,
                timestep=3600,
            )

        # Assert
        self.assertEqual(interpolator.sampling_method, ProfileSamplingMethod.DEFAULT)
        self.assertEqual(
            log_context.output[0],
            "INFO:omotes_simulator_core.entities.assets.controller.profile_interpolation:"
            "No sampling method provided, using default sampling method: actual",
        )

    def test_default_interpolation_method_logs_info(self):
        """Test that missing interpolation method logs info and uses default."""
        # Arrange

        # Act
        with self.assertLogs(
            "omotes_simulator_core.entities.assets.controller.profile_interpolation",
            level="INFO",
        ) as log_context:
            interpolator = ProfileInterpolator(
                profile=self.profile_data,
                sampling_method=ProfileSamplingMethod.ACTUAL,
                interpolation_method=None,
                timestep=3600,
            )

        # Assert
        self.assertEqual(interpolator.interpolation_method, ProfileInterpolationMethod.DEFAULT)
        self.assertEqual(
            log_context.output[0],
            "INFO:omotes_simulator_core.entities.assets.controller.profile_interpolation:"
            "No interpolation method provided, using default interpolation method: linear",
        )

    def test_no_simulation_timestep_uses_default(self):
        """Test that missing simulation timestep logs warning and uses default value."""
        # Arrange

        # Act
        with self.assertLogs(
            "omotes_simulator_core.entities.assets.controller.profile_interpolation",
            level="WARNING",
        ) as log_context:
            interpolator = ProfileInterpolator(
                profile=self.profile_data,
                sampling_method=ProfileSamplingMethod.ACTUAL,
                interpolation_method=ProfileInterpolationMethod.LINEAR,
                timestep=None,
            )
            resampled_profile = interpolator.get_resampled_profile()

        # Assert
        self.assertEqual(interpolator.simulation_timestep, None)
        self.assertIsNotNone(resampled_profile)
        self.assertEqual(
            log_context.output[0],
            "WARNING:omotes_simulator_core.entities.assets.controller.profile_interpolation:"
            "No simulation timestep provided, using default of 3600 seconds (1 hour)",
        )
