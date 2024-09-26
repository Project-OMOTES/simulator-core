#  Copyright (c) 2024. Deltares & TNO
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
"""Module containing the classes for the controller."""

from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
    AssetControllerAbstract,
)


class ControllerProducer(AssetControllerAbstract):
    """Class to store the source for the controller."""

    def __init__(
        self,
        name: str,
        identifier: str,
        temperature_supply: float,
        temperature_return: float,
        power: float,
        priority: int = 1,
    ):
        """Constructor for the source.

        :param str name: Name of the source.
        :param str identifier: Unique identifier of the source.
        :param float temperature_supply: Supply temperature of the source.
        :param float temperature_return: Return temperature of the source.
        :param float power: Power of the source.
        :param int priority: Priority of the source.
        """
        super().__init__(name, identifier)
        self.temperature_return: float = temperature_return
        self.temperature_supply: float = temperature_supply
        self.power: float = power
        self.priority: int = priority
