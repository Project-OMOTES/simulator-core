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
"""Module containing classes for profile data sampling and interpolation."""

import datetime
import logging
from enum import Enum
from typing import Optional

import math
import pandas as pd
from scipy.interpolate import interp1d

logger = logging.getLogger(__name__)


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
        sampling_method: Optional[ProfileSamplingMethod] = None,
        interpolation_method: Optional[ProfileInterpolationMethod] = None,
        timestep: Optional[int] = None,
    ):
        """Initialize the profile interpolator.

        :param pd.DataFrame profile: DataFrame with 'date' and 'values' columns
        :param ProfileSamplingMethod sampling_method: Method to use for profile sampling
        :param ProfileInterpolationMethod interpolation_method: Method to use for
        profile interpolation
        :param Optional[int] timestep: Simulation timestep in seconds.
        """
        self.profile = profile

        # Use defaults if not provided
        if sampling_method is None:
            logger.info("No sampling method provided, using default sampling method: actual")
            sampling_method = ProfileSamplingMethod.DEFAULT
        if interpolation_method is None:
            logger.info(
                "No interpolation method provided, using default interpolation method: linear"
            )
            interpolation_method = ProfileInterpolationMethod.DEFAULT

        self.sampling_method = sampling_method
        self.interpolation_method = interpolation_method
        self.simulation_timestep = timestep
        self.start_index = 0
        self.start_index_resampled = 0
        self._interpolator: Optional[interp1d] = None
        self.resampled_profile = self._resample_profile()

    def _resample_profile(self) -> pd.DataFrame:
        """Resample the profile to match the desired timestep using SciPy interpolation.

        :return: Resampled profile.
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

        # Sample to greatest common divider - workaround the limitation of the rolling function
        gcd_seconds = math.gcd(int(profile_timestep), int(timestep))
        minor_step = pd.to_timedelta(gcd_seconds, unit="s")
        index_minor = pd.date_range(
            start=self.profile["date"].iloc[0], end=self.profile["date"].iloc[-1], freq=minor_step
        )
        profile_resample_minor = (
            self.profile.set_index("date")
            .reindex(index_minor)
            .interpolate(method=self.interpolation_method.value)
        )

        points_in_window = int(timestep / gcd_seconds)
        indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=points_in_window)

        # Map sampling methods to their corresponding pandas rolling functions
        rolling = profile_resample_minor["values"].rolling(window=indexer, min_periods=1)

        profile_sampling_methods = {
            ProfileSamplingMethod.ACTUAL: lambda: rolling.apply(lambda x: x.iloc[0]),
            ProfileSamplingMethod.AVERAGE: lambda: rolling.mean(),
            ProfileSamplingMethod.MAXIMUM: lambda: rolling.max(),
            ProfileSamplingMethod.MINIMUM: lambda: rolling.min(),
        }

        if self.sampling_method not in profile_sampling_methods:
            logger.error(f"Unknown sampling method: {self.sampling_method.value}")
            raise ValueError(f"Unknown sampling method: {self.sampling_method.value}")

        df_indexer = profile_sampling_methods[self.sampling_method]()
        return pd.DataFrame({"date": df_indexer.index, "values": df_indexer.values})

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
                return float(self.resampled_profile["values"].iloc[index_resampled])
        return 0.0
