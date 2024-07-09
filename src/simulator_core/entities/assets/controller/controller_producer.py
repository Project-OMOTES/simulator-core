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

from simulator_core.entities.assets.asset_defaults import (DEFAULT_TEMPERATURE,
                                                           DEFAULT_TEMPERATURE_DIFFERENCE)
from simulator_core.entities.assets.controller.controller_classes import AssetControllerAbstract
from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject


class ControllerProducer(AssetControllerAbstract):
    """Class to store the source for the controller."""

    def __init__(self, name: str, identifier: str):
        """Constructor for the source.

        :param str name: Name of the source.
        :param str identifier: Unique identifier of the source.
        """
        super().__init__(name, identifier)
        self.temperature_return: float = DEFAULT_TEMPERATURE
        self.temperature_supply: float = DEFAULT_TEMPERATURE + DEFAULT_TEMPERATURE_DIFFERENCE
        self.power: float = 1000
        self.priority: int = 1

    def set_controller_data(self, esdl_asset: EsdlAssetObject) -> None:
        """Method to get the controller data for esdl object."""
        result = esdl_asset.get_property(
            esdl_property_name="power", default_value=self.power
        )
        if result[1]:
            self.power = result[0]
        else:
            raise ValueError("No power found for asset: " + esdl_asset.esdl_asset.name)
        self.temperature_supply = esdl_asset.get_supply_temperature("Out")
        self.temperature_return = esdl_asset.get_return_temperature("In")
