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

"""File containing utility functions for the transforms."""
from typing import Dict, List


def reverse_dict(original_dict: dict) -> Dict[str, List[type]]:
    """Method to reverse a dict.

    Creates a dict with set(values) as keys and the keys of the original dict as list values.

    :param dict original_dict: Dict to be reversed {keys:values}.
    :return: Reversed dict with {set(values):list[keys]}.
    """
    new_dict = {}
    for key, value in original_dict.items():
        if value not in new_dict:
            new_dict[value] = [key]
        else:
            new_dict[value].append(key)
    return new_dict
