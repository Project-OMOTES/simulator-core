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

"""Pump classes."""
import uuid
from typing import Dict

from pandapipes import create_circ_pump_const_mass_flow, pandapipesNet
from pandas import DataFrame

from simulator_core.entities.assets.asset_abstract import AssetAbstract

# TODO: Do we need to define a "general" pump class?


class CirculationPumpConstantMass(AssetAbstract):
    """Wrapper class for pandapipes circulation pumps with constant mass flow."""

    def __init__(
        self,
        pandapipes_net: pandapipesNet,
        p_to_junction: float,
        mdot_kg_per_s: float,
        t_to_junction: float,
        in_service: bool = True,
        name: str = None,
        index: int = None
    ):
        """Initialize a CirculationPumpConstantMass object."""
        super().__init__(asset_name=name, asset_id=str(uuid.uuid4()), panda_pipe_net=pandapipes_net)
        self.p_to_junction = p_to_junction
        self.mdot_kg_per_s = mdot_kg_per_s
        self.t_to_junction = t_to_junction
        self.in_service = in_service
        self.name = name
        self.index = index
        # Initialize the pump
        self._initialized = False

    def create(self) -> None:
        """Register the control valve in the pandapipes network."""
        if not self._initialized:
            self._initialized = True
            # Register the pump in the pandapipes network
            self.index = create_circ_pump_const_mass_flow(
                net=self.pandapipes_net,
                return_junction=self.from_junction.index,
                flow_junction=self.to_junction.index,
                p_flow_bar=self.p_to_junction,
                mdot_flow_kg_per_s=self.mdot_kg_per_s,
                t_flow_k=self.t_to_junction,
                in_service=self.in_service,
                name=self.name,
                index=self.index,
            )

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
        return {}

    def simulation_performed(self) -> bool:
        """Placeholder to indicate that a simulation has been performed.

        :return bool: True if a simulation has been performed, False otherwise.
        """
        return True

    def add_physical_data(self, data: Dict[str, float]):
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
