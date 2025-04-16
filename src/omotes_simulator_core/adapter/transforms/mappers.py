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
"""Mapper classes."""
import dataclasses

from docutils.io import InputError
from esdl.esdl import Joint as esdl_junction

from omotes_simulator_core.adapter.transforms.controller_mappers import (
    ControllerConsumerMapper,
    ControllerProducerMapper,
    ControllerStorageMapper,
    ControllerHeatTransferMapper,
)
from omotes_simulator_core.adapter.transforms.esdl_asset_mapper import EsdlAssetMapper
from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.controller.controller_consumer import ControllerConsumer
from omotes_simulator_core.entities.assets.controller.controller_heat_transfer import (
    ControllerHeatTransferAsset,
)
from omotes_simulator_core.entities.assets.controller.controller_network import ControllerNetwork
from omotes_simulator_core.entities.assets.controller.controller_producer import ControllerProducer
from omotes_simulator_core.entities.assets.controller.controller_storage import ControllerStorage
from omotes_simulator_core.entities.assets.junction import Junction
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.entities.heat_network import HeatNetwork
from omotes_simulator_core.entities.network_controller import NetworkController
from omotes_simulator_core.entities.network_controller_new import NetworkControllerNew
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract
from omotes_simulator_core.solver.network.network import Network
from omotes_simulator_core.adapter.transforms.esdl_graph_mapper import EsdlGraphMapper
from omotes_simulator_core.adapter.utility.graph import Graph


def replace_joint_in_connected_assets(
    connected_py_assets: list[tuple[str, str]],
    py_joint_dict: dict[str, list[tuple[str, str]]],
    py_asset_id: str,
    iteration_limit: int = 10,
) -> list[tuple[str, str]]:
    """Replace joint with assets connected to the elements.

    Replace items in the connected_py_assets list that are connected to a Joint
    with the items that are connected to the Joint, except for the current asset.

    :param connected_py_assets: List of connected assets
    :param py_joint_dict: Dictionary with joint id as key and list of tuples with
    connected asset id and port as value.
    :param py_asset_id: Id of the asset all the connected assets are connected to
    :param iteration_limit: Limit for the number of iterations

    """
    replace_bool = True
    while replace_bool and iteration_limit > 0:
        replace_bool = False
        iteration_limit -= 1
        for index, connected_py_asset in enumerate(connected_py_assets):
            connected_py_asset_id, _ = connected_py_asset
            if connected_py_asset_id in py_joint_dict:
                # remove the joint from the list and add the connected assets
                connected_py_assets.pop(index)
                # get the connected assets
                additional_assets = py_joint_dict[connected_py_asset_id].copy()
                # remove the current asset from the list
                for index, additional_asset_properties in enumerate(additional_assets):
                    additional_asset_id, _ = additional_asset_properties
                    if additional_asset_id == py_asset_id:
                        additional_assets.pop(index)
                        break
                # add the connected assets to the list
                connected_py_assets.extend(additional_assets)
                replace_bool = True
                break
    if iteration_limit == 0:
        raise RuntimeError("Error in replacing joint in connected assets.")
    else:
        return connected_py_assets


@dataclasses.dataclass
class NetworkItems:
    """Dataclass to hold the different network items."""

    heat_transfer_primary: list[ControllerHeatTransferAsset]
    heat_transfer_secondary: list[ControllerHeatTransferAsset]
    consumer: list[ControllerConsumer]
    producer: list[ControllerProducer]
    storage: list[ControllerStorage]

    def add(self, asset: AssetAbstract) -> None:
        """Add the asset to the correct list."""
        if isinstance(asset, ControllerConsumer):
            self.consumer.append(asset)
        elif isinstance(asset, ControllerProducer):
            self.producer.append(asset)
        elif isinstance(asset, ControllerStorage):
            self.storage.append(asset)
        else:
            raise ValueError("Asset type not recognized.")


class EsdlEnergySystemMapper(EsdlMapperAbstract):
    """Creates a HeatNetwork entity object based on a PyESDL EnergySystem object."""

    def __init__(self, esdl_object: EsdlObject):
        """Constructor for esdl to heat network mapper.

        :param esdl_object: Esdl object to be converted to a Heatnetwork
        """
        self.esdl_object = esdl_object

    def to_esdl(self, entity: HeatNetwork) -> EsdlObject:
        """Method to convert a HeatNetwork object back to an esdlobject.

        For now this method is not implemented.
        :param HeatNetwork entity: HeatNetwork object to be converted to esdl object
        :return: EsdlObject, which is the converted HeatNetwork object.
        """
        raise NotImplementedError("EsdlEnergySystemMapper.to_esdl()")

    def to_entity(self, network: Network) -> tuple[list[AssetAbstract], list[Junction]]:
        """Method to convert esdl to Heatnetwork object.

        This method first converts all assets into a list of assets.
        Next to this a list of Junctions is created. This is then used
        to create the Heatnetwork object.
        :param Network network: network to add the components to.
        :return: (List[AssetAbstract], List[Junction]), tuple of list of assets and junctions.
        """
        # TODO: This method requires a clean-up!
        py_assets_list = self._convert_assets(network)
        py_junction_list = self._create_junctions(network, py_assets_list)

        return py_assets_list, py_junction_list

    def _create_junctions(
        self,
        network: Network,
        py_assets_list: list[AssetAbstract],
    ) -> list[Junction]:
        """Method to create junctions and connect the assets with them.

        :param network: network to add the junctions to.
        :param py_assets_list: list of assets to connect to the junctions.
        :param py_joint_dict: dictionary with all jints in the esdl.

        :return: List of junctions that are created and connected to the assets.
        """
        py_joint_dict = self._get_junction()
        py_junction_list = []
        # loop over assets and create junctions and connect them
        for py_asset in py_assets_list:
            for con_point in range(0, py_asset.number_of_con_points):
                if not py_asset.solver_asset.is_connected(con_point):
                    connected_py_assets = self.esdl_object.get_connected_assets(
                        py_asset.asset_id, py_asset.connected_ports[con_point]
                    )
                    # Replace items in the connected_py_assets list that are connected to a Joint
                    # with the items that are connected to the Joint, except for the current asset.
                    connected_py_assets = replace_joint_in_connected_assets(
                        connected_py_assets, py_joint_dict, py_asset.asset_id
                    )
                    for connected_py_asset, connected_py_port in connected_py_assets:
                        index = [py_asset_temp.asset_id for py_asset_temp in py_assets_list].index(
                            connected_py_asset
                        )
                        con_point_2 = py_assets_list[index].connected_ports.index(connected_py_port)

                        node_id = network.connect_assets(
                            asset1_id=py_asset.solver_asset.name,
                            connection_point_1=con_point,
                            asset2_id=py_assets_list[index].solver_asset.name,
                            connection_point_2=con_point_2,
                        )
                        py_junction_list.append(
                            Junction(network.get_node(node_id), name=str(node_id))
                        )
        return py_junction_list

    def _convert_assets(self, network: Network) -> list[AssetAbstract]:
        """Method to convert all assets from the esdl to a list of pyassets.

        This method loops over all assets in the esdl and converts them to pyassets.

        :param Network network: network to add the components to.
        :return: List of pyassets.
        """
        py_assets_list = []
        for esdl_asset in self.esdl_object.get_all_assets_of_type("asset"):
            # Esdl Junctions need to be skipped in this method, they are added in another method.
            if isinstance(esdl_asset.esdl_asset, esdl_junction):
                continue
            py_assets_list.append(EsdlAssetMapper.to_entity(esdl_asset))
            network.add_existing_asset(py_assets_list[-1].solver_asset)

        return py_assets_list

    def _get_junction(self) -> dict[str, list[tuple[str, str]]]:
        """Method to create an overview of all assets connected to a joint in the esdl.

        This method creates a dictionary with the joint id as key.
        The value is a list of all connected assets and the id of the port it is connected to.

        :return: dict[Any, list[list[tuple[str, str]]], which is the dictionary with the connected
        assets.
        """
        py_joint_dict = {}
        for esdl_joint in self.esdl_object.get_all_assets_of_type("joint"):
            temp_list = [
                self.esdl_object.get_connected_assets(
                    asset_id=esdl_joint.esdl_asset.id, port_id=port
                )
                for port in esdl_joint.get_port_ids()
            ]
            py_joint_dict[esdl_joint.get_id()] = [item for sublist in temp_list for item in sublist]
        return py_joint_dict


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

    def to_entity(self, esdl_object: EsdlObject) -> NetworkController:
        """Method to convert esdl to NetworkController object.

        This method first converts all assets into a list of assets.
        Next to this a list of Junctions is created. This is then used
        to create the NetworkController object.
        :param EsdlObject esdl_object: esdl object to convert to NetworkController object.

        :return: NetworkController, which is the converted EsdlObject object.
        """
        consumers = [
            ControllerConsumerMapper().to_entity(esdl_asset=esdl_asset)
            for esdl_asset in esdl_object.get_all_assets_of_type("consumer")
        ]
        producers = [
            ControllerProducerMapper().to_entity(esdl_asset=esdl_asset)
            for esdl_asset in esdl_object.get_all_assets_of_type("producer")
        ]
        storages = [
            ControllerStorageMapper().to_entity(esdl_asset=esdl_asset)
            for esdl_asset in esdl_object.get_all_assets_of_type("storage")
        ]
        return NetworkController(producers, consumers, storages)

    def to_entity_new(self, esdl_object: EsdlObject) -> NetworkControllerNew:
        """Method to convert esdl to NetworkController object.

        This method first converts all assets into a list of assets.
        Next to this a list of Junctions is created. This is then used
        to create the NetworkController object.
        :param EsdlObject esdl_object: esdl object to convert to NetworkController object.

        :return: NetworkController, which is the converted EsdlObject object.
        """
        # create graph to be able to check for connectivity
        graph = EsdlGraphMapper().to_entity(esdl_object)
        network_list = []
        heat_transfer_assets = [
            ControllerHeatTransferMapper().to_entity(esdl_asset=esdl_asset)
            for esdl_asset in esdl_object.get_all_assets_of_type("heat_transfer")
        ]
        consumers = [
            ControllerConsumerMapper().to_entity(esdl_asset=esdl_asset)
            for esdl_asset in esdl_object.get_all_assets_of_type("consumer")
        ]
        producers = [
            ControllerProducerMapper().to_entity(esdl_asset=esdl_asset)
            for esdl_asset in esdl_object.get_all_assets_of_type("producer")
        ]
        storages = [
            ControllerStorageMapper().to_entity(esdl_asset=esdl_asset)
            for esdl_asset in esdl_object.get_all_assets_of_type("storage")
        ]
        # if there are no heat transfer assets, all assets can be stored into one network.
        if not heat_transfer_assets:
            networks = [
                ControllerNetwork(
                    heat_transfer_assets_prim_in=[],
                    heat_transfer_assets_sec_in=[],
                    consumers_in=consumers,
                    producers_in=producers,
                    storage_in=storages,
                )
            ]
            return NetworkControllerNew(networks=networks)
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
        for asset in consumers + producers + storages:
            for network in network_list:
                if belongs_to_network(asset.id, network, graph):
                    network.add(asset)
                    continue
        # creating network controller classes
        networks = []
        for network in network_list:
            networks.append(
                ControllerNetwork(
                    heat_transfer_assets_prim_in=network.heat_transfer_primary,
                    heat_transfer_assets_sec_in=network.heat_transfer_secondary,
                    consumers_in=network.consumer,
                    producers_in=network.producer,
                    storage_in=network.storage,
                )
            )
        # storing the path from network to the main network (number 0). We use a graph for this.
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
        if not (graph.is_tree()):
            raise InputError(
                "The network is looped via the heat pumps and heat exchangers, "
                "which is not supported."
            )

        for i in range(1, len(networks)):
            networks[i].path = graph.get_path(str(i), "0")
            if len(networks[i].path) > 3:
                raise InputError(
                    "The network is connected via more then two stages which is not supported."
                )
        return NetworkControllerNew(networks=networks)


def belongs_to_network(id: str, network: NetworkItems, graph: Graph) -> bool:
    """Check if the id is connected to a heat transfer asset in the network..

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
