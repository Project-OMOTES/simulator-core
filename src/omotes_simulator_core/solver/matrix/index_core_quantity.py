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

from enum import IntEnum

NUMBER_OF_CORE_QUANTITIES = 3


class CoreQuantity(IntEnum):
    """Offsets of core quantities within a connection point."""

    MASS_FLOW_RATE = 0
    PRESSURE = 1
    INTERNAL_ENERGY = 2


def get_index_property(core_quantity: CoreQuantity, connection_point: int) -> int:
    """Get the component-relative index of a core quantity at a connection point.

    :param core_quantity: The core quantity for which to get the index.
    :param connection_point: The connection point for which to get the index.
    :return: The relative index, without the component's absolute matrix base.
    """
    return int(core_quantity) + connection_point * NUMBER_OF_CORE_QUANTITIES
