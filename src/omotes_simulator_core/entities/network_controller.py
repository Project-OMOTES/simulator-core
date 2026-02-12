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
"""Module for controller which can also cope with Heat pumps and heat exchangers."""

import datetime
import logging

from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_HEAT_DEMAND,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
)
from omotes_simulator_core.entities.assets.controller.controller_network import ControllerNetwork
from omotes_simulator_core.entities.heat_network import HeatNetwork
from omotes_simulator_core.entities.network_controller_abstract import NetworkControllerAbstract

logger = logging.getLogger(__name__)

AssetSetpointsDict = dict[str, dict[str, float | bool]]


class NetworkController(NetworkControllerAbstract):
    """class for the new network controller."""

    def __init__(
        self,
        networks: list[ControllerNetwork],
    ) -> None:
        """Constructor of the class, which sets all attributes."""
        self.networks = networks

    def update_network_state(self, heat_network: HeatNetwork) -> None:
        """Method to update the network state."""
        for network in self.networks:
            # Update the state of all controllers in the network
            for controller in network.producers + network.consumers + network.storages:
                controller.set_state(heat_network.get_asset_by_id(controller.id).get_state())

    def update_networks_factor(self) -> None:
        """Method to update the factor of the networks taken into account the changing COP."""
        for network in self.networks:
            current_network = network
            network.factor_to_first_network = [1]
            for step in network.path:
                if current_network == self.networks[int(step)]:
                    continue
                for asset in current_network.heat_transfer_assets_prim:
                    if self.networks[int(step)].exists(asset.id):
                        network.factor_to_first_network.append(asset.factor)
                        # current_network = self.networks[int(step)]
                        break
                for asset in current_network.heat_transfer_assets_sec:
                    if self.networks[int(step)].exists(asset.id):
                        network.factor_to_first_network.append(1 / asset.factor)
                        # current_network = self.networks[int(step)]
                        break

    def update_setpoints(self, time: datetime.datetime) -> dict:
        """Method to get the controller inputs for the network.

        This method is used to determine the set points for all assets in the network.
        This is done in the following steps:
        1. Set the conversion factor for all networks based on the heat exchangers/heat pumps.
        2. Calculate the total demand and supply of the network converted to the first network in
            the list.
        3. Based on these results the set points for demand, supply and storage can be set.
        4. Finally, the heat transfer assets are set based on the set points of the producers,
            consumers and stroages

        :param float time: Time step for which to run the controller.
        :return: dict with the key the asset id and the heat demand for that asset.
        """
        self.update_networks_factor()
        total_demand = sum([network.get_total_heat_demand(time) for network in self.networks])
        total_supply = sum([network.get_total_supply() for network in self.networks])
        if total_supply > total_demand:
            # total supply is larger than demand, so demand can be set to required demand.
            consumers = self._set_consumer_to_demand(time)
            surplus_supply = total_supply - total_demand
            # Check charge capacity from storage
            total_charge_storage = sum(
                [network.get_total_charge_storage() for network in self.networks]
            )
            if total_charge_storage > surplus_supply:
                # there is more charge capacity than surplus supply, so we can set source to max and storages to charge with the surplus supply.
                producers = self._set_producers_to_max()
                storages = self._set_storages_charge_power(surplus_supply)
            else:
                # The storage can charge to max. The sources need to be capped.
                storages = self._set_all_storages_charge_to_max()
                producers = self._set_producers_based_on_priority(
                    surplus_supply + total_charge_storage
                )
        else:
            # total supply is lower than demand, so we need to check if there is enough discharge capacity from storage.
            total_discharge_storage = sum(
                [network.get_total_discharge_storage() for network in self.networks]
            )
            if (total_supply + total_discharge_storage) <= total_demand:
                logger.warning(
                    f"Total supply + storage is lower than total demand at time: {time}"
                    f"Consumers are capped to the available power."
                )
                factor = (total_supply + total_discharge_storage) / total_demand
                producers = self._set_producers_to_max()

                storages = self._set_all_storages_discharge_to_max()
                consumers = self._set_consumer_to_demand(time, factor=factor)
            else:
                # there is enough supply + storage to cover the demand. sources to max and storages to deliver the rest.
                consumers = self._set_consumer_to_demand(time)
                surplus_demand = total_supply - total_demand
                producers = self._set_producers_to_max()
                storages = self._set_storages_discharge_power(surplus_demand)
        producers.update(consumers)
        producers.update(storages)

        # Getting the settings for the heat transfer assets
        heat_transfer = {}
        total_charge_storage = sum(
            [network.get_total_charge_storage() for network in self.networks]
        )
        total_discharge_storage = sum(
            [network.get_total_discharge_storage() for network in self.networks]
        )

        # Initialize the producer, consumer, and storage setpoints dicts.
        producer_setpoints: AssetSetpointsDict = {}
        consumer_setpoints: AssetSetpointsDict = {}
        storage_setpoints: AssetSetpointsDict = {}

        if (total_supply + total_discharge_storage) <= total_demand:
            logger.warning(
                "Total supply + storage is lower than total demand at time: %s"
                "Consumers are capped to the available power.",
                time,
            )
            factor = (total_supply + total_discharge_storage) / total_demand
            # Define setpoints
            producer_setpoints = self._set_producers_to_max()
            storage_setpoints = self._set_all_storages_discharge_to_max()
            consumer_setpoints = self._set_consumer_to_demand(time, factor=factor)
        else:
            # Set consumer to requested demand.
            consumer_setpoints = self._set_consumer_to_demand(time, factor=1.0)
            # Set producers and storages based on the supply and demand, and the charge and
            # discharge capacity of the storage.
            if total_supply >= total_demand:
                # there is a surplus of supply we can charge the storage, storage becomes consumer.
                surplus_supply = total_supply - total_demand
                if surplus_supply <= total_charge_storage:
                    storage_setpoints = self._set_storages_charge_power(surplus_supply)
                    producer_setpoints = self._set_producers_to_max()
                elif surplus_supply > total_charge_storage:
                    # need to cap the power of the source based on priority
                    storage_setpoints = self._set_storages_charge_power(total_charge_storage)
                    producer_setpoints = self._set_producers_based_on_priority(
                        total_demand + total_charge_storage
                    )
            else:
                # there is a deficit of supply we can discharge the storage, storage becomes
                # producer.
                deficit_supply = total_demand - total_supply
                storage_setpoints = self._set_storages_discharge_power(deficit_supply)
                producer_setpoints = self._set_producers_to_max()

        # Update the asset setpoints with the setpoints of the producers, consumers,
        # and storages.
        asset_setpoints: AssetSetpointsDict = {}
        asset_setpoints.update(producer_setpoints)
        asset_setpoints.update(storage_setpoints)
        asset_setpoints.update(consumer_setpoints)

        # Getting the settings for the heat transfer assets
        heat_transfer: AssetSetpointsDict = {}

        # Set all the networks where there is only on primary or secondary heat exchanger.
        # Everything will then be set, since all heat transfer assets belong to a network where
        # they are the only one.
        for network in self.networks:
            number_of_heat_exchangers = len(network.heat_transfer_assets_prim) + len(
                network.heat_transfer_assets_sec
            )

            if number_of_heat_exchangers != 1:
                continue

            total_heat_supply: float = 0
            for producer in network.producers:
                total_heat_supply -= asset_setpoints[producer.id][PROPERTY_HEAT_DEMAND]
            for consumer in network.consumers:
                total_heat_supply -= asset_setpoints[consumer.id][PROPERTY_HEAT_DEMAND]
            for storage in network.storages:
                total_heat_supply -= asset_setpoints[storage.id][PROPERTY_HEAT_DEMAND]

            # this might look weird, but we know there is only one primary or secondary asset.
            # So we can directly set it.
            for asset in network.heat_transfer_assets_prim:
                if total_heat_supply > 0:
                    heat_transfer.update(asset.set_asset(total_heat_supply))
                else:
                    heat_transfer.update(asset.set_asset(total_heat_supply, True))
            for asset in network.heat_transfer_assets_sec:
                if total_heat_supply > 0:
                    heat_transfer.update(asset.set_asset(-total_heat_supply, True))
                else:
                    heat_transfer.update(asset.set_asset(-total_heat_supply))

        # Update the asset setpoints with the heat transfer setpoints.
        asset_setpoints.update(heat_transfer)

        # Set the pressure.
        for network in self.networks:
            pressure_set_asset = network.set_pressure()
            asset_setpoints[pressure_set_asset][PROPERTY_SET_PRESSURE] = True

        return asset_setpoints

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

    # TODO: Limit charge to effecitve charge
    def _set_storages_charge_power(self, power: float) -> dict:
        results: dict = {}
        total_power = sum([network.get_total_charge_storage() for network in self.networks])
        if total_power == 0:
            factor = 1.0
        else:
            factor = power / total_power
        for network in self.networks:
            results.update(network.set_storage_charge_power(factor=factor))
        return results

    # TODO: Limit discharge to effecitve discharge
    def _set_storages_discharge_power(self, power: float) -> dict:
        results: dict = {}
        total_power = sum([network.get_total_discharge_storage() for network in self.networks])
        if total_power == 0:
            factor = 1.0
        else:
            factor = power / total_power
        for network in self.networks:
            results.update(network.set_storage_discharge_power(factor=factor))
        return results

    def _set_producers_based_on_priority(self, required_supply: float) -> dict:
        """Method to set the producers based on the priority of the source."""
        producers = {}
        priority = 0
        while required_supply > 0:
            priority += 1
            max_supply_priority = self._get_total_supply_priority(priority)
            required_supply -= max_supply_priority
            if required_supply > 0:
                # set the producers with the priority to the max
                for network in self.networks:
                    producers.update(network.set_supply_to_max(priority))
            else:
                # set the producers with the priority with a factor.
                factor = 1 + required_supply / max_supply_priority
                for network in self.networks:
                    producers.update(network.set_supply(factor=factor, priority=priority))
        if len(producers) < sum([len(network.producers) for network in self.networks]):
            # not al producers are set need to set the remaining to zero.
            for network in self.networks:
                for producer in network.producers:
                    if producer.id not in producers:
                        producers[producer.id] = {
                            PROPERTY_HEAT_DEMAND: 0,
                            PROPERTY_TEMPERATURE_IN: producer.temperature_in,
                            PROPERTY_TEMPERATURE_OUT: producer.temperature_out,
                            PROPERTY_SET_PRESSURE: False,
                        }
        return producers

    def _get_total_supply_priority(self, priority: int) -> float:
        """Method to get the total supply of the network based on priority."""
        return float(
            sum([network.get_total_supply_priority(priority) for network in self.networks])
        )
