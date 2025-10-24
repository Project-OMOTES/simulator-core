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
"""Module containing the classes for the controller."""

import datetime
import logging

import pandas as pd

from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
    AssetControllerAbstract,
)
from omotes_simulator_core.entities.assets.controller.profile_interpolation import (
    ProfileInterpolator,
    ProfileSamplingMethod,
    ProfileInterpolationMethod,
)

logger = logging.getLogger(__name__)


class ControllerConsumer(AssetControllerAbstract):
    """Class to store the consumer for the controller asset."""

    def __init__(
        self,
        name: str,
        identifier: str,
        temperature_in: float,
        temperature_out: float,
        max_power: float,
        profile: pd.DataFrame,
        sampling_method: ProfileSamplingMethod,
        interpolation_method: ProfileInterpolationMethod,
    ):
        """Constructor for the consumer.

        :param str name: Name of the consumer.
        :param str identifier: Unique identifier of the consumer.
        :param float temperature_in: Temperature input of the consumer.
        :param float temperature_out: Temperature output of the consumer.
        :param float max_power: Maximum power of the consumer.
        :param ProfileSamplingMethod sampling_method: Method for profile sampling.
        :param ProfileInterpolationMethod interpolation_method: Method for profile interpolation.
        """
        super().__init__(name, identifier)
        self.temperature_in = temperature_in
        self.temperature_out = temperature_out
        self.profile: pd.DataFrame = profile
        self.start_index = 0
        self.max_power: float = max_power

        # Create profile interpolator
        self.profile_interpolator = ProfileInterpolator(
            profile=profile,
            sampling_method=sampling_method,
            interpolation_method=interpolation_method,
        )

    def get_heat_demand(self, time: datetime.datetime) -> float:
        """Method to get the heat demand of the consumer.

        :param datetime.datetime time: Time for which to get the heat demand.
        :return: float with the heat demand.
        """
        demand = self.profile_interpolator.get_value(time)

        if demand > self.max_power:
            logging.warning(
                f"Demand of {self.name} is higher than maximum power of asset" f" at time {time}."
            )
            return self.max_power

        return demand


# TODO: The max_power constraint check may never fail because max_power is inf by default
