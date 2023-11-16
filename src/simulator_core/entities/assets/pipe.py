"""Module containing pipe class."""
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


from typing import Dict
from pandas import DataFrame
from simulator_core.entities.assets.asset_abstract import AssetAbstract


class Pipe(AssetAbstract):
    """A class representing a pipe in a heat network."""

    def __init__(
            self,
            asset_name: str,
            asset_id: str,
    ):
        """Initialize a Pipe object.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        """
        super().__init__(asset_name, asset_id)

    def add_physical_data(self, data: Dict[str, float]):
        """Method to add physical data to the asset.

        :param dict data:dictionary containing the data to be added the asset. The key is the name
                        of the property, the value of the dict is the value of the property.
        :return:
        """
        pass

    def set_setpoints(self, setpoints: Dict, **kwargs) -> None:
        """Placeholder to set the setpoints of an asset prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the asset.
            The keys of the dictionary are the names of the setpoints and the values are the values
        """
        pass

    def get_setpoints(self, **kwargs) -> Dict:
        """Placeholder to get the setpoint attributes of an asset.

        :return Dict: The setpoints of the asset. The keys of the dictionary are the names of the
            setpoints and the values are the values.
        """
        pass

    def simulation_performed(self) -> bool:
        """Placeholder to indicate that a simulation has been performed.

        :return bool: True if a simulation has been performed, False otherwise.
        """
        pass

    def _create(self) -> None:
        """Placeholder to create an asset in a pandapipes network."""
        pass

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
        pass
