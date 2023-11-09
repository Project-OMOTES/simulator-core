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

""" Esdl asset wrapper class."""

from esdl import esdl


class EsdlObject:
    """
    EsdlObject class is a wrapper around PyEsdl
    """
    es: esdl.EnergySystem

    def __init__(self, esdl_energysystem: esdl.EnergySystem) -> None:
        """
        constructor for EsdlObject
        :param esdl_energysystem: PyEsdl EnergySystem object
        """
        self.es = esdl_energysystem

    def __repr__(self) -> str:
        return str(self.es)
