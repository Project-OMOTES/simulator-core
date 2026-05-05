#  Copyright (c) 2026. Deltares & TNO
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
"""Module containing classes for profile data sampling and interpolation."""

from dataclasses import dataclass


@dataclass
class Temperatures:
    """Class to store the temperatures used in the simulation."""

    in_flow: float
    out_flow: float


def celcius_to_kelvin(temperature: float) -> float:
    """Convert Celcius to Kelvin.

    :param temperature: temperature in C
    :return: temperature in K
    """
    return temperature + 273.15


def kelvin_to_celcius(temperature: float) -> float:
    """Convert Kelvin to Celcius.

    :param temperature: temperature in K
    :return: temperature in C
    """
    return temperature - 273.15
