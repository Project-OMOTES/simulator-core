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

import numpy as np
import pandas as pd
from simulator_core.entities.assets.asset_defaults import (DEFAULT_TEMPERATURE,
                                                           DEFAULT_TEMPERATURE_DIFFERENCE)
from simulator_core.entities.assets.controller.controller_classes import AssetControllerAbstract
from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject


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
        self.max_power: float = np.inf

    def get_heat_demand(self, time: datetime.datetime) -> float:
        """Method to get the heat demand of the consumer.

        :param datetime.datetime time: Time for which to get the heat demand.
        :return: float with the heat demand.
        """
        for index in range(self.start_index, len(self.profile)):
            if abs((self.profile["date"][index].to_pydatetime() - time).total_seconds()) < 3600:
                self.start_index = index
                if self.profile["values"][index] > self.max_power:
                    # TODO need to pass a message that power is insufficient and is
                    #  capped to the max power available
                    return self.max_power
                else:
                    return float(self.profile["values"][index])
        return 0

    def add_profile(self, profile: pd.DataFrame) -> None:
        """Method to add a profile to the consumer."""
        self.profile = profile

    def set_controller_data(self, esdl_asset: EsdlAssetObject) -> None:
        """Method to get the controller data for esdl object."""
        self.temperature_supply = esdl_asset.get_return_temperature("Out")
        self.temperature_return = esdl_asset.get_supply_temperature("In")
        result = esdl_asset.get_property("power", np.inf)
        if result[0] == 0:
            self.max_power = np.inf
        elif result[1]:
            self.max_power = result[0]
