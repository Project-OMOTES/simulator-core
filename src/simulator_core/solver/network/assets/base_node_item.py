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
import uuid
from abc import ABC, abstractmethod

from simulator_core.solver.matrix.equation_object import EquationObject
from simulator_core.solver.network.assets.base_item import BaseItem


class BaseNodeItem(ABC):
    """A base class for node items in a network."""

    def __init__(self, number_of_unknowns: int, name: uuid.UUID):
        """Initializes the BaseNodeItem object with the given parameters.

        :param int number_of_unknowns: The number of unknown variables for the item.
        :param uuid.UUID name: The unique identifier of the item.
        """
        self.name = name
        self.number_of_unknowns = number_of_unknowns
        self.matrix_index = 0
        self.prev_sol: list[float] = [0.0] * self.number_of_unknowns

    def set_matrix_index(self, index: int) -> None:
        """Sets the matrix index of the item.

        :param int index: The index of the item in the matrix.
        """
        self.matrix_index = index

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
