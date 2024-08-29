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
import logging
from typing import List
from omotes_simulator_core.entities.network_controller_abstract import NetworkControllerAbstract
from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_TEMPERATURE_SUPPLY,
    PROPERTY_TEMPERATURE_RETURN,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_SET_PRESSURE,
)
from omotes_simulator_core.entities.assets.controller.controller_producer import ControllerProducer
from omotes_simulator_core.entities.assets.controller.controller_consumer import ControllerConsumer
from omotes_simulator_core.entities.assets.controller.controller_storage import ControllerStorage

logger = logging.getLogger(__name__)


class NetworkController(NetworkControllerAbstract):
    """Class to store the network controller."""

    def __init__(
        self,
        producers: List[ControllerProducer],
        consumers: List[ControllerConsumer],
        storages: List[ControllerStorage],
    ) -> None:
        """Constructor for controller for a heat network."""
        self.producers = producers
        self.consumers = consumers
        self.storages = storages

    def update_setpoints(self, time: datetime.datetime) -> dict:
        """Method to get the controller inputs for the network.

        :param float time: Time step for which to run the controller.
        :return: dict with the key the asset id and the heat demand for that asset.
        """
        # TODO add also the possibility to return mass flow rate instead of heat demand.
        if self.get_total_supply() <= self.get_total_demand(time):
            logger.warning(f"Total supply is lower than total demand at time: {time}")
            producers = self._set_producers_to_max()
            consumers = self._set_consumer_capped(time)
        else:
            # need to cap the power of the source based on priority. Consumers can meet their demand
            consumers = self._set_consumer_to_demand(time)
            producers = self._set_producers_based_on_priority(time)
        producers.update(consumers)
        return producers

    def get_total_demand(self, time: datetime.datetime) -> float:
        """Method to get the total heat demand of the network.

        :param datetime.datetime time: Time for which to get the total heat demand.
        :return float: Total heat demand of all consumers.
        """
        return sum([consumer.get_heat_demand(time) for consumer in self.consumers])

    def get_total_supply(self) -> float:
        """Method to get the total heat supply of the network.

        :return float: Total heat supply of all producers.
        """
        return float(sum([producer.power for producer in self.producers]))

    def get_total_supply_priority(self, priority: int) -> float:
        """Method to get the total supply of the network for all sources with a certain priority.

        :param int priority: The priority of the sources.
        :return float: Total heat supply of all producers with a certain priority.
        """
        return float(
            sum([producer.power for producer in self.producers if producer.priority == priority])
        )

    def _set_producers_to_max(self) -> dict:
        """Method to set the producers to the max power.

        :return dict: Dict with key= asset-id and value=setpoints for the producers.
        """
        producers = {}
        for source in self.producers:
            producers[source.id] = {
                PROPERTY_HEAT_DEMAND: source.power,
                PROPERTY_TEMPERATURE_RETURN: source.temperature_return,
                PROPERTY_TEMPERATURE_SUPPLY: source.temperature_supply,
                PROPERTY_SET_PRESSURE: False,
            }
        # setting the first producer to set the pressure.
        producers[self.producers[0].id][PROPERTY_SET_PRESSURE] = True
        return producers

    def _set_consumer_capped(self, time: datetime.datetime) -> dict:
        """Method to set the consumer to the max available power of the producers.

        :param datetime.datetime time: Time for which to cap the heat demand based on available
        power.

        :return: dict with the key the asset id and the value a dict with the set points for the
        consumers.
        """
        factor = self.get_total_supply() / self.get_total_demand(time)
        return self._set_consumer_to_demand(time=time, factor=factor)

    def _set_consumer_to_demand(self, time: datetime.datetime, factor: float = 1.0) -> dict:
        """Method to set the consumer to the demand.

        :param datetime.datetime time: Time for which to set the consumer to the demand.
        :param float factor: Factor to multiply the heat demand with.

        :return: dict with the key the asset id and the value a dict with the set points for the
        consumers.
        """
        consumers = {}
        for consumer in self.consumers:
            consumers[consumer.id] = {
                PROPERTY_HEAT_DEMAND: consumer.get_heat_demand(time) * factor,
                PROPERTY_TEMPERATURE_RETURN: consumer.temperature_return,
                PROPERTY_TEMPERATURE_SUPPLY: consumer.temperature_supply,
            }
        return consumers

    def _set_producers_based_on_priority(self, time: datetime.datetime) -> dict:
        """Method to set the producers based on priority.

        :param datetime.datetime time: Time for which to set the producers based on priority.

        :return: dict with the key the asset id and the value a dict with the set points for the
        producers.
        """
        producers = self._set_producers_to_max()
        total_demand = self.get_total_demand(time)
        if total_demand > self.get_total_supply():
            raise ValueError(
                "Total demand is higher than total supply. "
                "Cannot set producers based on priority."
            )
        priority = 0
        set_pressure = True
        while total_demand > 0:
            priority += 1
            total_supply = self.get_total_supply_priority(priority)
            if total_supply > total_demand:
                factor = total_demand / total_supply
                for source in self.producers:
                    if source.priority == priority:
                        producers[source.id][PROPERTY_HEAT_DEMAND] = source.power * factor
                        if set_pressure:
                            producers[source.id][PROPERTY_SET_PRESSURE] = True
                            set_pressure = False
                total_demand = 0
            else:
                for source in self.producers:
                    if source.priority == priority:
                        producers[source.id][PROPERTY_HEAT_DEMAND] = source.power
                total_demand -= total_supply
        return producers
