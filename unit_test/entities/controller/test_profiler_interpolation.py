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
"""Test Interpolation class."""

import unittest
from datetime import datetime
import pandas as pd
import numpy as np

# UPDATE THIS IMPORT IF YOUR MODULE PATH DIFFERS
from omotes_simulator_core.entities.assets.controller.profile_interpolation import (
    ProfileInterpolator,
    ProfileSamplingMethod,
    ProfileInterpolationMethod,
    set_interpolation_timestep_and_simulation_start_time,
)


class TestProfileInterpolator(unittest.TestCase):
    def setUp(self):
        # Simple hourly profile (tz-aware) for 2019-01-01 00:00..02:00
        self.tz = "Europe/Amsterdam"
        self.profile = pd.DataFrame(
            {
                "date": pd.to_datetime(
                    ["2019-01-01 00:00:00", "2019-01-01 01:00:00", "2019-01-01 02:00:00"]
                ).tz_localize(self.tz),
                "values": [0.0, 10.0, 20.0],
            }
        )

    def tearDown(self):
        # Reset globals so tests are isolated
        set_interpolation_timestep_and_simulation_start_time(
            timestep=None, simulation_start_time=None
        )

    # ---------- Resampling behavior ----------

    def test_warns_and_uses_default_timestep_when_none(self):
        """If simulation_timestep is None, a WARNING is logged and default 3600s is assumed."""
        set_interpolation_timestep_and_simulation_start_time(
            timestep=None, simulation_start_time=datetime(2019, 1, 1, 0, 0, 0)
        )
        with self.assertLogs(level="WARNING") as cm:
            ip = ProfileInterpolator(
                profile=self.profile.copy(),
                sampling_method=ProfileSamplingMethod.ACTUAL,
                interpolation_method=ProfileInterpolationMethod.LINEAR,
            )
        # Because profile timestep is hourly, no resampling should occur
        pd.testing.assert_frame_equal(ip.resampled_profile, self.profile)
        self.assertTrue(
            any("No simulation timestep provided" in m for m in cm.output),
            msg="Expected warning about default timestep.",
        )

    def test_warns_and_returns_original_if_no_sim_start_time(self):
        """If simulation_start_time is None and resampling would be needed, keep original with WARNING."""
        # Force a non-hourly timestep to trigger resampling, but leave sim_start None
        set_interpolation_timestep_and_simulation_start_time(
            timestep=1800, simulation_start_time=None
        )
        with self.assertLogs(level="WARNING") as cm:
            ip = ProfileInterpolator(
                profile=self.profile.copy(),
                sampling_method=ProfileSamplingMethod.ACTUAL,
                interpolation_method=ProfileInterpolationMethod.LINEAR,
            )
        # Should NOT resample because sim_start is missing
        pd.testing.assert_frame_equal(ip.resampled_profile, self.profile)
        self.assertTrue(
            any("simulation start time not available" in m for m in cm.output),
            msg="Expected warning about missing simulation start time.",
        )

    def test_resamples_when_timestep_differs_and_sim_start_given(self):
        """Resamples to 30-min grid starting at simulation_start_time localized to profile tz."""
        set_interpolation_timestep_and_simulation_start_time(
            timestep=1800, simulation_start_time=datetime(2019, 1, 1, 0, 0, 0)
        )
        ip = ProfileInterpolator(
            profile=self.profile.copy(),
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )
        times = ip.resampled_profile["date"].tolist()
        vals = ip.resampled_profile["values"].to_numpy()

        expected_times = pd.to_datetime(
            [
                "2019-01-01 00:00:00",
                "2019-01-01 00:30:00",
                "2019-01-01 01:00:00",
                "2019-01-01 01:30:00",
                "2019-01-01 02:00:00",
            ]
        ).tz_localize(self.tz)
        self.assertEqual(times, list(expected_times))
        # Linear ramp: 0, 5, 10, 15, 20
        np.testing.assert_allclose(vals, np.array([0, 5, 10, 15, 20], dtype=float))

    # ---------- get_value (ACTUAL) ----------

    def test_get_value_actual_returns_resampled_value(self):
        set_interpolation_timestep_and_simulation_start_time(
            timestep=1800, simulation_start_time=datetime(2019, 1, 1, 0, 0, 0)
        )
        ip = ProfileInterpolator(
            profile=self.profile.copy(),
            sampling_method=ProfileSamplingMethod.ACTUAL,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )
        # Call 00:30 first, then 01:00
        v2 = ip.get_value(pd.Timestamp("2019-01-01 00:30:00", tz=self.tz).to_pydatetime())
        self.assertAlmostEqual(v2, 5.0, places=6)

        v1 = ip.get_value(pd.Timestamp("2019-01-01 01:00:00", tz=self.tz).to_pydatetime())
        self.assertAlmostEqual(v1, 10.0, places=6)

    # ---------- Window aggregation: forward [t, t+Δt) ----------

    def test_forward_window_average_includes_left_edge_excludes_right(self):
        set_interpolation_timestep_and_simulation_start_time(
            timestep=1800, simulation_start_time=datetime(2019, 1, 1, 0, 0, 0)
        )
        ip = ProfileInterpolator(
            profile=self.profile.copy(),
            sampling_method=ProfileSamplingMethod.AVERAGE,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )
        # Call 00:30 first, then 01:00
        t2 = pd.Timestamp("2019-01-01 00:30:00", tz=self.tz).to_pydatetime()
        v2 = ip.get_value(t2)  # expect 5.0
        self.assertAlmostEqual(v2, 5.0, places=6)

        t1 = pd.Timestamp("2019-01-01 01:00:00", tz=self.tz).to_pydatetime()
        v1 = ip.get_value(t1)  # expect 10.0
        self.assertAlmostEqual(v1, 10.0, places=6)

    def test_forward_window_max_min(self):
        """MAXIMUM/MINIMUM use the same [t, t+Δt) window semantics."""
        set_interpolation_timestep_and_simulation_start_time(
            timestep=3600, simulation_start_time=datetime(2019, 1, 1, 0, 0, 0)
        )
        # For t=00:00, window [00:00, 01:00) includes only 0.0
        t = pd.Timestamp("2019-01-01 00:00:00", tz=self.tz).to_pydatetime()

        ip_max = ProfileInterpolator(
            profile=self.profile.copy(),
            sampling_method=ProfileSamplingMethod.MAXIMUM,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )
        self.assertAlmostEqual(ip_max.get_value(t), 0.0, places=6)

        ip_min = ProfileInterpolator(
            profile=self.profile.copy(),
            sampling_method=ProfileSamplingMethod.MINIMUM,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )
        self.assertAlmostEqual(ip_min.get_value(t), 0.0, places=6)

    def test_forward_window_includes_original_left_sample_over_interpolated(self):
        """If an original sample exists at t, it is used (not the interpolated value)."""
        set_interpolation_timestep_and_simulation_start_time(
            timestep=1800, simulation_start_time=datetime(2019, 1, 1, 0, 0, 0)
        )
        # At t=01:00 there is an original sample = 10.0; ensure aggregation uses 10.0
        ip = ProfileInterpolator(
            profile=self.profile.copy(),
            sampling_method=ProfileSamplingMethod.AVERAGE,
            interpolation_method=ProfileInterpolationMethod.LINEAR,
        )
        t = pd.Timestamp("2019-01-01 01:00:00", tz=self.tz).to_pydatetime()
        self.assertAlmostEqual(ip.get_value(t), 10.0, places=6)
