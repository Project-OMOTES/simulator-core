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

"""Abstract class for asset."""

from abc import ABC, abstractmethod
from typing import Dict, List

from pandas import DataFrame

from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from simulator_core.entities.assets.junction import Junction
from simulator_core.solver.network.assets.base_asset import BaseAsset


class AssetAbstract(ABC):
    """Abstract class for Asset."""

    from_junction: Junction | None
    """The junction where the asset starts."""

    to_junction: Junction | None
    """The junction where the asset ends."""

    name: str
    """The name of the asset."""

    asset_id: str
    """The unique identifier of the asset."""

    output: List[Dict[str, float]]
    """The output of the asset as a list with a dictionary per timestep."""
    solver_asset: BaseAsset

    def __init__(self, asset_name: str, asset_id: str):
        """Basic constructor for asset objects.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param PandapipesNet pandapipe_net: Pnadapipes network object to register asset to.
        """
        self.from_junction = None
        self.to_junction: Junction = None
        self.name: str = asset_name
        self.asset_id: str = asset_id
        self.output: List[Dict[str, float]] = []

    @abstractmethod
    def set_setpoints(self, setpoints: Dict) -> None:
        """Placeholder to set the setpoints of an asset prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the asset.
            The keys of the dictionary are the names of the setpoints and the values are the values
        """

    def get_setpoints(self) -> Dict[str, float]:
        """Placeholder to get the setpoint attributes of an asset.

        :return Dict: The setpoints of the asset. The keys of the dictionary are the names of the
            setpoints and the values are the values.
        """
        return {}

    @abstractmethod
    def add_physical_data(self, esdl_asset: EsdlAssetObject) -> None:
        """Placeholder method to add physical data to an asset."""

    def set_from_junction(self, from_junction: Junction) -> None:
        """Method to set the from junction of an asset.

        :param Junction from_junction: The junction where the asset starts.
        """
        self.from_junction = from_junction

    def set_to_junction(self, to_junction: Junction) -> None:
        """Method to set the to junction of an asset.

        :param Junction to_junction: The junction where the asset ends.
        """
        self.to_junction = to_junction

    @abstractmethod
    def write_to_output(self) -> None:
        """Placeholder to get data from pandapipes and store it in the asset."""

    def get_output(self) -> List[Dict[str, float]]:
        """Returns all the output of the asset.

        :return: A dict of property name and list of values.
        """
        return self.output

    def get_timeseries(self) -> DataFrame:
        """Get timeseries as a dataframe from a pandapipes asset.

        The header is a tuple of the asset id and the property name.
        """
        # Create dataframe
        temp_dataframe = DataFrame(self.output)
        # Set header
        temp_dataframe.columns = [
            (self.asset_id, column_name) for column_name in temp_dataframe.columns
        ]
        return temp_dataframe
