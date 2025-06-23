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

"""Module containing abstract BaseNodeItem class."""
from abc import ABC, abstractmethod

from omotes_simulator_core.solver.matrix.equation_object import EquationObject
from omotes_simulator_core.solver.matrix.index_core_quantity import index_core_quantity
from omotes_simulator_core.solver.network.assets.base_item import BaseItem
from omotes_simulator_core.solver.solver_constants import MASSFLOW_ZERO_LIMIT


class BaseNodeItem(ABC):
    """A base class for node items in a network."""

    def __init__(self, name: str, _id: str, number_of_unknowns: int):
        """Initializes the BaseNodeItem object with the given parameters.

        :param int number_of_unknowns: The number of unknown variables for the item.
        :param str name: The name of the node.
        :param str _id: The unique identifier of the node.
        """
        self.name = name
        self.id = _id
        self.number_of_unknowns = number_of_unknowns
        self.matrix_index = 0
        self.massflow_zero_limit = MASSFLOW_ZERO_LIMIT
        self.prev_sol: list[float] = [0.0] * self.number_of_unknowns

    def reset_prev_sol(self) -> None:
        """Resets the previous solution to zero."""
        self.prev_sol = [0.0] * self.number_of_unknowns

    def set_matrix_index(self, index: int) -> None:
        """Sets the matrix index of the item.

        :param int index: The index of the item in the matrix.
        """
        self.matrix_index = index

    def get_index_matrix(self, property_name: str, use_relative_indexing: bool) -> int:
        """Method to get matrix index of a certain property for a connection point.

        :param str property_name: The property name for which the matrix index is needed.
        :param bool matrix: Whether the index in the matrix should be included.
        :return: The matrix index for the property and connection point.
        """
        return index_core_quantity.get_index_property(
            property_name=property_name, connection_point=0
        ) + (0 if use_relative_indexing else self.matrix_index)

    @abstractmethod
    def get_equations(self) -> list[EquationObject]:
        """Returns the equations for the item.

        :return: The equations for the item.
        :rtype: list[EquationObject]
        """

    @abstractmethod
    def connect_asset(self, asset: BaseItem, connection_point: int) -> None:
        """Connects the asset to the node item.

        :param BaseItem asset: The asset to connect to the node item.
        :param int connection_point: The connection point of the asset to connect to.
        """

    @abstractmethod
    def get_connected_assets(self) -> list[tuple[BaseItem, int]]:
        """Returns the connected assets of the node item.

        :return: The connected assets of the node item.
        :rtype: Tuple[BaseItem, int]
        """
