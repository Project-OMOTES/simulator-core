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
"""Module containing classes for profile data sampling and interpolation."""

import datetime
import logging
from enum import Enum
from typing import Optional

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

logger = logging.getLogger(__name__)

_simulation_timestep: Optional[float] = None
_simulation_start_time: Optional[datetime.datetime] = None


def set_interpolation_timestep_and_simulation_start_time(
    timestep: float, simulation_start_time: datetime.datetime
) -> None:
    """Set the global configuration for all ProfileInterpolator instances."""
    global _simulation_timestep, _simulation_start_time
    _simulation_timestep = timestep
    _simulation_start_time = simulation_start_time


class ProfileSamplingMethod(Enum):
    """Enumeration for different sampling methods.

    :param actual : return actual value at the time step
    :param average : return average value from the window time
    :param maximum : return maximum value from the window time
    :param minimum : return minimum value from the window time
    """

    DEFAULT = "actual"
    ACTUAL = "actual"
    AVERAGE = "average"
    MAXIMUM = "maximum"
    MINIMUM = "minimum"


class ProfileInterpolationMethod(Enum):
    """Enumeration for different interpolation methods.

    :param Linear : linear interpolation
    :param Zero : zeroth-order spline interpolation
    :param Slinear : first-order spline interpolation
    :param Quadratic : second-order spline interpolation
    :param Cubic : third-order spline interpolation
    """

    DEFAULT = "linear"
    LINEAR = "linear"
    ZERO = "zero"
    SLINEAR = "slinear"
    QUADRATIC = "quadratic"
    CUBIC = "cubic"


class ProfileInterpolator:
    """Class to handle profile interpolation for time series data."""

    def __init__(
        self,
        profile: pd.DataFrame,
        sampling_method: ProfileSamplingMethod,
        interpolation_method: ProfileInterpolationMethod,
    ):
        """Initialize the profile interpolator.

        :param pd.DataFrame profile: DataFrame with 'date' and 'values' columns
        :param ProfileSamplingMethod sampling_method: Method to use for profile sampling
        :param ProfileInterpolationMethod interpolation_method: Method to use for
        profile interpolation
        :param simulation_start_time: Optional start time to align the resampled profile with
        """
        self.profile = profile
        self.sampling_method = sampling_method
        self.interpolation_method = interpolation_method
        self.simulation_timestep = _simulation_timestep
        self.simulation_start_time = _simulation_start_time
        self.start_index = 0
        self.start_index_resampled = 0
        self._interpolator: Optional[interp1d] = None
        self.resampled_profile = self._resample_profile_if_needed()

    def _resample_profile_if_needed(self) -> pd.DataFrame:
        """Resample the profile to match the desired timestep using SciPy interpolation.

        :return: Resampled DataFrame with the desired timestep
        """
        # If no simulation timestep is set, use original profile
        if self.simulation_timestep is None:
            return self.profile

        profile_timestep = float(
            (
                pd.to_datetime(self.profile["date"].iloc[1])
                - pd.to_datetime(self.profile["date"].iloc[0])
            ).total_seconds()
        )

        if abs(profile_timestep - self.simulation_timestep) == 0.0:
            return self.profile

        return self._interpolate_profile_to_timestep()

    def _interpolate_profile_to_timestep(self) -> pd.DataFrame:
        """Use SciPy to interpolate profile using the given timestep.

        :return: Interpolated profile
        """
        # If no simulation timestep is set, use original profile
        if self.simulation_timestep is None:
            return self.profile

        # Convert dates to timestamps for interpolation
        dates = pd.to_datetime(self.profile["date"])
        timestamps = dates.astype(int) // 10**9
        values = self.profile["values"].values

        interpolator = interp1d(
            timestamps,
            values,
            kind=self.interpolation_method.value,
            bounds_error=False,
            fill_value=np.nan,
        )

        # Find starting point for resampling
        if self.simulation_start_time is not None:
            # Find first simulation time step that is >= simulation start time
            sim_start = pd.Timestamp(self.simulation_start_time)
            timestep_seconds = int(self.simulation_timestep)

            # Ensure timezone compatibility
            profile_end = dates.iloc[-1]
            profile_start = dates.iloc[0]

            # Make sim_start timezone-compatible with the profile dates
            if profile_start.tz is not None and sim_start.tz is None:
                sim_start = sim_start.tz_localize(profile_start.tz)
            elif profile_start.tz is None and sim_start.tz is not None:
                sim_start = sim_start.tz_localize(None)

            # Generate simulation time steps starting from sim_start
            current_time = sim_start
            while current_time <= profile_end:  # Continue until we cover the profile
                if current_time >= profile_start:  # Start from first time >= profile start
                    break
                current_time += pd.Timedelta(seconds=timestep_seconds)

            # Generate resampled times from this point
            new_times = pd.date_range(
                start=current_time, end=profile_end, freq=f"{timestep_seconds}s"
            )
        else:
            # Original behavior: start from profile start
            new_times = pd.date_range(
                start=dates.iloc[0], end=dates.iloc[-1], freq=f"{int(self.simulation_timestep)}s"
            )

        # Convert to timestamps for interpolation
        new_timestamps = new_times.astype(int) // 10**9

        # Interpolate values
        new_values = interpolator(new_timestamps)

        # Create new DataFrame
        return pd.DataFrame({"date": new_times, "values": new_values})

    def get_value(self, time: datetime.datetime) -> float:  # TODO this should be improved.
        """Get interpolated value at the specified time.

        :param datetime.datetime time: Time for which to get the value
        :return: Interpolated value
        """
        for index_resampled in range(self.start_index_resampled, len(self.resampled_profile)):
            if (
                abs(
                    (
                        self.resampled_profile["date"].iloc[index_resampled].to_pydatetime() - time
                    ).total_seconds()
                )
                < 1e-6
            ):
                self.start_index_resampled = index_resampled
                if self.sampling_method == ProfileSamplingMethod.ACTUAL:
                    return float(self.resampled_profile["values"].iloc[index_resampled])
                elif self.sampling_method in [
                    ProfileSamplingMethod.AVERAGE,
                    ProfileSamplingMethod.MAXIMUM,
                    ProfileSamplingMethod.MINIMUM,
                ]:
                    # Get filtered values in the time window for pandas-based methods
                    values_in_window = self._get_values_in_window(time)

                    if self.sampling_method == ProfileSamplingMethod.AVERAGE:
                        return float(values_in_window.mean()) if len(values_in_window) > 0 else 0.0
                    elif self.sampling_method == ProfileSamplingMethod.MAXIMUM:
                        return float(values_in_window.max()) if len(values_in_window) > 0 else 0.0
                    elif self.sampling_method == ProfileSamplingMethod.MINIMUM:
                        return float(values_in_window.min()) if len(values_in_window) > 0 else 0.0
                else:
                    logging.error(f"Unknown sampling method: {self.sampling_method.value}")
        return 0.0

    def _get_values_in_window(self, time: datetime.datetime) -> pd.Series:
        """Collect values from the ORIGINAL profile within (t-Δt, t).

        Always include the two window edges evaluated via the interpolant.
        """
        if self.simulation_timestep is None:
            raise ValueError("Simulation timestep must be set to use window-based sampling methods")

        target_time = pd.Timestamp(time)
        window_size = pd.Timedelta(seconds=self.simulation_timestep)

        profile_timestep = pd.to_datetime(self.profile["date"].iloc[1]) - pd.to_datetime(
            self.profile["date"].iloc[0]
        )

        # 1) take original points strictly inside (t-Δt, t)
        mask = (self.profile["date"] > target_time - window_size) & (
            self.profile["date"] < target_time
        )
        inner_vals = self.profile.loc[mask, "values"].astype(float).to_list()
        inner_times = pd.to_datetime(self.profile.loc[mask, "date"])

        # 2) include window edges using interpolation of the ORIGINAL profile
        left_edge = self._eval_at(target_time - window_size)
        left_edge_time = target_time + profile_timestep - window_size
        right_edge = self._eval_at(target_time)
        if (
            not inner_times.empty
            and abs((inner_times.iloc[0] - left_edge_time).total_seconds()) < 1e-6
        ):
            left_edge = np.nan  # ignore duplicate (will be skipped in mean/max/min)

        # 3) return as a Series (edges first so max/min/avg see boundaries)
        return pd.Series([left_edge, *inner_vals, right_edge], dtype=float)

    # --- add these small helpers inside ProfileInterpolator ---

    def _get_interpolator(self) -> interp1d:
        """Build an interpolator over the ORIGINAL profile."""
        if self._interpolator is not None:
            return self._interpolator
        dates = pd.to_datetime(self.profile["date"])
        ts_sec = dates.astype(int) // 10**9

        vals = self.profile["values"].to_numpy(dtype=float)

        self._interpolator = interp1d(
            ts_sec,
            vals,
            kind=self.interpolation_method.value,
            bounds_error=False,
            fill_value=np.nan,
            assume_sorted=True,
        )
        return self._interpolator

    def _eval_at(self, t: pd.Timestamp) -> float:
        """Evaluate interpolant at timestamp t (seconds)."""
        f = self._get_interpolator()
        ts = int(t.value // 1_000_000_000)
        return float(f(ts))
