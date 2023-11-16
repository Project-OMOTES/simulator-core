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
from typing import Dict, TypeVar
from pandapipes import pandapipesNet
from pandas import DataFrame


Junction_type = TypeVar("Junction")


class AssetAbstract(ABC):
    """Abstract class for Asset."""

    from_junction: Junction_type | None
    to_junction: Junction_type | None
    pandapipes_net: pandapipesNet | None

    def __init__(self, asset_name: str, asset_id: str):
        """Basic constructor for asset objects.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        """
        self.from_junction = None
        self.to_junction = None
        # Define the pandapipes network
        self.pandapipes_net = None
        self.name = asset_name
        self.id = asset_id

    @abstractmethod
    def set_setpoints(self, setpoints: Dict, **kwargs) -> None:
        """Placeholder to set the setpoints of an asset prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the asset.
            The keys of the dictionary are the names of the setpoints and the values are the values
        """
        pass

    @abstractmethod
    def get_setpoints(self, **kwargs) -> Dict:
        """Placeholder to get the setpoint attributes of an asset.

        :return Dict: The setpoints of the asset. The keys of the dictionary are the names of the
            setpoints and the values are the values.
        """
        pass

    @abstractmethod
    def simulation_performed(self) -> bool:
        """Placeholder to indicate that a simulation has been performed.

        :return bool: True if a simulation has been performed, False otherwise.
        """
        pass

    @abstractmethod
    def _create(self) -> None:
        """Placeholder to create an asset in a pandapipes network."""
        pass

    @abstractmethod
    def add_physical_data(self, data: Dict[str, float]):
        """Placeholder method to add physical data to an asset."""
        pass

    def connect_junctions(self, from_junction, to_junction):
        """Method to connect junctions to a asset.

        :param Junction from_junction: The junction where the asset starts.
        :param Junction to_junction: The junction where the asset end.
        :return:
        """
        self.from_junction = from_junction
        self.to_junction = to_junction

    @abstractmethod
    def write_to_output(self) -> None:
        """Placeholder to write the asset to the output.

        The output list is a list of dictionaries, where each dictionary
        represents the output of its asset for a specific timestep.
        """
        pass

    @abstractmethod
    def get_timeseries(self) -> DataFrame:
        """Get timeseries as a dataframe from a pandapipes asset.

        The header is a tuple of the asset id and the property name.
        """
        pass
