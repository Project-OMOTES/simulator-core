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
"""Module containing the network class."""
import uuid

import numpy.typing as npt

from omotes_simulator_core.solver.network.assets.base_asset import BaseAsset
from omotes_simulator_core.solver.network.assets.boundary import BaseBoundary
from omotes_simulator_core.solver.network.assets.fall_type import FallType
from omotes_simulator_core.solver.network.assets.heat_transfer_asset import HeatTransferAsset
from omotes_simulator_core.solver.network.assets.node import Node
from omotes_simulator_core.solver.network.assets.production_asset import HeatBoundary
from omotes_simulator_core.solver.network.assets.solver_pipe import SolverPipe


class Network:
    """Class to store a network consisting of nodes and assets."""

    str_to_class_dict = {
        "Boundary": BaseBoundary,
        "Asset": BaseAsset,
        "Fall": FallType,
        "Production": HeatBoundary,
        "Pipe": SolverPipe,
        "HeatTransferAsset": HeatTransferAsset,
    }
    assets: dict[str, BaseAsset]
    nodes: dict[str, Node]

    def __init__(self) -> None:
        """Constructor of the network class.

        Initializes the class properties and loads the fluid properties.
        """
        self.assets = {}
        self.nodes = {}

    def add_asset(
        self, asset_type: str, name: str | None = None, identifier: str | None = None
    ) -> str:
        """Method to add an asset to the network.

        This method creates and asset of the given type.
        If the type does not exist a ValueError is raised.
        The unique id which is created for this asset is returned.
        :param name: Unique name of the asset, if not given a random uuid is created.
        :param str asset_type: The type of asset to be added
        :param str identifier: Unique identifier of the asset, if not given a random uuid is
        created.
        :return: Unique id of the asset.
        """
        if asset_type not in self.str_to_class_dict:
            raise ValueError(asset_type + " not recognized.")
        if name is None:
            name = str(uuid.uuid4())
        if identifier is None:
            identifier = str(uuid.uuid4())
        self.assets[name] = self.str_to_class_dict[asset_type](name=name, _id=identifier)
        return name

    def add_existing_asset(self, asset: BaseAsset) -> str:
        """Method to add an existing asset to the network.

        This method adds an existing asset to the network. It checks if the asset already exists.
        If it does a ValueError is raised.
        :param BaseAsset asset: The asset to be added to the network.
        :return: Unique id of the asset.
        """
        if asset.name in self.assets:
            raise ValueError(f"{asset.name} already exists in network.")
        self.assets[asset.name] = asset
        return asset.name

    def _connect_single_asset_at_node(
        self,
        asset_id_connected: str,
        connection_point_connected: int,
        asset_id_unconnected: str,
        connection_point_unconnected: int,
    ) -> str:
        """Method to connect a single asset to a node.

        This method connects the unconnected asset to the node of the connected asset.
        The id of the node is returned.

        :param asset_id_connected: id of the connected asset
        :type asset_id_connected: str
        :param connection_point_connected: Connection point of the connected asset
        :type connection_point_connected: int
        :param asset_id_unconnected: id of the unconnected asset
        :type asset_id_unconnected: str
        :param connection_point_unconnected: Connection point of the unconnected asset
        :type connection_point_unconnected: int
        :return: id of node connecting the two assets
        """
        # Get the node of the connected asset
        node = self.assets[asset_id_connected].get_connected_node(
            connection_point=connection_point_connected
        )
        # Connect the asset to the node
        self.assets[asset_id_unconnected].connect_node(
            connection_point=connection_point_unconnected, node=node
        )
        # Connect the node to the asset
        node.connect_asset(
            self.assets[asset_id_unconnected], connection_point=connection_point_unconnected
        )
        return node.name

    def _connect_both_assets_at_node(
        self,
        asset1_id: str,
        connection_point_1: int,
        asset2_id: str,
        connection_point_2: int,
    ) -> str:
        """Method to connect to assets at the given connection points.

        Connects the two assets to a new node and returns the id of the node.

        :param asset1_id: id of first asset to be connected
        :type asset1_id: str
        :param connection_point_1: Connection point of first asset to be connected
        :type connection_point_1: int
        :param asset2_id: id of second asset to be connected
        :type asset2_id: str
        :param connection_point_2: Connection point of second asset to be connected
        :type connection_point_2: int
        :return: id of node connecting the two assets
        """
        # Create a new node
        node_id = str(uuid.uuid4())
        self.nodes[node_id] = Node(name=node_id, _id=node_id)
        # Connect the assets to the node
        for asset_id, connection_point in [
            (asset1_id, connection_point_1),
            (asset2_id, connection_point_2),
        ]:
            self.assets[asset_id].connect_node(
                connection_point=connection_point, node=self.nodes[node_id]
            )
            self.nodes[node_id].connect_asset(
                asset=self.assets[asset_id], connection_point=connection_point
            )
        return node_id

    def _connect_both_assets_and_replace_node(
        self,
        asset1_id: str,
        connection_point_1: int,
        asset2_id: str,
        connection_point_2: int,
    ) -> str:
        """Method to connect to assets at the given connection points.

        Connects the two assets to a new node and returns the id of the node.

        :param asset1_id: id of first asset to be connected
        :type asset1_id: str
        :param connection_point_1: Connection point of first asset to be connected
        :type connection_point_1: int
        :param asset2_id: id of second asset to be connected
        :type asset2_id: str
        :param connection_point_2: Connection point of second asset to be connected
        :type connection_point_2: int
        :return: id of node connecting the two assets
        """
        # Retrieve the nodes of the assets
        node1 = self.assets[asset1_id].get_connected_node(connection_point=connection_point_1)
        node2 = self.assets[asset2_id].get_connected_node(connection_point=connection_point_2)
        # Check if the nodes are the same, if so return the name of the node.
        if node1 == node2:
            return node1.name
        else:
            # Both nodes are different, connect the two nodes and remove the second node.
            # First connect all assets connected to the second node to the first node.
            for connected_comp, connection_point in node2.get_connected_assets():
                # Disconnect the connected component from the second node
                connected_comp.disconnect_node(connection_point=connection_point)
                # Connect the connected component to the first node
                self.connect_assets(
                    asset1_id=connected_comp.name,
                    connection_point_1=connection_point,
                    asset2_id=asset1_id,
                    connection_point_2=connection_point_1,
                )
            # Remove the second node from the network
            del self.nodes[node2.name]
            # Finally connect the first asset to the second asset
            self.assets[asset2_id].disconnect_node(connection_point=connection_point_2)
            self.assets[asset2_id].connect_node(connection_point=connection_point_2, node=node1)
            return node1.name

    def connect_assets(
        self,
        asset1_id: str,
        connection_point_1: int,
        asset2_id: str,
        connection_point_2: int,
    ) -> str:
        """Method to connect to assets at the given connection points.

        This method connects the two assets if the exists. It checks if they already are connected.
        If not a new node is created. Otherwise, both are connected to the existing node.
        The id of the node connecting the two is returned

        :param asset1_id: id of first asset to be connected
        :param connection_point_1: Connection point of first asset to be connected
        :param asset2_id: id of second asset to be connected
        :param connection_point_2: Connection point of second asset to be connected
        :return: id of node connecting the two assets
        """
        # Check if both assets exist; if not raise a ValueError
        for asset_id in [asset1_id, asset2_id]:
            self.exists_asset(asset_id=asset_id)
        # Create boolean list with for each asset wether the connection point is connected
        connected_1 = self.assets[asset1_id].is_connected(connection_point=connection_point_1)
        connected_2 = self.assets[asset2_id].is_connected(connection_point=connection_point_2)
        # Use the connect_assets_decision_tree to connect the assets
        return self.connect_assets_decision_tree(
            connected_1=connected_1,
            connected_2=connected_2,
            asset1_id=asset1_id,
            connection_point_1=connection_point_1,
            asset2_id=asset2_id,
            connection_point_2=connection_point_2,
        )

    def connect_assets_decision_tree(
        self,
        connected_1: bool,
        connected_2: bool,
        asset1_id: str,
        connection_point_1: int,
        asset2_id: str,
        connection_point_2: int,
    ) -> str:
        """Method to connect to assets at the given connection points.

        The method uses a decision tree to connect the assets. The decision tree is as follows:
        1. If both assets are not connected, create a new node and connect everything.
        2. If asset 1 is connected and asset 2 is not, connect the node of asset 1 to asset 2.
        3. If asset 2 is connected and asset 1 is not, connect the node of asset 2 to asset 1.
        4. If both assets are connected, check if they are connected to the same node, otherwise
        connect the two nodes and remove the second node.
        5. If none of the above is true raise a NotImplementedError.

        :param connected_1: Boolean indicating if asset 1 is connected
        :param connected_2: Boolean indicating if asset 2 is connected
        :param asset1_id: id of first asset to be connected
        :param connection_point_1: Connection point of first asset to be connected
        :param asset2_id: id of second asset to be connected
        :param connection_point_2: Connection point of second asset to be connected
        :return: id of node connecting the two assets
        """
        if not any([connected_1, connected_2]):
            # both assets are not connected. Create a new node and connect everything.
            return self._connect_both_assets_at_node(
                asset1_id=asset1_id,
                connection_point_1=connection_point_1,
                asset2_id=asset2_id,
                connection_point_2=connection_point_2,
            )
        elif connected_1 and (not connected_2):
            # asset 1 connected asset 2 not, connect the node of asset 1 to asset 2
            return self._connect_single_asset_at_node(
                asset_id_connected=asset1_id,
                connection_point_connected=connection_point_1,
                asset_id_unconnected=asset2_id,
                connection_point_unconnected=connection_point_2,
            )
        elif (not connected_1) and connected_2:
            # asset 2 connected asset 1 not connect the node of asset 2 to asset 1
            return self._connect_single_asset_at_node(
                asset_id_connected=asset2_id,
                connection_point_connected=connection_point_2,
                asset_id_unconnected=asset1_id,
                connection_point_unconnected=connection_point_1,
            )
        else:
            # Effectively we call: all([connected_1, connected_2])
            # both assets are connected, check if they are connected to the same node
            # otherwise connect the two nodes and remove the second node.
            return self._connect_both_assets_and_replace_node(
                asset1_id=asset1_id,
                connection_point_1=connection_point_1,
                asset2_id=asset2_id,
                connection_point_2=connection_point_2,
            )

    def exists_asset(self, asset_id: str) -> bool:
        """Method returns true when an asset with the given id exists in the network.

        :param str asset_id: unique id of the asset to check.

        :return:True when asset exists and False when not
        """
        if asset_id not in self.assets:
            raise ValueError(f"Asset with id:{asset_id} does not exist in network.")
        else:
            return True

    def exists_node(self, node_id: str) -> bool:
        """Method returns true when a node with the given id exists in the network.

        :param str node_id: unique id of the node to check.

        :return:True when node exists and False when not
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node with id:{node_id} does not exist in network.")
        else:
            return True

    def remove_asset(self) -> None:
        """Method to remove an asset from the network."""

    def disconnect_asset(self) -> None:
        """Method to disconnect an asset from the network."""

    def get_asset(self, asset_id: str) -> BaseAsset:  # type: ignore
        """Method to get an asset in the network.

        Method returns the asset with the given id, when it exists in the network.
        when it does not exist a ValueError is raised.

        :param id: asset_id of the asset which needs to be retrieved.
        :type asset_id: str
        :return: Asset
        """
        if self.exists_asset(asset_id):
            return self.assets[asset_id]

    def get_node(self, node_id: str) -> Node:  # type: ignore
        """Method to get a node in the network.

        Method returns the node with the given id, when it exists in the network.
        when it does not exist a ValueError is raised.

        :param node_id: node_id of the node which needs to be retrieved.
        :type node_id: str
        :return: Node
        """
        if self.exists_node(node_id=node_id):
            return self.nodes[node_id]

    def check_connectivity_assets(self) -> bool:
        """Method to check if all assets are connected at all of their connection points.

        Method returns True when all assets are connected and False when an asset is not connected.
        :return: True or False depending on if all assets are connected
        """
        # TODO pass back which assets are not connected.
        result = [asset.is_all_connected() for _, asset in self.assets.items()]
        return all(result)

    def check_connectivity_nodes(self) -> bool:
        """Method to check if all nodes are connected.

        Method returns True when all nodes are connected and False when an node is not connected.
        :return: True or False depending on if all nodes are connected
        """
        result = [node.is_connected() for _, node in self.nodes.items()]
        return all(result)

    def check_connectivity(self) -> bool:
        """Method to check if all nodes and assets are connected.

        :return:True when everything is connected and False when not.
        """
        return self.check_connectivity_assets() and self.check_connectivity_nodes()

    def set_result_asset(self, solution: npt.NDArray) -> None:
        """Method to transfer the solution to the asset in the network.

        :param list[float] solution:Solution to be transferred to the assets.
        :return: None
        """
        for asset in self.assets:
            index = self.get_asset(asset_id=asset).matrix_index
            nou = self.get_asset(asset_id=asset).number_of_unknowns
            self.get_asset(asset_id=asset).prev_sol = solution[index : index + nou].tolist()

    def set_result_node(self, solution: npt.NDArray) -> None:
        """Method to transfer the solution to the nodes in the network.

        :param list[float] solution:Solution to be transferred to the nodes.
        :return: None
        """
        for node in self.nodes:
            index = self.get_node(node_id=node).matrix_index
            nou = self.get_node(node_id=node).number_of_unknowns
            self.get_node(node_id=node).prev_sol = solution[index : index + nou].tolist()

    def print_result(self) -> None:
        """Method to print the result of the network."""
        for asset in self.assets:
            print(type(self.get_asset(asset_id=asset)))
            print(self.get_asset(asset_id=asset).get_result())
