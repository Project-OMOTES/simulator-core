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

    @property
    def prev_sol(self) -> np.ndarray:
        """The previous solution of the calculation.

        Defaults to an array of zeros with a certain length (number of unknowns).
        """
        return self._prev_sol

    @prev_sol.setter
    def prev_sol(self, value: np.ndarray) -> None:
        """Stores the previous solution and invalidates the values derived from it.

        :param value: The previous solution of the calculation.
        :return: None
        """
        self._prev_sol = value
        self.invalidate_solution_cache()

    def invalidate_solution_cache(self) -> None:  # noqa: B027
        """Invalidates the values which items derive from the previous solution.

        Items which cache values that only depend on the previous solution, such as fluid
        properties, implement this method to discard those values. Items without such a cache
        do not have to implement this method, therefore it is not abstract.
        """

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
        # The matrix indices of the cached equations are no longer valid.
        self.reset_cached_equations()

    def reset_cached_equations(self) -> None:  # noqa: B027
        """Resets the cached equation objects of the item.

        Equations of which the indices and coefficients do not change between iterations are
        created once and stored on the item. This method invalidates those equations, so that
        they are recreated when they are requested again. Items which do not cache equations
        do not have to implement this method, therefore it is not abstract.
        """

    def get_index_matrix(
        self, property_name: str, connection_point: int, use_relative_indexing: bool
    ) -> int:
        """Returns the index of the property&connection point in the coefficient array or matrix.

        :param str property_name: The property name for which the matrix index is needed.
        :param int connection_point: The connection point for which the matrix index is needed.
        :param bool use_relative_indexing: returns the index into coefficient array for the current
            component matrix if true, otherwise return the index in the complete matrix if false.

        :return: The matrix index for the property and connection point.
        """
        relative_index = index_core_quantity.get_index_property(
            property_name=property_name, connection_point=connection_point
        )
        if use_relative_indexing:
            return relative_index
        return relative_index + self.matrix_index

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
