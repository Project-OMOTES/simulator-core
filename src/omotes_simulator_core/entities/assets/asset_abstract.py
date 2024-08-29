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

from pandas import DataFrame, concat

from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.entities.assets.junction import Junction
from omotes_simulator_core.solver.network.assets.base_asset import BaseAsset

from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_MASSFLOW,
    PROPERTY_PRESSURE,
    PROPERTY_TEMPERATURE,
)


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

    outputs: List[List[Dict[str, float]]]
    """The output of the asset as a list with a dictionary per timestep."""

    connected_ports: List[str]
    """List of ids of the connected ports."""
    solver_asset: BaseAsset
    asset_type = "asset_abstract"

    def __init__(self, asset_name: str, asset_id: str, connected_ports: List[str]) -> None:
        """Basic constructor for asset objects.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param List[str] connected_ports: List of ids of the connected ports.
        """
        self.from_junction = None
        self.to_junction = None
        self.name = asset_name
        self.asset_id = asset_id
        self.connected_ports = connected_ports
        self.outputs = [[] for _ in range(len(self.connected_ports))]

    def __repr__(self) -> str:
        """Method to print string with the name of the asset."""
        return self.__class__.__name__ + " " + self.name

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

    def write_standard_output(self) -> None:
        """Write the output of the asset to the output list.

        The output list is a list of dictionaries, where each dictionary
        represents the output of its asset for a specific timestep.
        The output of the asset is a list with a dictionary for each port
        of the asset. Teh basic properties mass flow rate, pressure and temperature are stored.
        All assets can add their own properties to the dictionary.
        """
        for i in range(len(self.connected_ports)):
            output_dict_temp = {
                PROPERTY_MASSFLOW: self.solver_asset.get_mass_flow_rate(i),
                PROPERTY_PRESSURE: self.solver_asset.get_pressure(i),
                PROPERTY_TEMPERATURE: self.solver_asset.get_temperature(i),
            }
            self.outputs[i].append(output_dict_temp)

    @abstractmethod
    def write_to_output(self) -> None:
        """Placeholder to get data and store it in the asset."""

    def get_timeseries(self) -> DataFrame:
        """Get timeseries as a dataframe from a asset.

        The header is a tuple of the port id and the property name.
        """
        # Create dataframe

        temp_data = DataFrame()
        for i in range(len(self.connected_ports)):
            temp_frame = DataFrame(self.outputs[i])
            temp_frame.columns = [
                (self.connected_ports[i], column_name) for column_name in temp_frame.columns
            ]
            temp_data = concat([temp_data, temp_frame], axis=1)
        return temp_data
