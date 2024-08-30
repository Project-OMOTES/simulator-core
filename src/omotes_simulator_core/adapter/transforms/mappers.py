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
from typing import Dict, List, Tuple

from esdl.esdl import Joint as esdl_junction

from omotes_simulator_core.adapter.transforms.esdl_asset_mapper import EsdlAssetMapper
from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract

from omotes_simulator_core.entities.assets.junction import Junction
from omotes_simulator_core.entities.assets.utils import Port
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.entities.heat_network import HeatNetwork
from omotes_simulator_core.entities.network_controller import NetworkController
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract
from omotes_simulator_core.solver.network.network import Network
from omotes_simulator_core.adapter.transforms.esdl_asset_mapper import (
    EsdlAssetControllerProducerMapper,
)
from omotes_simulator_core.adapter.transforms.esdl_asset_mapper import (
    EsdlAssetControllerConsumerMapper,
)
from omotes_simulator_core.adapter.transforms.esdl_asset_mapper import (
    EsdlAssetControllerStorageMapper,
)


def connect_connected_asset(
    connected_py_assets: List[Tuple[str, Port]],
    junction: Junction,
    py_assets_list: List[AssetAbstract],
) -> None:
    """Method to connect assets connected to one asset to the same junction.

    :param connected_py_assets: List of connected assets
    :param junction: Junction to connect the assets to
    :param py_assets_list: List of assets
    :return: None
    """
    for connected_py_asset in connected_py_assets:
        index = [py_asset_temp.asset_id for py_asset_temp in py_assets_list].index(
            connected_py_asset[0]
        )
        if connected_py_asset[1] == Port.In:  # from
            py_assets_list[index].set_from_junction(from_junction=junction)
        else:  # to
            py_assets_list[index].set_to_junction(to_junction=junction)


def replace_joint_in_connected_assets(
    connected_py_assets: List[Tuple[str, Port]],
    py_joint_dict: Dict[str, List[Tuple[str, Port]]],
    py_asset_id: str,
    iteration_limit: int = 10,
) -> List[Tuple[str, Port]]:
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

    def to_entity(self, network: Network) -> Tuple[List[AssetAbstract], List[Junction]]:
        """Method to convert esdl to Heatnetwork object.

        This method first converts all assets into a list of assets.
        Next to this a list of Junctions is created. This is then used
        to create the Heatnetwork object.
        :param Network network: network to add the compenents to.
        :return: (List[AssetAbstract], List[Junction]), tuple of list of assets and junctions.
        """
        # TODO: This method requires a clean-up!
        py_assets_list = []
        py_joint_dict = {}
        for esdl_asset in self.esdl_object.get_all_assets_of_type("asset"):
            # Esdl Junctions need to be skipped for now, are added later.
            if isinstance(esdl_asset.esdl_asset, esdl_junction):
                py_joint_dict[esdl_asset.esdl_asset.id] = [
                    *self.esdl_object.get_connected_assets(esdl_asset.esdl_asset.id, Port.In),
                    *self.esdl_object.get_connected_assets(esdl_asset.esdl_asset.id, Port.Out),
                ]
            else:
                py_assets_list.append(EsdlAssetMapper().to_entity(esdl_asset))
                py_assets_list[-1].add_physical_data(esdl_asset=esdl_asset)
                network.add_existing_asset(py_assets_list[-1].solver_asset)

        py_junction_list = []

        # loop over assets and create junctions and connect them
        for py_asset in py_assets_list:
            for con_point in range(0, 2):
                if not py_asset.solver_asset.is_connected(con_point):
                    connected_py_assets = self.esdl_object.get_connected_assets(
                        py_asset.asset_id, Port.In if con_point == 0 else Port.Out
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
                        if connected_py_port == Port.In:
                            node_id = network.connect_assets(
                                asset1_id=py_asset.solver_asset.name,
                                connection_point_1=con_point,
                                asset2_id=py_assets_list[index].solver_asset.name,
                                connection_point_2=0,
                            )
                            py_junction_list.append(
                                Junction(network.get_node(node_id), name=str(node_id))
                            )
                            py_assets_list[index].set_to_junction(py_junction_list[-1])
                        else:
                            node_id = network.connect_assets(
                                asset1_id=py_asset.solver_asset.name,
                                connection_point_1=con_point,
                                asset2_id=py_assets_list[index].solver_asset.name,
                                connection_point_2=1,
                            )
                            py_junction_list.append(
                                Junction(network.get_node(node_id), name=str(node_id))
                            )
                            py_assets_list[index].set_from_junction(py_junction_list[-1])
                        # connect the connected assets to the junction
                        if con_point == 0:
                            py_asset.set_to_junction(py_junction_list[-1])
                        else:
                            py_asset.set_from_junction(py_junction_list[-1])

        return py_assets_list, py_junction_list


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
            EsdlAssetControllerConsumerMapper().to_entity(esdl_asset=esdl_asset)
            for esdl_asset in esdl_object.get_all_assets_of_type("consumer")
        ]
        producers = [
            EsdlAssetControllerProducerMapper().to_entity(esdl_asset=esdl_asset)
            for esdl_asset in esdl_object.get_all_assets_of_type("producer")
        ]
        storages = [
            EsdlAssetControllerStorageMapper().to_entity(esdl_asset=esdl_asset)
            for esdl_asset in esdl_object.get_all_assets_of_type("storage")
        ]
        return NetworkController(producers, consumers, storages)
