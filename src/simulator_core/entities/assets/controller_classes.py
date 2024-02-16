#  Copyright (c) 2023. Deltares & TNO
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

import pandas as pd
from simulator_core.entities.assets.asset_defaults import (DEFAULT_TEMPERATURE,
                                                           DEFAULT_TEMPERATURE_DIFFERENCE)


class AssetControllerAbstract:
    """Abstract class for the asset controller."""

    def __init__(self, name: str, identifier: str):
        """Constructor for the asset controller.

        :param str name: Name of the controller object.
        :param str identifier: Unique identifier of the controller asset.
        """
        self.name = name
        self.id = identifier


class ControllerConsumer(AssetControllerAbstract):
    """Class to store the consumer for the controller asset."""

    def __init__(self, name: str, identifier: str):
        """Constructor for the consumer.

        :param str name: Name of the consumer.
        :param str identifier: Unique identifier of the consumer.
        """
        super().__init__(name, identifier)
        self.temperature_return = DEFAULT_TEMPERATURE
        self.temperature_supply = DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE
        self.profile: pd.DataFrame = pd.DataFrame()
        self.start_index = 0

    def get_heat_demand(self, time: datetime.datetime) -> float:
        """Method to get the heat demand of the consumer.

        :param datetime.datetime time: Time for which to get the heat demand.
        :return: float with the heat demand.
        """
        for index in range(self.start_index, len(self.profile)):
            if abs((self.profile["date"][index].to_pydatetime() - time).total_seconds()) < 3600:
                self.start_index = index
                return float(self.profile["values"][index])
        return 0

    def add_profile(self, profile: pd.DataFrame) -> None:
        """Method to add a profile to the consumer."""
        self.profile = profile


class ControllerSource(AssetControllerAbstract):
    """Class to store the source for the controller."""

    def __init__(self, name: str, identifier: str):
        """Constructor for the source.

        :param str name: Name of the source.
        :param str identifier: Unique identifier of the source.
        """
        super().__init__(name, identifier)
        self.temperature_return: float = DEFAULT_TEMPERATURE
        self.temperature_supply: float = DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE
        self.power: float = 5000000000
