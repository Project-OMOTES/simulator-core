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
from typing import List, Tuple

from esdl import InPort, OutPort
from esdl.esdl_handler import EnergySystemHandler

from omotes_simulator_core.adapter.transforms.string_to_esdl import StringEsdlAssetMapper
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.entities.assets.utils import Port

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
        output_list = []
        for asset_type in StringEsdlAssetMapper().to_esdl(esdl_asset_type):
            output_list += [
                EsdlAssetObject(asset)
                for asset in self.energy_system_handler.get_all_instances_of_type(asset_type)
            ]
        return output_list

    def get_connected_assets(self, asset_id: str, port: Port) -> List[Tuple[str, Port]]:
        """Method to get the id's of connected assets from the esdl.

        This returns a list of list with the connected asset id and the port to which it is
        connected to the asset.
        First it is set if the request is an in or outport. Then the connected ports to the asset
        are added to a list. In the final step all assets elong to the ports are listed together
        with the type of port they are connected to.

        :param str id: id of the asset for which we want to know the connected assets
        :param Port port: port for which the connected assets need to be returned.
        :return: List of list which the id of the connected assets and the connected port.
        """
        # TODO 1. Add support for components with multiple in and outports, like heat exchanger
        # TODO 2. What if it is connected to a joint?
        connected_assets = []
        esdl_asset = self.energy_system_handler.get_by_id(asset_id)

        type_port = OutPort if port == Port.Out else InPort
        connected_port_ids = []
        for esdl_port in esdl_asset.port:
            if isinstance(esdl_port, type_port):
                connected_port_ids = esdl_port.connectedTo
                break
        for connected_port_id in connected_port_ids:
            connected_port_type = Port.Out if isinstance(connected_port_id, OutPort) else Port.In
            connected_assets.append((connected_port_id.energyasset.id, connected_port_type))
        return connected_assets
