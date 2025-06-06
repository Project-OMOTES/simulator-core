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

"""Module containing utility functions."""

from pathlib import Path

from esdl.esdl_handler import EnergySystemHandler


def pyesdl_from_file(file_path: str | Path) -> EnergySystemHandler:
    """
    Loads esdl file into memory and returns a handle to be able to use this file.

    Please note that it is not checked if the file is a valid esdl file.
    :param str | Path file_path: Location of the ESDL file to be loaded into memory.
    If file_path is a string, convert it to a Path object, then check if its not a path.
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError("Not a valid path to an ESDL file")
    esh = EnergySystemHandler()
    esh.load_file(str(file_path))
    return esh


def pyesdl_from_string(input_str: str) -> EnergySystemHandler:
    """
    Loads esdl file from a string into memory.

    Please note that it is not checked if the contents of the string is a valid esdl.
    :param input_str: string containing the contents of an esdl file.
    """
    esh = EnergySystemHandler()
    esh.load_from_string(input_str)
    return esh
