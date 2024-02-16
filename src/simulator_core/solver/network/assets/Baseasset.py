"""Module containing BaseAsset class."""
import math
import uuid
from simulator_core.solver.network.assets.BaseItem import BaseItem
from simulator_core.solver.matrix.equation_object import EquationObject
from simulator_core.solver.matrix.core_enum import IndexEnum, NUMBER_CORE_QUANTITIES
from typing import Dict, TypeVar

Node = TypeVar("Node")


class BaseAsset(BaseItem):
    """A base class for assets in a network.

    This class inherits from BaseItem and provides methods for connecting nodes, checking connection
    status, and adding thermal and pressure equations.

    :param uuid.UUID name: The unique identifier of the asset.
    :param int, optional number_of_unknowns: The number of unknown variables in the asset,
    defaults to 6.
    :param int, optional number_con_points: The number of connection points in the asset,
    defaults to 2.
    """
    connected_nodes: Dict[int, Node]

    def __init__(self, name: uuid.UUID,
                 number_of_unknowns: int = 6, number_con_points: int = 2,
                 supply_temperature: float = 293.15):
        """Initializes the BaseAsset object with the given parameters.

        :param uuid.UUID name: The unique identifier of the node.
        :param int, optional number_of_unknowns: The number of unknown variables for the node.
        The default is 3.
        :param int, optional number_con_points: The number of connection points for the asset.
            The default is 2, which corresponds to the inlet and outlet.
        """
        super().__init__(number_of_unknowns, name)
        self.number_of_connection_point = number_con_points
        self.supply_temperature = supply_temperature
        self.connected_nodes = {}

    def connect_node(self, connection_point: int, node: Node):
        """Connects a node to a connection point of the asset.

        :param connection_point: The index of the connection point to connect.
        :type connection_point: int
        :param node: The node to connect.
        :type node: Node
        :raises ValueError: If the connection point is already connected to a node.
        """
        if connection_point > self.number_of_connection_point:
            raise IndexError(f"Asset {self.name} only has {self.number_of_connection_point}. "
                             f"{connection_point} is to high")
        if connection_point in self.connected_nodes:
            raise ValueError(f" connection point {connection_point}  of asset {self.name} "
                             f" already connected to a node")

        self.connected_nodes[connection_point] = node

    def is_connected(self, connection_point: int) -> bool:
        """Checks if a connection point is connected to a node.

        :param connection_point: The index of the connection point to check.
        :type connection_point: int
        :return: True if the connection point is connected, False otherwise.
        :rtype: bool
        """
        return connection_point in self.connected_nodes

    def get_connected_node(self, connection_point: int) -> Node:
        """Checks if a connection point is connected to a node.

        :param connection_point: The index of the connection point to check.
        :type connection_point: int
        :return: True if the connection point is connected, False otherwise.
        :rtype: bool
        """
        if self.is_connected(connection_point):
            return self.connected_nodes[connection_point]
        raise ValueError(str(connection_point) + " is not connected")

    def is_all_connected(self):
        """Checks if all connection points are connected to nodes.

        :return: True if all connection points are connected, False otherwise.
        :rtype: bool
        """
        result = [self.is_connected(i) for i in range(self.number_of_connection_point)]
        return all(result)

    def add_thermal_equations(self, connection_point: int) -> EquationObject:
        """Adds a thermal equation for a connection point of the asset.

        :param connection_point: The index of the connection point to add the equation for.
        :type connection_point: int
        :return: An equation object representing the thermal equation.
        :rtype: EquationObject
        """
        if self.prev_sol[IndexEnum.discharge + connection_point * NUMBER_CORE_QUANTITIES] > 0:
            return self.add_prescribe_temp(connection_point)
        else:
            return self.add_temp_to_node_equation(connection_point)

    def add_prescribe_temp(self, connection_point: int) -> EquationObject:
        """Adds a prescribed temperature equation for a connection point of the asset.

        :param connection_point: The index of the connection point to add the equation for.
        :type connection_point: int
        :return: An equation object representing the prescribed temperature equation.
        :rtype: EquationObject
        """
        equation_object = EquationObject()
        equation_object.indices = [self.matrix_index + IndexEnum.internal_energy
                                   + connection_point * NUMBER_CORE_QUANTITIES]
        equation_object.coefficients = [1.0]
        equation_object.rhs = self.fluid_properties.get_ie(self.supply_temperature)
        return equation_object

    def add_temp_to_node_equation(self, connection_point: int) -> EquationObject:
        """Adds a temperature to node equation for a connection point of the asset.

        :param connection_point: The index of the connection point to add the equation for.
        :type connection_point: int
        :return: An equation object representing the temperature to node equation.
        :rtype: EquationObject
        """
        equation_object = EquationObject()
        equation_object.indices = [self.matrix_index + IndexEnum.internal_energy +
                                   connection_point * NUMBER_CORE_QUANTITIES,
                                   self.get_connected_node(connection_point).matrix_index +
                                   IndexEnum.internal_energy]
        equation_object.coefficients = [1.0, -1.0]
        equation_object.rhs = 0.0
        return equation_object

    def add_press_to_node_equation(self, connection_point: int) -> EquationObject:
        """Adds a pressure to node equation for a connection point of the asset.

        :param connection_point: The index of the connection point to add the equation for.
        :type connection_point: int
        :return: An equation object representing the pressure to node equation.
        :rtype: EquationObject
        """
        equation_object = EquationObject()
        equation_object.indices = [self.matrix_index + IndexEnum.pressure
                                   + connection_point * NUMBER_CORE_QUANTITIES,
                                   self.connected_nodes[connection_point].matrix_index
                                   + IndexEnum.pressure]
        equation_object.coefficients = [1.0, -1.0]
        equation_object.rhs = 0.0
        return equation_object

    def get_result(self) -> list[float]:
        """Method to get the result of the asset.

        :return: a list of the unknowns which are solved.
        """
        results = []
        for i in range(self.number_of_connection_point):
            for j in range(math.floor(self.number_of_unknowns / self.number_of_connection_point)):
                if j == 2:
                    results.append(self.fluid_properties.get_t(
                        self.prev_sol[i * math.floor(self.number_of_unknowns
                                                     / self.number_of_connection_point) + j]))
                else:
                    results.append(self.prev_sol[i * math.floor(self.number_of_unknowns
                                                                / self.number_of_connection_point) + j])
        return results

    def get_equations(self) -> list[EquationObject]:
        return []
