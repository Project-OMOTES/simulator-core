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
from typing import Optional

import pandas as pd

from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
    AssetControllerAbstract,
)


class ControllerProducer(AssetControllerAbstract):
    """Class to store the source for the controller."""

    def __init__(
        self,
        name: str,
        identifier: str,
        temperature_in: float,
        temperature_out: float,
        power: float,
        marginal_costs: float,
        profile: pd.DataFrame,
        priority: None | int = 1,
    ):
        """Constructor for the source.

        :param str name: Name of the source.
        :param str identifier: Unique identifier of the source.
        :param float temperature_in: Inlet temperature of the source.
        :param float temperature_out: Outlet temperature of the source.
        :param float power: Power of the source.
        :param float marginal_costs: Marginal costs of the source.
        :param int priority: Priority of the source.
        """
        super().__init__(name, identifier)
        self.temperature_in: float = temperature_in
        self.temperature_out: float = temperature_out
        self.power: float = power
        self.marginal_costs: float = marginal_costs
        self.priority: None | int = priority
        self.profile: pd.DataFrame = profile.set_index("date") if not profile.empty else profile

    def get_max_power(self, time: datetime.datetime) -> float:
        """Gets the maximum producer power at the given timestep.

        If there is a profile, it will look it up, otherwise it returns the
        maximum power defined in the esdl parameter.
        """
        if self.profile.empty:
            max_power = self.power
        else:
            try:
                max_power = float(self.profile.loc[time, "values"])
            except KeyError:
                max_power = self.power

        return max_power
