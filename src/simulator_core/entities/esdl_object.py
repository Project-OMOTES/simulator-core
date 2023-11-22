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

""" Esdl asset wrapper class."""

import logging

from esdl.esdl_handler import EnergySystemHandler

from simulator_core.adapter.transforms.string_to_esdl import StringEsdlAssetMapper
from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject

logger = logging.getLogger(__name__)


class EsdlObject:
    """EsdlObject class is a wrapper around PyEsdl."""

    energy_system_handler: EnergySystemHandler

    def __init__(self, esdl_energysystem_handler: EnergySystemHandler) -> None:
        """
        Constructor for EsdlObject.

        :param esdl_energysystem: PyEsdl EnergySystem object
        """
        self.energy_system_handler = esdl_energysystem_handler

    def __repr__(self) -> str:
        """Returns a string describing the esdl file object."""
        return str(self.energy_system_handler)

    def get_all_assets_of_type(self, esdl_asset_type: str) -> list[EsdlAssetObject]:
        """
        Returns a list of all the esdl assets of the specified type in the esdl file.

        If the type is not found an empty list is returned.
        :param esdl_asset_type: str of the asset type assets need to be gathered.
        """
        return [
            EsdlAssetObject(asset)
            for asset in self.energy_system_handler.get_all_instances_of_type(
                StringEsdlAssetMapper().to_esdl(esdl_asset_type)
            )
        ]
