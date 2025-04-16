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

from omotes_simulator_core.entities.assets.controller.controller_consumer import ControllerConsumer
from omotes_simulator_core.entities.assets.controller.controller_heat_transfer import (
    ControllerHeatTransferAsset,
)
from omotes_simulator_core.entities.assets.controller.controller_producer import ControllerProducer
from omotes_simulator_core.entities.assets.controller.controller_storage import ControllerStorage
from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_TEMPERATURE_SUPPLY,
    PROPERTY_TEMPERATURE_RETURN,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_SET_PRESSURE,
)
import datetime


class ControllerNetwork:
    """Class storing an assets in the network which are hydraulic connected to each other.

    This class is used to be able to cope with heat exchangers and heat pumps.
    """

    def __init__(
        self,
        heat_transfer_assets_prim_in: list[ControllerHeatTransferAsset],
        heat_transfer_assets_sec_in: list[ControllerHeatTransferAsset],
        consumers_in: list[ControllerConsumer],
        producers_in: list[ControllerProducer],
        storage_in: list[ControllerStorage],
        factor: float = 1,
    ) -> None:
        """Constructor of the class, which sets all attributes."""
        self.heat_transfer_assets_prim = heat_transfer_assets_prim_in
        self.heat_transfer_assets_sec = heat_transfer_assets_sec_in
        self.consumers = consumers_in
        self.producers = producers_in
        self.storages = storage_in
        self.factor = factor
        self.path: list[str] = []

    def exists(self, id: str) -> bool:
        """Method to check an asset is in the network."""
        return any(
            [
                asset.id == id
                for asset in self.heat_transfer_assets_prim
                + self.heat_transfer_assets_sec
                + self.consumers
                + self.producers
                + self.storages
            ]
        )

    def get_total_heat_demand(self, time: datetime.datetime) -> float:
        """Method which the total heat demand at the given time."""
        return sum([consumer.get_heat_demand(time) for consumer in self.consumers]) * self.factor

    def get_total_discharge_storage(self) -> float:
        """Method to get the total storage discharge power of the network.

        :return float: Total heat discharge of all storages.
        """
        # TODO add limit based on state of charge
        return float(sum([storage.max_discharge_power for storage in self.storages])) * self.factor

    def get_total_charge_storage(self) -> float:
        """Method to get the total storage charge power of the network.

        :return float: Total heat charge of all storages.
        """
        # TODO add limit based on state of charge
        return float(sum([storage.max_charge_power for storage in self.storages])) * self.factor

    def get_total_supply(self) -> float:
        """Method to get the total heat supply of the network.

        :return float: Total heat supply of all producers.
        """
        return float(sum([producer.power for producer in self.producers])) * self.factor

    def set_supply_to_max(self, priority: int = 0) -> dict:
        """Method to set the producers to the max power.

        :return dict: Dict with key= asset-id and value=setpoints for the producers.
        """
        producers = {}
        for source in self.producers:
            if priority == 0:
                pass
            elif source.priority != priority:
                continue
            producers[source.id] = {
                PROPERTY_HEAT_DEMAND: source.power,
                PROPERTY_TEMPERATURE_RETURN: source.temperature_return,
                PROPERTY_TEMPERATURE_SUPPLY: source.temperature_supply,
                PROPERTY_SET_PRESSURE: False,
            }
        return producers

    def set_supply(self, factor: float = 1, priority: int = 0) -> dict:
        """Method to set the producers to the max power.

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
                PROPERTY_TEMPERATURE_RETURN: source.temperature_return,
                PROPERTY_TEMPERATURE_SUPPLY: source.temperature_supply,
                PROPERTY_SET_PRESSURE: False,
            }
        return producers

    def set_all_storages_discharge_to_max(self) -> dict:
        """Method to set all the storages to the max discharge power.

        :return dict: Dict with key= asset-id and value=setpoints for the storages.
        """
        storages = {}
        for storage in self.storages:
            storages[storage.id] = {
                PROPERTY_HEAT_DEMAND: -storage.max_discharge_power,
                PROPERTY_TEMPERATURE_RETURN: storage.temperature_return,
                PROPERTY_TEMPERATURE_SUPPLY: storage.temperature_supply,
            }
        return storages

    def set_all_storages_charge_to_max(self) -> dict:
        """Method to set all the storages to the max discharge power.

        :return dict: Dict with key= asset-id and value=setpoints for the storages.
        """
        storages = {}
        for storage in self.storages:
            storages[storage.id] = {
                PROPERTY_HEAT_DEMAND: storage.max_charge_power,
                PROPERTY_TEMPERATURE_RETURN: storage.temperature_return,
                PROPERTY_TEMPERATURE_SUPPLY: storage.temperature_supply,
            }
        return storages

    def set_consumer_to_demand(self, time: datetime.datetime, factor: float = 1.0) -> dict:
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

    def get_total_supply_priority(self, priority: int):
        """Method to get the total supply of the network for all sources with a certain priority."""
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
