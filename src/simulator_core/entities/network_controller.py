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

"""NetworkController entity."""
import datetime

from simulator_core.entities.assets.asset_defaults import (PROPERTY_TEMPERATURE_SUPPLY,
                                                           PROPERTY_TEMPERATURE_RETURN,
                                                           PROPERTY_HEAT_DEMAND,
                                                           PROPERTY_SET_PRESSURE)
from simulator_core.entities.assets.controller_classes import ControllerSource, ControllerConsumer
from typing import List


class NetworkController:
    """Class to store the network controller."""

    def __init__(self, consumers: List[ControllerConsumer], sources: List[ControllerSource]) \
            -> None:
        """Constructor for controller for a heat network."""
        self.sources = sources
        self.consumers = consumers

    def run_time_step(self, time: datetime.datetime) -> dict:
        """Method to get the controller inputs for the network.

        :param float time: Time step for which to run the controller.
        :return: dict with the key the asset id and the heat demand for that asset.
        """
        # TODO add also the possibility to return mass flow rate instead of heat demand.

        controller_input = {}
        for consumer in self.consumers:
            controller_input[consumer.id] = {PROPERTY_HEAT_DEMAND: consumer.get_heat_demand(time),
                                             PROPERTY_TEMPERATURE_RETURN:
                                                 consumer.temperature_return,
                                             PROPERTY_TEMPERATURE_SUPPLY:
                                                 consumer.temperature_supply}
        for source in self.sources:
            controller_input[source.id] = {PROPERTY_HEAT_DEMAND: self.get_total_demand(time)
                                           / len(self.sources),
                                           PROPERTY_TEMPERATURE_RETURN: source.temperature_return,
                                           PROPERTY_TEMPERATURE_SUPPLY: source.temperature_supply,
                                           PROPERTY_SET_PRESSURE: False}
            # setting the first source to set the pressure for now.
            controller_input[self.sources[0].id][PROPERTY_SET_PRESSURE] = True
        return controller_input

    def get_total_demand(self, time: datetime.datetime) -> float:
        """Method to get the total heat demand of the network."""
        return sum([consumer.get_heat_demand(time) for consumer in self.consumers])

    def get_total_supply(self) -> float:
        """Method to get the total heat supply of the network."""
        return float(sum([source.power for source in self.sources]))
