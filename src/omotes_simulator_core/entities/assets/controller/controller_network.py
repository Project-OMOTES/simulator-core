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
from omotes_simulator_core.entities.assets.controller.controler_heat_transfer import (
    ControllerHeatTransferAsset,
)
from omotes_simulator_core.entities.assets.controller.controller_producer import ControllerProducer
from omotes_simulator_core.entities.assets.controller.controller_storage import ControllerStorage
import datetime


class ControllerNetwork:
    """Class storing an assets in the network which are hydraulic connected to each other.
    This class is used to be able to cope with heat exchangers and heat pumps."""

    def __init__(
        self,
        heat_transfer_assets_in: list[ControllerHeatTransferAsset],
        consumers_in: list[ControllerConsumer],
        producers_in: list[ControllerProducer],
        storage_in: list[ControllerStorage],
    ) -> None:
        """Constructor of the class, which sets all attributes."""
        self.heat_transfer_assets = heat_transfer_assets_in
        self.consumers = consumers_in
        self.producers = producers_in
        self.storage = storage_in

    def get_total_heat_demand(self, time: datetime.datetime) -> float:
        """Method which the total heat demand at the given time."""
        pass

    def get_total_supply(self, priority: int) -> float:
        """Method which returns the total supply of the network"""
        pass

    def set_demand(self, factor: float = 1) -> None:
        pass

    def set_supply(self, total_supply: float, priority: int) -> None:
        pass
