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
from typing import Dict, List, TypeVar

from pandapipes import pandapipesNet
from pandas import DataFrame

Junction = TypeVar("Junction")
EsdlAssetObject = TypeVar("EsdlAssetObject")


class AssetAbstract(ABC):
    """Abstract class for Asset."""

    from_junction: Junction | None
    """The junction where the asset starts."""

    to_junction: Junction | None
    """The junction where the asset ends."""

    pandapipes_net: pandapipesNet
    """The pandapipes network to which the asset belongs."""

    name: str
    """The name of the asset."""

    asset_id: str
    """The unique identifier of the asset."""

    output: List[Dict[str, float]]
    """The output of the asset as a list with a dictionary per timestep."""

    def __init__(self, asset_name: str, asset_id: str, pandapipe_net: pandapipesNet):
        """Basic constructor for asset objects.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param PandapipesNet pandapipe_net: Pnadapipes network object to register asset to.
        """
        self.from_junction = None
        self.to_junction: Junction = None
        # Define the pandapipes network
        self.pandapipes_net = pandapipe_net
        self.name = asset_name
        self.asset_id = asset_id

    def set_setpoints(self, setpoints: Dict) -> None:  # noqa: B027
        """Placeholder to set the setpoints of an asset prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the asset.
            The keys of the dictionary are the names of the setpoints and the values are the values
        """
        pass

    def get_setpoints(self) -> Dict:
        """Placeholder to get the setpoint attributes of an asset.

        :return Dict: The setpoints of the asset. The keys of the dictionary are the names of the
            setpoints and the values are the values.
        """
        return {}

    @abstractmethod
    def simulation_performed(self) -> bool:
        """Placeholder to indicate that a simulation has been performed.

        :return bool: True if a simulation has been performed, False otherwise.
        """
        pass

    @abstractmethod
    def create(self) -> None:
        """Placeholder to create an asset in a pandapipes network."""
        pass

    @abstractmethod
    def add_physical_data(self, esdl_asset: EsdlAssetObject) -> None:
        """Placeholder method to add physical data to an asset."""
        pass

    def set_from_juction(self, from_junction: Junction) -> None:
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
        """Placeholder to write the asset to the output.

        The output list is a list of dictionaries, where each dictionary
        represents the output of its asset for a specific timestep.
        """
        pass

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
