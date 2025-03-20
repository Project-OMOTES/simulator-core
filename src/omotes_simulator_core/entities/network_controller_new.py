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
        if total_demand > (total_supply + total_discharge_storage):
            logger.warning("Not enough supply to meet demand")
            # source to max , storage to max and demand capped.
            return {}
        if total_demand > total_supply:
            # source to max, storage set to mat final part of demand, demand to what is needed
            return {}
        # source to max and remaining to storage
        if total_demand + total_charge_storage > total_supply:
            # source to max, storage to max and demand capped
            return {}

        # source capped and storage to max
        return {}
