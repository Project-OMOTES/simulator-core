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

"""ProductionCluster class."""
from typing import Dict

from simulator_core.entities.assets.asset_abstract import AssetAbstract
from simulator_core.entities.assets.asset_defaults import (
    DEFAULT_NODE_HEIGHT,
    DEFAULT_PRESSURE,
    DEFAULT_TEMPERATURE,
    DEFAULT_TEMPERATURE_DIFFERENCE,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_MASSFLOW,
    PROPERTY_PRESSURE_RETURN,
    PROPERTY_PRESSURE_SUPPLY,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_RETURN,
    PROPERTY_TEMPERATURE_SUPPLY,
)
from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from simulator_core.entities.assets.utils import (
    heat_demand_and_temperature_to_mass_flow,
)
from simulator_core.solver.network.assets.production_asset import ProductionAsset


class ProductionCluster(AssetAbstract):
    """A ProductionCluster represents an asset that produces heat."""

    thermal_production_required: float | None
    """The thermal production required by the asset [W]."""

    temperature_supply: float
    """The supply temperature of the asset [K]."""

    temperature_return: float
    """The return temperature of the asset [K]."""

    pressure_supply: float
    """The supply pressure of the asset [Pa]."""

    control_mass_flow: bool
    """Flag to indicate whether the mass flow rate is controlled.
    If True, the mass flow rate is controlled. If False, the mass flow rate is not controlled
    and the pressure is predescribed.
    """

    controlled_mass_flow: float | None
    """The controlled mass flow of the asset [kg/s]."""

    def __init__(self, asset_name: str, asset_id: str):
        """Initialize a ProductionCluster object.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param PandapipesNet pandapipe_net: Pandapipes network object to register asset to.
        """
        super().__init__(asset_name=asset_name, asset_id=asset_id)
        self.height_m = DEFAULT_NODE_HEIGHT
        # DemandCluster thermal and mass flow specifications
        self.thermal_production_required = None
        self.temperature_supply = DEFAULT_TEMPERATURE
        self.temperature_return = DEFAULT_TEMPERATURE - DEFAULT_TEMPERATURE_DIFFERENCE
        # DemandCluster pressure specifications
        self.pressure_supply = DEFAULT_PRESSURE
        self.control_mass_flow = False
        # Controlled mass flow
        self.controlled_mass_flow = None
        self.solver_asset = ProductionAsset(
            name=self.name,
            _id=self.asset_id,
            pre_scribe_mass_flow=False,
            set_pressure=self.pressure_supply,
        )

    def add_physical_data(self, esdl_asset: EsdlAssetObject) -> None:
        """Method to add physical data to the asset.

        :param EsdlAssetObject esdl_asset: The ESDL asset object containing the physical data.
        :return:
        """

    def _set_supply_temperature(self, temperature_supply: float) -> None:
        """Set the supply temperature of the asset.

        :param float temperature_supply: The supply temperature of the asset.
            The temperature should be supplied in Kelvin.
        """
        # Set the temperature of the circulation pump mass flow
        self.temperature_supply = temperature_supply
        self.solver_asset.supply_temperature = self.temperature_supply

    def _set_return_temperature(self, temperature_return: float) -> None:
        """Set the return temperature of the asset.

        :param float temperature_return: The return temperature of the asset.
            The temperature should be supplied in Kelvin.
        """
        # Set the return temperature of the asset
        self.temperature_return = temperature_return

    def _set_heat_demand(self, heat_demand: float) -> None:
        """Set the heat demand of the asset.

        :param float heat_demand: The heat demand of the asset.
            The heat demand should be supplied in Watts.
        """
        # Calculate the mass flow rate
        self.controlled_mass_flow = heat_demand_and_temperature_to_mass_flow(
            thermal_demand=heat_demand,
            temperature_supply=self.temperature_supply,
            temperature_return=self.temperature_return,
        )

        # Check if the mass flow rate is positive
        if self.controlled_mass_flow < 0.0:
            raise ValueError(
                f"The mass flow rate {self.controlled_mass_flow} of the asset {self.name}"
                + " is negative."
            )
        else:
            # Set the mass flow rate of the control valve
            self.solver_asset.mass_flow_rate_set_point = self.controlled_mass_flow  # type: ignore

    def _set_pressure_or_mass_flow_control(self, pressure_supply: bool) -> None:
        """Set the asset to predescribe either the pressure or the mass flow rate.

        :param bool pressure_supply: True when the pressure needs to be set
        """
        if pressure_supply:
            self.solver_asset.pre_scribe_mass_flow = False  # type: ignore
        else:
            self.solver_asset.pre_scribe_mass_flow = True   # type: ignore

    def set_pressure_supply(self, pressure_supply: float) -> None:
        """Set the supply pressure of the asset.

        :param float pressure_supply: The supply pressure of the asset.
            The pressure should be supplied in Pascal.
        """
        # Check if the pressure is positive
        if pressure_supply < 0.0:
            raise ValueError(
                f"The pressure {pressure_supply} of the asset {self.name} can not be negative."
            )
        # Set the supply pressure of the asset
        self.pressure_supply = pressure_supply
        # Set the pressure of the solver asset
        self.solver_asset.set_pressure = self.pressure_supply   # type: ignore

    def set_setpoints(self, setpoints: Dict) -> None:
        """Set the setpoints of the asset.

        :param Dict setpoints: The setpoints of the asset in a dictionary,
            as "property_name": value pairs.

        """
        # Default keys required
        necessary_setpoints = {
            PROPERTY_TEMPERATURE_SUPPLY,
            PROPERTY_TEMPERATURE_RETURN,
            PROPERTY_HEAT_DEMAND,
            PROPERTY_SET_PRESSURE,
        }
        # Dict to set
        setpoints_set = set(setpoints.keys())
        # Check if all setpoints are in the setpoints
        if necessary_setpoints.issubset(setpoints_set):
            # Set the setpoints
            self._set_pressure_or_mass_flow_control(setpoints[PROPERTY_SET_PRESSURE])
            self._set_supply_temperature(setpoints[PROPERTY_TEMPERATURE_SUPPLY])
            self._set_return_temperature(setpoints[PROPERTY_TEMPERATURE_RETURN])
            self._set_heat_demand(setpoints[PROPERTY_HEAT_DEMAND])
        else:
            # Print missing setpoints
            raise ValueError(
                f"The setpoints {necessary_setpoints.difference(setpoints_set)} are missing."
            )

    def update(self) -> None:
        """Update the asset properties to the results from the previous (timestep) simulation.

        Sets the values of the supply temperature, return temperature and heat demand
        to the values of the previous simulation. In addition, the mass flow rate is set
        to the value of the previous simulation.
        """

    def write_to_output(self) -> None:
        """Write the output of the asset to the output list.

        The output list is a list of dictionaries, where each dictionary
        represents the output of its asset for a specific timestep.

        The output of the asset is a dictionary with the following keys:
        - PROPERTY_HEAT_DEMAND: The heat demand of the asset.
        - PROPERTY_TEMPERATURE_SUPPLY: The supply temperature of the asset.
        - PROPERTY_TEMPERATURE_RETURN: The return temperature of the asset.
        - PROPERTY_PRESSURE_SUPPLY: The supply pressure of the asset.
        - PROPERTY_PRESSURE_RETURN: The return pressure of the asset.
        - PROPERTY_MASSFLOW: The mass flow rate of the asset.
        """
        output_dict = {
            PROPERTY_MASSFLOW: self.solver_asset.get_mass_flow_rate(1),
            PROPERTY_PRESSURE_SUPPLY: self.solver_asset.get_pressure(0),
            PROPERTY_PRESSURE_RETURN: self.solver_asset.get_pressure(1),
            PROPERTY_TEMPERATURE_SUPPLY: self.solver_asset.get_temperature(0),
            PROPERTY_TEMPERATURE_RETURN: self.solver_asset.get_temperature(1),
        }
        self.output.append(output_dict)
