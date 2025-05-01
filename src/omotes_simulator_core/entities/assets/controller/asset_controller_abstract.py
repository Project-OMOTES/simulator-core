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


class AssetControllerAbstract:
    """Abstract class for the asset controller."""

    def __init__(self, name: str, identifier: str):
        """Constructor for the asset controller.

        :param str name: Name of the controller object.
        :param str identifier: Unique identifier of the controller asset.
        """
        self.name = name
        self.id = identifier

    def set_state(self, state: dict[str, float]) -> None:
        """Placeholder to set the state of the controller.

        :param dict[str, float] state: State of the controller from the asset_abstract
            get_state method.
        """
        return None
