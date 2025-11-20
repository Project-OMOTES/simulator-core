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
    ):
        """Constructor for the consumer.

        :param str name: Name of the consumer.
        :param str identifier: Unique identifier of the consumer.
        :param float temperature_in: Temperature input of the consumer.
        :param float temperature_out: Temperature output of the consumer.
        :param float max_power: Maximum power of the consumer.
        :param pd.DataFrame profile: Resampled profile based on interpolation and sampling methods.
        """
        super().__init__(name, identifier)
        self.temperature_in = temperature_in
        self.temperature_out = temperature_out
        self.max_power: float = max_power
        self.profile: pd.DataFrame = profile.set_index("date") if not profile.empty else profile

    def get_heat_demand(self, time: datetime.datetime) -> float:
        """Method to get the heat demand of the consumer.

        :param datetime.datetime time: Time for which to get the heat demand.
        :return: float with the heat demand.
        """
        if self.profile.empty:
            return 0.0

        try:
            demand = float(self.profile.loc[time, "values"])
        except KeyError:
            return 0.0

        if demand > self.max_power:
            logging.warning(
                f"Demand of {self.name} is higher than maximum power of asset at time {time}."
            )
            return self.max_power
        else:
            return demand
