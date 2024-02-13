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

"""Valve classes."""
from typing import Dict

from pandapipes import create_flow_control, pandapipesNet
from pandas import DataFrame

from simulator_core.entities.assets.asset_abstract import AssetAbstract
from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from simulator_core.entities.assets.asset_defaults import DEFAULT_DIAMETER


class ControlValve(AssetAbstract):
    """Wrapper class for pandapipes control valves."""

    def __init__(
        self, asset_name: str, asset_id: str, pandapipe_net: pandapipesNet,
            diameter: float = DEFAULT_DIAMETER
    ):
        """Initialize a ControlValve object."""
        super().__init__(asset_name=asset_name, asset_id=asset_id,
                         pandapipe_net=pandapipe_net)
        self.controlled_mdot_kg_per_s = 10.0
        self.diameter_m = diameter
        self.control_active = True
        self.in_service = True
        self.index = 0
        # Initialize the control valve
        self._initialized = False

    def create(self) -> None:
        """Register the control valve in the pandapipes network."""
        if not self._initialized:
            self.index = create_flow_control(
                net=self.pandapipes_net,
                from_junction=self.from_junction.index,
                to_junction=self.to_junction.index,
                controlled_mdot_kg_per_s=self.controlled_mdot_kg_per_s,
                diameter_m=self.diameter_m,
                control_active=self.control_active,
                in_service=self.in_service,
                name=self.name,
            )
            self._initialized = True

    def set_setpoints(self, setpoints: Dict, **kwargs: Dict) -> None:
        """Placeholder to set the setpoints of an asset prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the asset.
            The keys of the dictionary are the names of the setpoints and the values are the values
        """
        pass

    def get_setpoints(self, **kwargs: Dict) -> Dict:
        """Placeholder to get the setpoint attributes of an asset.

        :return Dict: The setpoints of the asset. The keys of the dictionary are the names of the
            setpoints and the values are the values.
        """
        return {}

    def simulation_performed(self) -> bool:
        """Placeholder to indicate that a simulation has been performed.

        :return bool: True if a simulation has been performed, False otherwise.
        """
        return True

    def add_physical_data(self, esdl_asset: EsdlAssetObject) -> None:
        """Placeholder method to add physical data to an asset."""
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
