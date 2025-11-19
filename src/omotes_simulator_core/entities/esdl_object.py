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

"""Esdl asset wrapper class."""

import logging

from esdl.esdl_handler import EnergySystemHandler

from omotes_simulator_core.adapter.transforms.string_to_esdl import (
    OmotesAssetLabels,
    StringEsdlAssetMapper,
)
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject

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

    def get_all_assets_of_type(self, esdl_asset_type: OmotesAssetLabels) -> list[EsdlAssetObject]:
        """
        Returns a list of all the esdl assets of the specified type in the esdl file.

        If the type is not found an empty list is returned.
        :param OmotesAssetLabels esdl_asset_type: Type of asset to return
        :return: List of EsdlAssetObject of the specified type
        """
        output_list = []
        for asset_type in StringEsdlAssetMapper().to_esdl(esdl_asset_type):
            esdl_assets = self.energy_system_handler.get_all_instances_of_type(asset_type)
            output_list += [EsdlAssetObject(asset) for asset in esdl_assets]
        return output_list

    def get_connected_assets(self, asset_id: str, port_id: str) -> list[tuple[str, str]]:
        """Method to get the id's of connected assets from the esdl.

        This returns a list of a tuple with the id of the connected asset and the id of the port
        to which the original asset is connected.

        :param str asset_id: id of the asset for which to return the connected assets.
        :param str port_id: id of the port for which to return the connected assets.
        :return: List of tuple with the id of the connected assets and the connected port ids.
        """
        esdl_asset = self.energy_system_handler.get_by_id(asset_id)

        connected_ports = []
        connected_assets = []
        for esdl_port in esdl_asset.port:
            if esdl_port.id == port_id:
                connected_ports = (
                    esdl_port.connectedTo
                )  # TODO: try to maybe only use assets that are enabled here.
                break

        connected_assets = [
            (port.energyasset.id, port.id)
            for port in connected_ports
            if str(port.energyasset.state) == "ENABLED"
        ]

        if not connected_ports or not connected_assets:
            raise ValueError(f"No connected assets found for asset: {asset_id} and port: {port_id}")

        return connected_assets

    def get_asset_by_id(self, asset_id: str) -> EsdlAssetObject:
        """Method to get an asset by its id.

        :param str asset_id: id of the asset to get.
        :return: EsdlAssetObject with the asset.
        """
        return EsdlAssetObject(self.energy_system_handler.get_by_id(asset_id))
