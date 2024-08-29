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

import pandas as pd
import logging
from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
    AssetControllerAbstract,
)

logger = logging.getLogger(__name__)


class ControllerStorage(AssetControllerAbstract):
    """Class to store the storage for the controller asset."""

    def __init__(
        self,
        name: str,
        identifier: str,
        temperature_supply: float,
        temperature_return: float,
        max_power: float,
        profile: pd.DataFrame,
    ):
        """Constructor for the storage.

        :param str name: Name of the storage.
        :param str identifier: Unique identifier of the consumer.
        """
        super().__init__(name, identifier)
        self.temperature_return = temperature_return
        self.temperature_supply = temperature_supply
        self.profile: pd.DataFrame = profile
        self.start_index = 0
        self.max_power: float = max_power

    def get_heat_demand(self, time: datetime.datetime) -> float:
        """Method to get the heat demand of the storage.

        :param datetime.datetime time: Time for which to get the heat demand.
        :return: float with the heat demand.
        """
        for index in range(self.start_index, len(self.profile)):
            if abs((self.profile["date"][index].to_pydatetime() - time).total_seconds()) < 3600:
                self.start_index = index
                if self.profile["values"][index] > self.max_power:
                    logging.warning(
                        f"Demand of {self.name} is higher than maximum power of asset"
                        f" at time {time}."
                    )
                    return self.max_power
                else:
                    return float(self.profile["values"][index])
        return 0
