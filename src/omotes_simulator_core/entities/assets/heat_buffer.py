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

"""Heat Buffer class."""
from cmath import isinf
from typing import Dict

import numpy as np

from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.asset_defaults import (
    DEFAULT_TEMPERATURE,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_MASSFLOW,
    PROPERTY_PRESSURE_RETURN,
    PROPERTY_PRESSURE_SUPPLY,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
)
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.entities.assets.utils import (
    heat_demand_and_temperature_to_mass_flow,
)
from omotes_simulator_core.solver.network.assets.production_asset import HeatBoundary
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


class HeatBuffer(AssetAbstract):
    """A HeatBuffer represents an asset that stores heat. Thus, it has the possibility to supply \
    heat or consume heat for storage."""

    temperature_supply: float
    """The supply temperature of the asset [K]."""

    temperature_return: float
    """The return temperature of the asset [K]."""

    thermal_power_allocation: float
    """The thermal for injection (positive) or production (negative) by the asset [W]."""

    mass_flowrate: float
    """The flow rate going in or out by the asset [kg/s]."""

    volume: float
    """The volume of the heat storage [m3]."""

    accumulation_time: float
    """The accumulation_time to calculate volume during injection and production [seconds]."""

    def __init__(
        self,
        asset_name: str,
        asset_id: str,
        port_ids: list[str],
        volume: float,
    ) -> None:
        """Initialize a HeatBuffer object.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        """
        super().__init__(asset_name=asset_name, asset_id=asset_id, connected_ports=port_ids)

        # Supply and return temperature of the asset [K]
        self.temperature_in = DEFAULT_TEMPERATURE
        self.temperature_out = DEFAULT_TEMPERATURE

        # Volume properties of the asset: volume [m3], fill level [fraction 0-1]
        self.tank_volume = volume
        self.num_layer = 5
        self.layer_volume = self.tank_volume / self.num_layer
        self.layer_mass = self.layer_volume * fluid_props.get_density(
            (self.temperature_in + self.temperature_out) / 2
        )
        self.layer_temperature = np.linspace(
            self.temperature_in, self.temperature_out, self.num_layer
        )

        # Thermal power allocation [W] for injection (positive) or production (negative) by the
        # asset and mass flowrate [kg/s] going in or out by the asset
        self.thermal_power_allocation = 0
        self.mass_flowrate = 0

        # HeatBoundary since heat buffer acts either as producer or consumer,
        # positive flow is discharge and negative flow is charge
        self.solver_asset = HeatBoundary(name=self.name, _id=self.asset_id)

        self.accumulation_time = 3600
        self.output: list = []
        self.first_time_step = True

    def set_setpoints(self, setpoints: Dict) -> None:
        """Placeholder to set the setpoints of an asset prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the asset.
        The keys of the dictionary are the names of the setpoints and the values are the values
        """
        # Default keys required
        necessary_setpoints = {
            PROPERTY_TEMPERATURE_IN,
            PROPERTY_TEMPERATURE_OUT,
            PROPERTY_HEAT_DEMAND,
        }
        # Dict to set
        setpoints_set = set(setpoints.keys())
        # Check if all setpoints are in the setpoints
        if necessary_setpoints.issubset(setpoints_set):
            # negative is charging and positive is discharging
            self.thermal_power_allocation = -setpoints[PROPERTY_HEAT_DEMAND]

            if self.first_time_step:
                self.temperature_in = setpoints[PROPERTY_TEMPERATURE_IN]
                self.temperature_out = setpoints[PROPERTY_TEMPERATURE_OUT]
                self.first_time_step = False
            else:
                # After the first time step: use solver temperature
                if self.thermal_power_allocation < 0:
                    self.temperature_in = self.solver_asset.get_temperature(0)
                else:
                    self.temperature_out = self.solver_asset.get_temperature(1)

            if self.thermal_power_allocation < 0:
                # when charging the output temperature is the bottom temperature of the tank
                self.temperature_out = self.layer_temperature[-1]
            else:
                # when discharging the input temperature is the upper temperature of the tank
                self.temperature_in = self.layer_temperature[0]

            self._calculate_massflowrate()
            self._calculate_new_temperature()
            self._set_solver_asset_setpoint()
        else:
            # Print missing setpoints
            raise ValueError(
                f"The setpoints {necessary_setpoints.difference(setpoints_set)} are missing."
            )

    def _calculate_massflowrate(self) -> None:
        """Calculate mass flowrate of the asset."""
        self.mass_flowrate = heat_demand_and_temperature_to_mass_flow(
            self.thermal_power_allocation, self.temperature_in, self.temperature_out
        )
        if isinf(self.mass_flowrate):
            self.mass_flowrate = 0

    def _calculate_new_temperature(self) -> None:
        """Calculate new temperature of the tank storage."""
        # heat exchange top side
        new_temperature = self.layer_temperature.copy()

        if self.mass_flowrate > 0:
            new_temperature[0] += min(
                1, self.mass_flowrate * self.accumulation_time / self.layer_mass
            ) * (self.temperature_in - self.layer_temperature[0])

            # heat exchange between layer
            for ii in range(self.num_layer - 1):
                new_temperature[ii + 1] += min(
                    1, self.mass_flowrate * self.accumulation_time / self.layer_mass
                ) * (new_temperature[ii] - new_temperature[ii + 1])

            self.layer_temperature = new_temperature

            self.temperature_out = self.layer_temperature[-1]
        else:
            new_temperature[-1] += min(
                1, abs(self.mass_flowrate) * self.accumulation_time / self.layer_mass
            ) * (self.temperature_out - self.layer_temperature[-1])

            # heat exchange between layer
            for ii in range(self.num_layer - 1, 0, -1):
                new_temperature[ii - 1] += min(
                    1, abs(self.mass_flowrate) * self.accumulation_time / self.layer_mass
                ) * (new_temperature[ii] - new_temperature[ii - 1])

            self.layer_temperature = new_temperature

            self.temperature_in = self.layer_temperature[0]

    def _set_solver_asset_setpoint(self) -> None:
        """Set the setpoint of solver asset."""
        if self.mass_flowrate > 0:
            self.solver_asset.supply_temperature = self.temperature_out
        else:
            self.solver_asset.supply_temperature = self.temperature_in
        self.solver_asset.mass_flow_rate_set_point = self.mass_flowrate  # type: ignore

    def add_physical_data(self, esdl_asset: EsdlAssetObject) -> None:
        """Method to add physical data to the asset.

        :param EsdlAssetObject esdl_asset: The esdl asset object to add the physical data from.
         :return:
        """

    def write_to_output(self) -> None:
        """Placeholder to write the asset to the output.

        The output list is a list of dictionaries, where each dictionary
        represents the output of its asset for a specific timestep.
        """
        output_dict = {
            PROPERTY_MASSFLOW: self.solver_asset.get_mass_flow_rate(1),
            PROPERTY_PRESSURE_SUPPLY: self.solver_asset.get_pressure(0),
            PROPERTY_PRESSURE_RETURN: self.solver_asset.get_pressure(1),
            PROPERTY_TEMPERATURE_IN: self.solver_asset.get_temperature(0),
            PROPERTY_TEMPERATURE_OUT: self.solver_asset.get_temperature(1),
        }
        self.output.append(output_dict)
