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

    def get_index_property(self, property_name: str, connection_point: int) -> int:
        """Method to get the property of the index."""
        return self.get_index(property_name) + connection_point * self.number_core_quantities

    def get_index(self, property_name: str) -> int:
        """Method to get the index of the property."""
        return int(getattr(self, property_name))


index_core_quantity = IndexCoreQuantity()
