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
from enum import Enum


class PortType(Enum):
    """Enum to define the type of port."""

    IN = 1
    OUT = 2


def sort_ports(connected_ports: list[tuple[str, PortType]]) -> list[str]:
    """Sort the ports of the asset based on the port type.

    The sort order is Inport, Outport, Starting with the first inport, then the first outport
    and so on.

    :param connected_ports: List of tuples with the port id and the port type.
    :return: List of port ids sorted by port type.
    """
    in_ports = [port_id for port_id, port_type in connected_ports if port_type == PortType.IN]
    out_ports = [port_id for port_id, port_type in connected_ports if port_type == PortType.OUT]
    if len(in_ports) != len(out_ports):
        raise ValueError("The number of in ports and out ports are not equal")
    result = []
    for in_port, out_port in zip(in_ports, out_ports):
        result.append(in_port)
        result.append(out_port)
    return result


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
