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

from omotes_simulator_core.adapter.transforms.string_to_esdl import OmotesAssetLabels
from omotes_simulator_core.adapter.utility.graph import Graph
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract


class EsdlGraphMapper(EsdlMapperAbstract):
    """Class to map an esdl file to an internal graph representation."""

    def __init__(self) -> None:
        """Initialize the class."""
        pass

    def to_entity(self, model: EsdlObject) -> Graph:
        """Convert the esdl asset object to an entity.

        Args:
            model (EsdlObject): The esdl model to convert.
        """
        graph = Graph()
        assets_to_graph(graph=graph, model=model)
        create_graph_nodes(graph=graph, model=model)
        return graph

    def to_esdl(self, entity: Graph) -> EsdlObject:
        """Convert the entity to an esdl asset object."""
        raise NotImplementedError("EsdlEnergySystemMapper.to_esdl()")


def create_graph_nodes(graph: Graph, model: EsdlObject) -> None:
    """Creates the connections between the nodes in the graph based on the connection in the model.

    For heat transfer assets, connections are made from the primary and secondary nodes to the
    connected assets. Please note that the assets first have to be added to the graph with the
    assets_to_graph function.

    Args:
        graph (Graph): The graph to add the connections to.
        model (EsdlObject): The esdl model to get the assets from.
    """
    for esdl_asset in model.get_all_assets_of_type(OmotesAssetLabels.ASSET):
        if esdl_asset.is_heat_transfer_asset():
            if not graph.node_exists(esdl_asset.get_id() + "_primary"):
                raise ValueError(f"Graph does not contain node {esdl_asset.get_id() + '_primary'}")
            port_ids = esdl_asset.get_port_ids()
            for i in range(len(port_ids)):
                # get ports ids gives an order list of first primary then secondary ports.
                port_str = "_primary" if i < 2 else "_secondary"
                for connected_asset_id in esdl_asset.get_connected_assets(port_ids[i]):
                    graph.connect(esdl_asset.get_id() + port_str, connected_asset_id)
            continue
        for port in esdl_asset.get_port_ids():
            if not graph.node_exists(esdl_asset.get_id()):
                raise ValueError(f"Graph does not contain node {esdl_asset.get_id()}")
            for connected_asset_id in esdl_asset.get_connected_assets(port):
                if model.get_asset_by_id(connected_asset_id).is_heat_transfer_asset():
                    continue
                graph.connect(esdl_asset.get_id(), connected_asset_id)


def assets_to_graph(graph: Graph, model: EsdlObject) -> None:
    """Converts all assets in the esdl object to nodes in the graph.

    For heat exchangers and heat pumps, two nodes are added, one for the primary
    side and one for the secondary side. All other assets are added as a single node.

    Args:
        graph (Graph): The graph to add the nodes to.
        model (EsdlObject): The esdl model to get the assets from.
    """
    for asset in model.get_all_assets_of_type(OmotesAssetLabels.ASSET):
        # heat transfer assets have two sides, so we add two nodes to the graph a primary
        # and secondary one
        if asset.is_heat_transfer_asset():
            graph.add_node(asset.get_id() + "_primary")
            graph.add_node(asset.get_id() + "_secondary")
            continue
        graph.add_node(asset.get_id())
