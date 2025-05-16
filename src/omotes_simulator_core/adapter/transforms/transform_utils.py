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
from dataclasses import dataclass
from enum import Enum


class PortType(Enum):
    """Enum to define the type of port."""

    IN = 1
    OUT = 2


@dataclass
class Port:
    """Dataclass to hold the port information."""

    port_id: str
    port_name: str
    port_type: PortType


def sort_ports(connected_ports: list[Port]) -> list[str]:
    """Sort the ports of the asset based on the port type.

    The sort order is Inport, Outport, Starting with the first inport, then the first outport
    and so on.

    :param connected_ports: List of tuples with the port id, name and the port type.
    :return: List of port ids sorted by port type.
    """
    in_ports = [port for port in connected_ports if port.port_type == PortType.IN]
    out_ports = [port for port in connected_ports if port.port_type == PortType.OUT]
    if len(in_ports) != len(out_ports):
        raise ValueError("The number of in ports and out ports are not equal")
    sorted_port_list = []
    for in_port, out_port in zip(in_ports, out_ports):
        sorted_port_list.append(in_port)
        sorted_port_list.append(out_port)
    if len(sorted_port_list) == 4:
        sorted_port_list = order_prim_sec_ports(sorted_port_list)
    return [port.port_id for port in sorted_port_list]


def order_prim_sec_ports(connected_ports: list[Port]) -> list[Port]:
    """Order the primary and secondary ports. in correct order.

    The correct order is first primary port, then secondary port.
    This can only be done by checking the port names.
    In primary port prim is in the name for secondary port sec is in the name.

    :param connected_ports: List of connected ports to be sorted.
    :return: List of connected ports sorted by primary and secondary ports.
    """
    primary_ports = [port for port in connected_ports if "Prim" in port.port_name]
    if len(primary_ports) != 2:
        raise ValueError("The number of ports with prim in the name is not equal to 2")
    secondary_ports = [port for port in connected_ports if "Sec" in port.port_name]
    if len(secondary_ports) != 2:
        raise ValueError("The number of ports with sec in the name is not equal to 2")
    return primary_ports + secondary_ports


def reverse_dict(original_dict: dict) -> dict[str, list[type]]:
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
