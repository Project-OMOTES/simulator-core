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

        :return: Resampled DataFrame with the desired timestep or original if no resampling needed
        """
        # Use default timestep if none provided
        if self.simulation_timestep is None:
            logger.warning(
                "No simulation timestep provided, using default of 3600 seconds (1 hour)"
            )
            timestep = 3600.0
        else:
            timestep = self.simulation_timestep

        # Return empty profile if it has no data
        if len(self.profile) < 2:
            return self.profile

        profile_timestep = float(
            (
                pd.to_datetime(self.profile["date"].iloc[1])
                - pd.to_datetime(self.profile["date"].iloc[0])
            ).total_seconds()
        )

        if abs(profile_timestep - timestep) < 1e-6:
            return self.profile

        return self._interpolate_profile()

    def _interpolate_profile(self) -> pd.DataFrame:
        """Use SciPy to interpolate profile using the given timestep.

        :return: Interpolated profile
        """
        # Use default timestep if none provided
        timestep = self.simulation_timestep if self.simulation_timestep is not None else 3600.0

        # Return original profile if no simulation start time is set
        if self.simulation_start_time is None:
            logger.warning(
                "Could not interpolate because simulation start time not available, "
                "using original profile"
            )
            return self.profile

        dates = pd.to_datetime(self.profile["date"])
        timestamps = (dates.view("int64") // 1_000_000_000).astype(np.int64)
        values = self.profile["values"].values

        interpolator = interp1d(
            timestamps,
            values,
            kind=self.interpolation_method.value,
            bounds_error=False,
            fill_value=np.nan,
        )

        new_times = pd.date_range(
            start=pd.Timestamp(self.simulation_start_time).tz_localize(dates.iloc[0].tz),
            end=dates.iloc[-1],
            freq=f"{int(timestep)}s",
        )
        new_timestamps = (new_times.view("int64") // 1_000_000_000).astype(np.int64)
        new_values = interpolator(new_timestamps)

        return pd.DataFrame({"date": new_times, "values": new_values})

    def get_value(self, time: datetime.datetime) -> float:
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
        # Use default timestep if none provided
        timestep = self.simulation_timestep if self.simulation_timestep is not None else 3600.0

        current_time = pd.Timestamp(time)
        window_size = pd.Timedelta(seconds=timestep)

        # Data points inside the time window retrieved from original profile
        mask = (self.profile["date"] >= current_time) & (
            self.profile["date"] < current_time + window_size
        )
        inner_values = self.profile.loc[mask, "values"].astype(float).to_list()

        # Take point if it lies outside the original profile
        has_left_sample = (pd.to_datetime(self.profile["date"]) == current_time).any()

        vals = []
        if not has_left_sample:
            vals.append(
                float(
                    self.resampled_profile.loc[
                        (self.resampled_profile["date"] == current_time), "values"
                    ].iloc[0]
                )
            )
        vals.extend(inner_values)

        return pd.Series(vals, dtype=float)
