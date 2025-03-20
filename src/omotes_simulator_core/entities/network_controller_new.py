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
"""Module for new controller which can also cope with Heat pumps and heat exchangers."""

import datetime
import logging
from omotes_simulator_core.entities.assets.controller.controller_network import ControllerNetwork
from omotes_simulator_core.entities.network_controller_abstract import NetworkControllerAbstract

logger = logging.getLogger(__name__)


class NetworkControllerNew(NetworkControllerAbstract):
    """class for the enw network controller."""

    def __init__(
        self,
        networks: list[ControllerNetwork],
    ) -> None:
        """Constructor of the class, which sets all attributes."""
        self.networks = networks

    def update_networks_factor(self):
        """Method to update the factor of the networks taken into account the changing COP."""
        for network in self.networks:
            current_network = network
            network.factor = 1
            for step in network.path:
                if current_network == self.networks[int(step)]:
                    continue
                for asset in current_network.heat_transfer_assets_prim:
                    if self.networks[int(step)].exists(asset.id):
                        network.factor *= asset.factor
                        current_network = self.networks[int(step)]
                        break
                for asset in current_network.heat_transfer_assets_sec:
                    if self.networks[int(step)].exists(asset.id):
                        network.factor /= asset.factor
                        current_network = self.networks[int(step)]
                        break

    def update_setpoints(self, time: datetime.datetime) -> dict:
        """Method to get the controller inputs for the network.

        :param float time: Time step for which to run the controller.
        :return: dict with the key the asset id and the heat demand for that asset.
        """
        self.update_networks_factor()
        total_demand = sum([network.get_total_heat_demand(time) for network in self.networks])
        total_supply = sum([network.get_total_supply() for network in self.networks])
        total_charge_storage = sum(
            [network.get_total_charge_storage() for network in self.networks]
        )
        total_discharge_storage = sum(
            [network.get_total_discharge_storage() for network in self.networks]
        )

        if (total_supply + total_discharge_storage) <= total_demand:
            logger.warning(
                f"Total supply + storage is lower than total demand at time: {time}"
                f"Consumers are capped to the available power."
            )
            factor = total_demand / (total_supply + total_discharge_storage)
            producers = self._set_producers_to_max()
            producers.update(self._set_all_storages_discharge_to_max())
            producers.update(self._set_consumer_to_demand(time, factor=factor))
            return producers
        consumers = self._set_consumer_to_demand(time)
        if total_supply >= total_demand:
            # there is a surplus of supply we can charge the storage, storage becomes consumer.
            surplus_supply = total_supply - total_demand
            if surplus_supply <= total_charge_storage:
                storages = self._set_storages_power(surplus_supply)
                producers = self._set_producers_to_max()
            else:
                # need to cap the power of the source based on priority
                storages = self._set_storages_power(total_charge_storage)
                producers = self._set_producers_based_on_priority(time)

        else:
            # there is a deficit of supply we can discharge the storage, storage becomes
            # producer.
            deficit_supply = total_supply - total_demand
            storages = self._set_storages_power(deficit_supply)
            producers = self._set_producers_to_max()
        producers.update(consumers)
        producers.update(storages)
        return producers

    def _set_producers_to_max(self) -> dict:
        result = {}
        for network in self.networks:
            result.update(network.set_supply_to_max())
        return result

    def _set_all_storages_discharge_to_max(self) -> dict:
        result = {}
        for network in self.networks:
            result.update(network.set_all_storages_discharge_to_max())
        return result

    def _set_all_storages_charge_to_max(self) -> dict:
        result = {}
        for network in self.networks:
            result.update(network.set_all_storages_charge_to_max())
        return result

    def _set_consumer_to_demand(self, time: datetime.datetime, factor: float = 1) -> dict:
        result = {}
        for network in self.networks:
            result.update(network.set_consumer_to_demand(time, factor=factor))
        return result

    def _set_storages_power(self, power: float) -> dict:
        return {}

    def _set_producers_based_on_priority(self, time: datetime.datetime) -> dict:
        return {}
