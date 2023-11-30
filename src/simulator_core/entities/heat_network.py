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

"""HeatNetwork entity class."""

from simulator_core.entities.assets.asset_abstract import AssetAbstract


class HeatNetwork:
    """Heat network class to be used to store the data of a heat network."""

    def __init__(self, asset_list: list[AssetAbstract], junction_list: list[AssetAbstract]):
        """Constructor of heatnework class to initialize the object.

        :param list[AssetAbstract] asset_list: List of assets which are in the network
        :param list[AssetAbstract] junction_list: List of junctions which are in the network.
        """
        self.assets = asset_list
        self.junctions = junction_list
