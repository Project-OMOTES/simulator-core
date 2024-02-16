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

"""demandCluster class."""
import uuid
from typing import Dict


from simulator_core.entities.assets.asset_abstract import AssetAbstract
from simulator_core.entities.assets.asset_defaults import (
    DEFAULT_DIAMETER,
    DEFAULT_TEMPERATURE,
    DEFAULT_TEMPERATURE_DIFFERENCE,
    DEFAULT_PRESSURE,
    DEFAULT_POWER,
    PROPERTY_MASSFLOW,
    PROPERTY_VOLUMEFLOW,
    PROPERTY_TEMPERATURE_SUPPLY,
    PROPERTY_TEMPERATURE_RETURN,
    PROPERTY_PRESSURE_SUPPLY,
    PROPERTY_PRESSURE_RETURN,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_THERMAL_POWER,
)
from simulator_core.entities.assets.junction import Junction
from simulator_core.entities.assets.heatexchanger import HeatExchanger
from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from simulator_core.entities.assets.valve import ControlValve
from simulator_core.entities.assets.utils import (
    heat_demand_and_temperature_to_mass_flow,
    mass_flow_and_temperature_to_heat_demand,
    mass_flow_to_volume_flow,
)


class DemandCluster(AssetAbstract):
    """A DemandCluster represents an asset that consumes heat."""

    def __init__(
            self,
            asset_name: str,
            asset_id: str,
    ):
        """Initialize a DemandCluster object.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param PandapipesNet pandapipe_net: Pandapipes network object to register asset to.
        """
        super().__init__(asset_name=asset_name, asset_id=asset_id)

        self._internal_diameter = DEFAULT_DIAMETER
        self.temperature_supply = DEFAULT_TEMPERATURE
        self.temperature_return: float = DEFAULT_TEMPERATURE - DEFAULT_TEMPERATURE_DIFFERENCE
        self.temperature_return_target = self.temperature_return
        self.pressure_input = DEFAULT_PRESSURE
        self.thermal_power_allocation = DEFAULT_POWER
        self.mass_flowrate = 0
        self.solver_asset = ProductionAsset(uuid.uuid4())
        # Output list
        self.output: list = []

    def set_setpoints(self, setpoints: Dict) -> None:
        """Placeholder to set the setpoints of an asset prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the asset.
            The keys of the dictionary are the names of the setpoints and the values are the values
        """
        self.thermal_power_allocation = setpoints[PROPERTY_HEAT_DEMAND]
        self.temperature_return_target = setpoints[PROPERTY_TEMPERATURE_RETURN]
        self.temperature_supply = setpoints[PROPERTY_TEMPERATURE_SUPPLY]
        adjusted_mass_flowrate = heat_demand_and_temperature_to_mass_flow(
            self.thermal_power_allocation,
            self.temperature_supply,
            self.temperature_return_target)
        self.solver_asset.supply_temperature = self.temperature_return_target
        self.solver_asset.mass_flow_rate_set_point = adjusted_mass_flowrate


    def simulation_performed(self) -> bool:
        """Check if the simulation has been performed.

        :return bool simulation_performed: True if the simulation has been performed,
            False otherwise.
        """
        return hasattr(self.pandapipes_net, 'res_flow_control')

    def add_physical_data(self, esdl_asset: EsdlAssetObject) -> None:
        """Method to add physical data to the asset.

        :param EsdlAssetObject esdl_asset: The esdl asset object to add the physical data from.
         :return:
        """
        pass

    def write_to_output(self) -> None:
        """Placeholder to write the asset to the output.

        The output list is a list of dictionaries, where each dictionary
        represents the output of its asset for a specific timestep.
        """
        outputs = dict()
        outputs[PROPERTY_MASSFLOW] = self.solver_asset.get_mass_flow_rate(0)

        self.output.append(outputs)
