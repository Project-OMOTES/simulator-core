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
"""Module containing the class for a heat trasnfer asset."""

from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
    AssetControllerAbstract,
)
from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_TEMPERATURE_SUPPLY,
    PROPERTY_TEMPERATURE_RETURN,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_SET_PRESSURE,
)


class ControllerHeatTransferAsset(AssetControllerAbstract):
    """Class for controlling a heat transfer asset."""

    def __init__(self, name: str, identifier: str, factor: float):
        """Constructor of the class, which sets all attributes.

        :param str name: Name of the consumer.
        :param str identifier: Unique identifier of the consumer.
        """
        super().__init__(name, identifier)
        self.factor = factor

    def set_asset(self, heat_demand: float) -> dict[str, dict[str, float]]:
        """Method to set the asset to the given heat demand.

        The supply and return temperatures are also set.
        :param float heat_demand: Heat demand to set.
        """

        return {
            self.id: {
                PROPERTY_HEAT_DEMAND: heat_demand,
                PROPERTY_TEMPERATURE_RETURN: 293.15,  # TODO set correct values also for prim and secondary side.
                PROPERTY_TEMPERATURE_SUPPLY: 293.15,
                PROPERTY_SET_PRESSURE: False,
            }
        }
