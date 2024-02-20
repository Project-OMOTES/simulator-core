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
"""module containing utility functions for the matrix."""


def relative_difference(value_1: float, value_2: float) -> float:
    """Calculates the relative difference between two points.

    :param value_1: first value to be used
    :param value_2: second value to be used
    :return: Relative difference, return 0 when the difference is 0.
    """
    diff = absolute_difference(value_1, value_2)
    if diff > 0.0:
        return diff / max(abs(value_1), abs(value_2))
    return 0.0


def absolute_difference(value_1: float, value_2: float) -> float:
    """Calculates the absolute difference between two points.

    :param value_1: first value to be used
    :param value_2: second value to be used
    :return: Absolute difference between value 1 and 2
    """
    return abs(value_1 - value_2)
