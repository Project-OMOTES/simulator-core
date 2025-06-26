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

"""Module containing abstract BaseItem class."""
from abc import ABC, abstractmethod

import numpy as np

from omotes_simulator_core.solver.matrix.equation_object import EquationObject
from omotes_simulator_core.solver.matrix.index_core_quantity import index_core_quantity
from omotes_simulator_core.solver.solver_constants import MASSFLOW_ZERO_LIMIT


class BaseItem(ABC):
    """A base class for items in a network."""

    prev_sol: np.ndarray
    """The previous solution of the calculation, defaults to an array of
    zeros with a certain length (number of unknowns)."""

    def __init__(self, number_of_unknowns: int, name: str, _id: str, number_connection_points: int):
        """Initializes the BaseItem object with the given parameters.

        :param int number_of_unknowns: The number of unknown variables for the item.
        :param str name: The name of the item.
        :param str _id: The unique identifier of the item.
        :param int number_connection_points: The number of connection points of the item.
        """
        self.name = name
        self.id = _id
        self.number_of_unknowns = number_of_unknowns
        self.number_of_connection_point = number_connection_points
        self.matrix_index = 0
        self.massflow_zero_limit = MASSFLOW_ZERO_LIMIT
        self.prev_sol = np.zeros(self.number_of_unknowns)

    def __repr__(self) -> str:
        """Returns the string representation of the item."""
        return str(self.name)

    def reset_prev_sol(self) -> None:
        """Resets the previous solution to zero."""
        self.prev_sol = np.zeros(self.number_of_unknowns)

    def set_matrix_index(self, index: int) -> None:
        """Sets the matrix index of the item.

        :param int index: The index of the item in the matrix.
        """
        self.matrix_index = index

    def get_index_matrix(
        self, property_name: str, connection_point: int, use_relative_indexing: bool
    ) -> int:
        """Returns the index of the property&connection point in the coefficient array or matrix.

        :param str property_name: The property name for which the matrix index is needed.
        :param int connection_point: The connection point for which the matrix index is needed.
        :param bool use_relative_indexing: returns the index into coefficient array for the current
        componentthe matrix if true, otherwise return the index in the complete matrix if false.
        :return: The matrix index for the property and connection point.
        """
        return index_core_quantity.get_index_property(
            property_name=property_name, connection_point=connection_point
        ) + (0 if use_relative_indexing else self.matrix_index)

    @abstractmethod
    def get_equations(self) -> list[EquationObject]:
        """Returns the equations for the item.

        :return: The equations for the item.
        :rtype: list[EquationObject]
        """

    @abstractmethod
    def disconnect_node(self, connection_point: int) -> None:
        """Disconnects a node from the item.

        :param int connection_point: The connection point to disconnect.
        """
