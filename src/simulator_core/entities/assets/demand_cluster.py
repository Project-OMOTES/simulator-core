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

from pandapipes import pandapipesNet

from simulator_core.entities.assets.asset_abstract import AssetAbstract
from simulator_core.entities.assets.asset_defaults import (
    DEFAULT_DIAMETER,
    DEFAULT_NODE_HEIGHT,
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
            pandapipe_net: pandapipesNet
    ):
        """Initialize a DemandCluster object.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param PandapipesNet pandapipe_net: Pandapipes network object to register asset to.
        """
        super().__init__(asset_name=asset_name, asset_id=asset_id, pandapipe_net=pandapipe_net)

        self._internal_diameter = DEFAULT_DIAMETER
        self.temperature_supply = DEFAULT_TEMPERATURE
        self.temperature_return: float = DEFAULT_TEMPERATURE - DEFAULT_TEMPERATURE_DIFFERENCE
        self.temperature_return_target = self.temperature_return
        self.pressure_input = DEFAULT_PRESSURE
        self.thermal_power_allocation = DEFAULT_POWER
        self.mass_flowrate = 0

        # Objects of the asset
        self._initialized = False
        self._intermediate_junction: Junction | None = None
        self._flow_control: None | ControlValve = None
        self._heat_exchanger: None | HeatExchanger = None
        # Output list
        self.output: list = []

    def create(self) -> None:
        """Create a representation of the asset in pandapipes.

        The DemandCluster asset contains multiple pandapipes components.

        The component model contains the following components:
        - A flow control valve to set the mass flow rate of the system.
        - A heat exchanger to set the power consumption of the demand
        - An intermediate junction to link both components.
        :param pandapipesNet pandapipes_net: pandapipes network object
        """
        if not self._initialized:
            # Create intermediate junction
            self._intermediate_junction = Junction(
                pandapipes_net=self.pandapipes_net,
                pn_bar=self.pressure_input,
                tfluid_k=self.temperature_supply,
                height_m=DEFAULT_NODE_HEIGHT,
                name=f"intermediate_junction_{self.name}",
            )
            # Create the control valve
            self._flow_control = ControlValve(
                pandapipe_net=self.pandapipes_net,
                asset_name=f"flow_control_{self.name}",
                asset_id=str(uuid.uuid4())
            )
            self._flow_control.from_junction = self.from_junction
            self._flow_control.to_junction = self._intermediate_junction
            self._flow_control.create()

            # Create the heat exchanger
            self._heat_exchanger = HeatExchanger(
                pandapipes_net=self.pandapipes_net,
                diameter_m=self._internal_diameter,
                heat_flux_w=self.thermal_power_allocation,
                name=f"heat_exchanger_{self.name}",
                in_service=True,
            )
            self._heat_exchanger.from_junction = self._intermediate_junction
            self._heat_exchanger.to_junction = self.to_junction
            self._heat_exchanger.create()

            self._initialized = True

    def set_setpoints(self, setpoints: Dict) -> None:
        """Placeholder to set the setpoints of an asset prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the asset.
            The keys of the dictionary are the names of the setpoints and the values are the values
        """
        self.thermal_power_allocation = setpoints[PROPERTY_HEAT_DEMAND]
        self.temperature_return_target = setpoints[PROPERTY_TEMPERATURE_RETURN]
        self.temperature_supply = setpoints[PROPERTY_TEMPERATURE_SUPPLY]
        self._set_demand_control()

    def _set_demand_control(self) -> None:
        """Function to control the DemandCluster to achieve target return temperature."""
        # adjust flowrate or power to meet the return temperature
        if self.pandapipes_net.flow_control.control_active[self._flow_control.index]:
            # if pump is active, set flowrate to meet Target Temperature
            self._heat_exchanger.qext_w = self.thermal_power_allocation
            self.pandapipes_net.heat_exchanger.qext_w[
                self._heat_exchanger.index] = self.thermal_power_allocation

            adjusted_mass_flowrate = heat_demand_and_temperature_to_mass_flow(
                self.thermal_power_allocation,
                self.temperature_supply,
                self.temperature_return_target,
                self.pandapipes_net)

            self._flow_control.controlled_mdot_kg_per_s = adjusted_mass_flowrate
            self.pandapipes_net.flow_control.controlled_mdot_kg_per_s[
                self._flow_control.index] = adjusted_mass_flowrate

        else:
            # if pump is disabled, set thermal power to meet Target Temperature
            adjusted_thermal_power_demand = mass_flow_and_temperature_to_heat_demand(
                self.temperature_supply,
                self.temperature_return_target,
                self.mass_flowrate,
                self.pandapipes_net)

            self._heat_exchanger.qext_w = adjusted_thermal_power_demand
            self.pandapipes_net.heat_exchanger.qext_w[
                self._heat_exchanger.index] = adjusted_thermal_power_demand

    def get_setpoints(self) -> Dict[str, float]:
        """Placeholder to get the setpoint attributes of an asset.

        :return Dict: The setpoints of the asset. The keys of the dictionary are the names of the
            setpoints and the values are the values.
        """
        setpoints: Dict[str, float] = {PROPERTY_HEAT_DEMAND: self.thermal_power_allocation,
                                       PROPERTY_TEMPERATURE_RETURN: self.temperature_return}

        return setpoints

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
        if not self._initialized:
            raise ValueError("Asset not initialized.")
        if not self.simulation_performed():
            raise ValueError("Simulation data not available.")
        outputs = dict()

        outputs[PROPERTY_TEMPERATURE_SUPPLY] = self.pandapipes_net.res_flow_control['t_from_k'][
            self._flow_control.index]
        outputs[PROPERTY_TEMPERATURE_RETURN] = self.pandapipes_net.res_heat_exchanger['t_to_k'][
            self._heat_exchanger.index]
        outputs[PROPERTY_PRESSURE_SUPPLY] = self.pandapipes_net.res_flow_control['p_from_bar'][
            self._flow_control.index]
        outputs[PROPERTY_PRESSURE_RETURN] = self.pandapipes_net.res_heat_exchanger['p_to_bar'][
            self._heat_exchanger.index]
        outputs[PROPERTY_MASSFLOW] = \
            self.pandapipes_net.res_heat_exchanger['mdot_from_kg_per_s'][
                self._heat_exchanger.index]
        outputs[PROPERTY_VOLUMEFLOW] = mass_flow_to_volume_flow(
            outputs[PROPERTY_MASSFLOW],
            outputs[PROPERTY_TEMPERATURE_SUPPLY],
            self.pandapipes_net)
        outputs[PROPERTY_THERMAL_POWER] = mass_flow_and_temperature_to_heat_demand(
            outputs[PROPERTY_TEMPERATURE_SUPPLY],
            outputs[PROPERTY_TEMPERATURE_RETURN],
            outputs[PROPERTY_MASSFLOW],
            self.pandapipes_net)

        self.output.append(outputs)
