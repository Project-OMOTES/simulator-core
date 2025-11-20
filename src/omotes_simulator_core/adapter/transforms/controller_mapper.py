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
"""Mapper class to convert ESDL objects to internal controller objects."""
import dataclasses
from typing import Optional

from omotes_simulator_core.adapter.transforms.controller_mappers import (
    ControllerConsumerMapper,
    ControllerHeatExchangeMapper,
    ControllerHeatPumpMapper,
    ControllerProducerMapper,
    ControllerStorageMapper,
)
from omotes_simulator_core.adapter.transforms.esdl_graph_mapper import EsdlGraphMapper
from omotes_simulator_core.adapter.transforms.mappers import EsdlMapperAbstract
from omotes_simulator_core.adapter.transforms.string_to_esdl import OmotesAssetLabels
from omotes_simulator_core.adapter.utility.graph import Graph
from omotes_simulator_core.entities.assets.controller import (
    ControllerConsumer,
    ControllerHeatTransferAsset,
    ControllerNetwork,
    ControllerProducer,
    ControllerStorage,
)
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.entities.network_controller import NetworkController


@dataclasses.dataclass
class NetworkItems:
    """Dataclass to hold the different network items."""

    heat_transfer_primary: list[ControllerHeatTransferAsset]
    heat_transfer_secondary: list[ControllerHeatTransferAsset]
    consumer: list[ControllerConsumer]
    producer: list[ControllerProducer]
    storage: list[ControllerStorage]

    def add(self, asset: ControllerStorage | ControllerProducer | ControllerConsumer) -> None:
        """Add the asset to the correct list."""
        if isinstance(asset, ControllerConsumer):
            self.consumer.append(asset)
        elif isinstance(asset, ControllerProducer):
            self.producer.append(asset)
        elif isinstance(asset, ControllerStorage):
            self.storage.append(asset)
        else:
            raise ValueError("Asset type not recognized.")


class EsdlControllerMapper(EsdlMapperAbstract):
    """Creates a NetworkController entity object based on a PyESDL EnergySystem object."""

    def __init__(self) -> None:
        """Constructor for esdl to heat network mapper."""

    def to_esdl(self, entity: NetworkController) -> EsdlObject:
        """Method to convert a NetworkController object to an esdlobject.

        For now this method is not implemented.
        :param NetworkController entity: NetworkController object to be converted to esdl object
        :return: EsdlObject, which is the converted NetworkController object.
        """
        raise NotImplementedError("EsdlControllerMapper.to_esdl()")

    def to_entity(
        self, esdl_object: EsdlObject, timestep: Optional[int] = None
    ) -> NetworkController:
        """Method to convert esdl to NetworkController object.

        This method first converts all assets into a list of assets.
        Next to this a list of Junctions is created. This is then used
        to create the NetworkController object.
        :param EsdlObject esdl_object: esdl object to convert to NetworkController object.
        :param int timestep: Simulation timestep in seconds.

        :return: NetworkController, which is the converted EsdlObject object.
        """
        # create graph to be able to check for connectivity
        graph = EsdlGraphMapper().to_entity(esdl_object)

        heat_transfer_assets = [
            ControllerHeatPumpMapper().to_entity(esdl_asset=esdl_asset)
            for esdl_asset in esdl_object.get_all_assets_of_type(OmotesAssetLabels.HEAT_PUMP)
            if esdl_asset.get_number_of_ports() == 4
        ] + [
            ControllerHeatExchangeMapper().to_entity(esdl_asset=esdl_asset)
            for esdl_asset in esdl_object.get_all_assets_of_type(OmotesAssetLabels.HEAT_EXCHANGER)
        ]

        consumers = [
            ControllerConsumerMapper().to_entity(esdl_asset=esdl_asset, timestep=timestep)
            for esdl_asset in esdl_object.get_all_assets_of_type(OmotesAssetLabels.CONSUMER)
        ]
        producers = [
            ControllerProducerMapper().to_entity(esdl_asset=esdl_asset)
            for esdl_asset in esdl_object.get_all_assets_of_type(OmotesAssetLabels.PRODUCER)
        ] + [
            ControllerProducerMapper().to_entity(esdl_asset=esdl_asset)
            for esdl_asset in esdl_object.get_all_assets_of_type(OmotesAssetLabels.HEAT_PUMP)
            if esdl_asset.get_number_of_ports() == 2
        ]

        storages = [
            ControllerStorageMapper().to_entity(esdl_asset=esdl_asset, timestep=timestep)
            for esdl_asset in esdl_object.get_all_assets_of_type(OmotesAssetLabels.STORAGE)
        ]

        # if there are no heat transfer assets, all assets can be stored into one network.
        if not heat_transfer_assets:
            networks = [
                ControllerNetwork(
                    heat_transfer_assets_prim_in=[],
                    heat_transfer_assets_sec_in=[],
                    consumers_in=consumers,
                    producers_in=producers,
                    storages_in=storages,
                )
            ]
            return NetworkController(networks=networks)
        network_list = self.heat_transfer_assets_to_network(graph, heat_transfer_assets)
        self.assets_to_networks(graph, network_list, consumers + producers + storages)
        # creating network controller classes
        networks = []
        for network in network_list:
            networks.append(
                ControllerNetwork(
                    heat_transfer_assets_prim_in=network.heat_transfer_primary,
                    heat_transfer_assets_sec_in=network.heat_transfer_secondary,
                    consumers_in=network.consumer,
                    producers_in=network.producer,
                    storages_in=network.storage,
                )
            )
        # storing the path from network to the main network (number 0). We use a graph for this.
        graph = self.networks_to_graph(networks)
        if not (graph.is_tree()):
            raise RuntimeError(
                "The network is looped via the heat pumps and heat exchangers, "
                "which is not supported."
            )

        for i in range(1, len(networks)):
            networks[i].path = graph.get_path(str(i), "0")
            if len(networks[i].path) > 3:
                raise RuntimeError(
                    "The network is connected via more then two stages which is not supported."
                )
        return NetworkController(networks=networks)

    def networks_to_graph(self, networks: list[ControllerNetwork]) -> Graph:
        """Create a graph from the networks.

        This graph is used to check the connectivity between the networks.
        The networks are simply named 0,1 etc.

        :param networks: list of networks to create the graph from.
        :return: Graph, which is the created graph from the networks.
        """
        graph = Graph()
        for i in range(len(networks)):
            graph.add_node(str(i))
        for i in range(len(networks)):
            for heat_transfer_asset in networks[i].heat_transfer_assets_prim:
                for j in range(len(networks)):
                    if i == j:
                        continue
                    if networks[j].exists(heat_transfer_asset.id):
                        graph.connect(str(i), str(j))
        return graph

    def assets_to_networks(
        self,
        graph: Graph,
        network_list: list[NetworkItems],
        assets: list[ControllerConsumer | ControllerProducer | ControllerStorage],
    ) -> None:
        """Method to move assets to networks.

        :param graph: for checking connectivity.
        :param network_list: list of NetworkItems to add the assets to.
        :param assets: list of assets to be added to networks.
        """
        for asset in assets:
            for network in network_list:
                if belongs_to_network(asset.id, network, graph):
                    network.add(asset)
                    continue

    def heat_transfer_assets_to_network(
        self, graph: Graph, heat_transfer_assets: list[ControllerHeatTransferAsset]
    ) -> list[NetworkItems]:
        """Method to move heat transfer assets to networks. or create new networks.

        :param graph: for checking connectivity.
        :param heat_transfer_assets: list of heat transfer assets to be added to networks.
        :return: list of NetworkItems, which are the networks with the heat transfer assets.
        """
        network_list: list[NetworkItems] = []
        for heat_transfer_asset in heat_transfer_assets:
            # First check if the heat transfer asset is connected to a network that already
            # is in the list
            belongs = False
            for network in network_list:
                if belongs_to_network(heat_transfer_asset.id + "_primary", network, graph):
                    network.heat_transfer_primary.append(heat_transfer_asset)
                    belongs = True
                    break
            if not belongs:
                network_list.append(
                    NetworkItems(
                        heat_transfer_primary=[heat_transfer_asset],
                        heat_transfer_secondary=[],
                        consumer=[],
                        producer=[],
                        storage=[],
                    )
                )
            belongs = False
            for network in network_list:
                if belongs_to_network(heat_transfer_asset.id + "_secondary", network, graph):
                    network.heat_transfer_primary.append(heat_transfer_asset)
                    belongs = True
                    break
            if not belongs:
                network_list.append(
                    NetworkItems(
                        heat_transfer_primary=[],
                        heat_transfer_secondary=[heat_transfer_asset],
                        consumer=[],
                        producer=[],
                        storage=[],
                    )
                )
        return network_list


def belongs_to_network(id: str, network: NetworkItems, graph: Graph) -> bool:
    """Check if the id is connected to a heat transfer asset in the network.

    :param id: id to check if it belongs to the network.
    :param network: NetworkItems to check if the id belongs to the network.
    :param graph: for checking connectivity.
    :return: bool, which is True if the id belongs to the network.
    """
    if network.heat_transfer_primary:
        if graph.is_connected(network.heat_transfer_primary[0].id + "_primary", id):
            return True
    if network.heat_transfer_secondary:
        if graph.is_connected(network.heat_transfer_secondary[0].id + "_secondary", id):
            return True
    return False
