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

"""Module with class to map and esdl file to an internal graph representation."""

from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.simulation.mappers.mappers import (
    EsdlMapperAbstract,
)
from omotes_simulator_core.adapter.utility.graph import Graph


class EsdlGraphMapper(EsdlMapperAbstract):
    """Class to map an esdl file to an internal graph representation."""

    def __init__(self):
        """Initialize the class."""
        pass

    def to_entity(self, model: EsdlObject) -> Graph:
        """Convert the esdl asset object to an entity."""
        graph = Graph()
        for asset in model.get_all_assets_of_type("heat_transfer"):
            # for heat pumps and heat exchangers, we need to add two nodes one for
            # the primary side and one for the secondary.
            graph.add_node(asset.get_id() + "_primary")
            graph.add_node(asset.get_id() + "_secondary")

        for asset in model.get_all_assets_of_type("asset"):
            if asset.is_heat_exchange_asset():
                continue
            graph.add_node(asset.get_id())

        for asset in model.get_all_assets_of_type("heat_transfer"):
            port_ids = asset.get_port_ids()
            for i in range(len(port_ids)):
                # get ports ids gives an order list of first primary then secondary ports.
                port_str = "_primary" if i < 2 else "_secondary"
                for connected_asset_id in asset.get_connected_assets(port_ids[i]):
                    graph.connect(asset.get_id() + port_str, connected_asset_id)

        for esdl_asset in model.get_all_assets_of_type("asset"):
            if esdl_asset.is_heat_exchange_asset():
                continue
            for port in esdl_asset.get_port_ids():
                for connected_asset_id in esdl_asset.get_connected_assets(port):
                    if model.get_asset_by_id(connected_asset_id).is_heat_exchange_asset():
                        continue
                    graph.connect(esdl_asset.get_id(), connected_asset_id)
        return graph

    def to_esdl(self, entity: Graph) -> EsdlObject:
        """Convert the entity to an esdl asset object."""
        raise NotImplementedError("EsdlEnergySystemMapper.to_esdl()")
