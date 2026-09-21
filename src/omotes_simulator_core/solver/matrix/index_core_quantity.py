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
"""Classes for storing core quantities of the matrix."""
import dataclasses


@dataclasses.dataclass
class IndexCoreQuantity:
    """Enum for the index of the matrix.

    This is used to store the order of the core quants in the matrix.
    The number of core quantities is the maximum number of core quantities used.
    for the indices these should be in increasing order. This is not checked.
    """

    number_core_quantities = 3
    mass_flow_rate = 0
    pressure = 1
    internal_energy = 2

    _property_names = ("mass_flow_rate", "pressure", "internal_energy")
    """The names of the core quantities for which the index table is created."""

    _maximum_cached_connection_point = 8
    """The highest connection point for which the index table is created."""

    def __post_init__(self) -> None:
        """Creates the lookup table with the index per property and connection point.

        The index of a property and connection point is requested millions of times during a
        simulation. Looking the index up in a dictionary is considerably faster than retrieving
        the attribute by its name and calculating the offset of the connection point.

        :return: None
        """
        self._index_table: dict[tuple[str, int], int] = {
            (property_name, connection_point): int(getattr(self, property_name))
            + connection_point * self.number_core_quantities
            for property_name in self._property_names
            for connection_point in range(self._maximum_cached_connection_point + 1)
        }

    def get_index_property(self, property_name: str, connection_point: int) -> int:
        """Method to get the property of the index."""
        index = self._index_table.get((property_name, connection_point))
        if index is None:
            return self.get_index(property_name) + connection_point * self.number_core_quantities
        return index

    def get_index(self, property_name: str) -> int:
        """Method to get the index of the property."""
        return int(getattr(self, property_name))


index_core_quantity = IndexCoreQuantity()
