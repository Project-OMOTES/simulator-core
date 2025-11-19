#  Copyright (c) 2025. Deltares & TNO
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
"""Module containing the class for a controller network."""

import datetime

from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_HEAT_DEMAND,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
)
from omotes_simulator_core.entities.assets.controller.controller_consumer import ControllerConsumer
from omotes_simulator_core.entities.assets.controller.controller_heat_transfer import (
    ControllerHeatTransferAsset,
)
from omotes_simulator_core.entities.assets.controller.controller_producer import ControllerProducer
from omotes_simulator_core.entities.assets.controller.controller_storage import ControllerStorage


class ControllerNetwork:
    """Class storing an assets in the network which are hydraulic connected to each other.

    This class is used to be able to cope with heat exchangers and heat pumps.
    """

    heat_transfer_assets_prim: list[ControllerHeatTransferAsset]
    """List of all heat transfer assets connected with the primary side to the network."""
    heat_transfer_assets_sec: list[ControllerHeatTransferAsset]
    """List of all heat transfer assets connected with the secondary side to the network."""
    consumers: list[ControllerConsumer]
    """List of all consumers in the network."""
    producers: list[ControllerProducer]
    """List of all producers in the network."""
    storages: list[ControllerStorage]
    """List of all storages in the network."""
    factor_to_first_network: float
    """Factor to calculate power in the first network in the list of networks."""
    path: list[str]
    """Path from this network to the first network in the total system."""

    def __init__(
        self,
        heat_transfer_assets_prim_in: list[ControllerHeatTransferAsset],
        heat_transfer_assets_sec_in: list[ControllerHeatTransferAsset],
        consumers_in: list[ControllerConsumer],
        producers_in: list[ControllerProducer],
        storages_in: list[ControllerStorage],
        factor_to_first_network: float = 1,
    ) -> None:
        """Constructor of the class, which sets all attributes."""
        self.heat_transfer_assets_prim = heat_transfer_assets_prim_in
        self.heat_transfer_assets_sec = heat_transfer_assets_sec_in
        self.consumers = consumers_in
        self.producers = producers_in
        self.storages = storages_in
        self.factor_to_first_network = factor_to_first_network
        self.path: list[str] = []

    def exists(self, identifier: str) -> bool:
        """Method to check an asset is in the network.

        :param str identifier: Identifier of the asset to check.
        :return bool: True when the asset is in the network, False otherwise.
        """
        return any(
            [
                asset.id == identifier
                for asset in self.heat_transfer_assets_prim
                + self.heat_transfer_assets_sec
                + self.consumers
                + self.producers
                + self.storages
            ]
        )

    def get_total_heat_demand(self, time: datetime.datetime) -> float:
        """Method which the total heat demand at the given time corrected to the first network."""
        return (
            sum([consumer.get_heat_demand(time) for consumer in self.consumers])
            * self.factor_to_first_network
        )

    def get_total_discharge_storage(self) -> float:
        """Method to get the total storage discharge of the network corrected to the first network.

        :return float: Total heat discharge of all storages.
        """
        # TODO add limit based on state of charge
        return (
            float(sum([storage.max_discharge_power for storage in self.storages]))
            * self.factor_to_first_network
        )

    def get_total_charge_storage(self) -> float:
        """Method to get the total storage charge of the network corrected to the first network.

        :return float: Total heat charge of all storages.
        """
        # TODO add limit based on state of charge
        return (
            float(sum([storage.max_charge_power for storage in self.storages]))
            * self.factor_to_first_network
        )

    def get_total_supply(self) -> float:
        """Method to get the total heat supply of the network.

        :return float: Total heat supply of all producers.
        """
        return (
            float(sum([producer.power for producer in self.producers]))
            * self.factor_to_first_network
        )

    def set_supply_to_max(self, priority: int = 0) -> dict:
        """Method to set the producers to the max power.

        :return dict: Dict with key= asset-id and value=setpoints for the producers.
        """
        return self.set_supply(factor=1, priority=priority)

    def set_supply(self, factor: float = 1, priority: int = 0) -> dict:
        """Method to set the producers with the given priority to max power times the factor.

        :param float factor: Factor to multiply the max power with.
        :param int priority: Priority of the producers to set. When 0 all producers are set.

        :return dict: Dict with key= asset-id and value=setpoints for the producers.
        """
        producers = {}
        for source in self.producers:
            if priority == 0:
                pass
            elif source.priority != priority:
                continue
            producers[source.id] = {
                PROPERTY_HEAT_DEMAND: source.power * factor,
                PROPERTY_TEMPERATURE_OUT: source.temperature_out,
                PROPERTY_TEMPERATURE_IN: source.temperature_in,
                PROPERTY_SET_PRESSURE: False,
            }
        return producers

    def set_storage_charge_power(self, factor: float = 1) -> dict:
        """Method to set the producers to the max power times the given factor.

        :param float factor: Factor to multiply the max charge power with.
        :return dict: Dict with key= asset-id and value=setpoints for the producers.
        """
        storage_settings = {}
        for storage in self.storages:
            storage_settings[storage.id] = {
                PROPERTY_HEAT_DEMAND: storage.max_charge_power * factor,
                PROPERTY_TEMPERATURE_OUT: storage.temperature_out,
                PROPERTY_TEMPERATURE_IN: storage.temperature_in,
            }
        return storage_settings

    def set_storage_discharge_power(self, factor: float = 1) -> dict:
        """Method to set the producers to the max power times the given factor.

        :param float factor: Factor to multiply the max discharge power with.
        :return dict: Dict with key= asset-id and value=setpoints for the producers.
        """
        storage_settings = {}
        for storage in self.storages:
            storage_settings[storage.id] = {
                PROPERTY_HEAT_DEMAND: -storage.max_discharge_power * factor,
                PROPERTY_TEMPERATURE_OUT: storage.temperature_out,
                PROPERTY_TEMPERATURE_IN: storage.temperature_in,
            }
        return storage_settings

    def set_all_storages_discharge_to_max(self) -> dict:
        """Method to set all the storages to the max discharge power.

        :return dict: Dict with key= asset-id and value=setpoints for the storages.
        """
        return self.set_storage_discharge_power()

    def set_all_storages_charge_to_max(self) -> dict:
        """Method to set all the storages to the max discharge power.

        :return dict: Dict with key= asset-id and value=setpoints for the storages.
        """
        return self.set_storage_charge_power()

    def set_consumer_to_demand(self, time: datetime.datetime, factor: float = 1.0) -> dict:
        """Method to set the consumer to the demand multiplied by the given factor.

        :param datetime.datetime time: Time for which to set the consumer to the demand.
        :param float factor: Factor to multiply the heat demand with.

        :return: dict with the key the asset id and the value a dict with the set points for the
        consumers.
        """
        consumers = {}
        for consumer in self.consumers:
            consumers[consumer.id] = {
                PROPERTY_HEAT_DEMAND: consumer.get_heat_demand(time) * factor,
                PROPERTY_TEMPERATURE_OUT: consumer.temperature_out,
                PROPERTY_TEMPERATURE_IN: consumer.temperature_in,
            }
        return consumers

    def get_total_supply_priority(self, priority: int) -> float:
        """Method to get the total supply of the network for all sources with a certain priority.

        :param int priority: Priority of the producers to get the total supply for.
        :return float: Total heat supply of all producers with the given priority.
        """
        return float(
            sum([producer.power for producer in self.producers if producer.priority == priority])
        )

    def set_pressure(self) -> str:
        """Returns the id of the asset for which the pressure can be set for this network.

        The controller needs to set per hydraulic separated part of the system the pressure.
        The network can thus pass back the id for which asset the pressure needs to be set.
        The controller can then do this.
        """
        if self.heat_transfer_assets_sec:
            return self.heat_transfer_assets_sec[0].id
        if self.producers:
            return self.producers[0].id
        raise ValueError("No asset found for which the pressure can be set.")
