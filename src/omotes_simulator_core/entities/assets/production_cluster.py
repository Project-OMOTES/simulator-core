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
import logging

from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.asset_defaults import (
    DEFAULT_NODE_HEIGHT,
    DEFAULT_PRESSURE,
    DEFAULT_TEMPERATURE,
    DEFAULT_TEMPERATURE_DIFFERENCE,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_HEAT_SUPPLIED,
    PROPERTY_HEAT_SUPPLY_SET_POINT,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
)
from omotes_simulator_core.entities.assets.utils import heat_demand_and_temperature_to_mass_flow
from omotes_simulator_core.solver.network.assets.production_asset import HeatBoundary

logger = logging.getLogger(__name__)


class ProductionCluster(AssetAbstract):
    """A ProductionCluster represents an asset that produces heat."""

    thermal_production_required: float | None
    """The thermal production required by the asset [W]."""

    temperature_in: float
    """The inlet temperature of the asset [K]."""

    temperature_out: float
    """The outlet temperature of the asset [K]."""

    pressure_supply: float
    """The supply pressure of the asset [Pa]."""

    control_mass_flow: bool
    """Flag to indicate whether the mass flow rate is controlled.
    If True, the mass flow rate is controlled. If False, the mass flow rate is not controlled
    and the pressure is predescribed.
    """

    controlled_mass_flow: float | None
    """The controlled mass flow of the asset [kg/s]."""

    heat_demand_set_point: float
    """The heat demand set point of the asset [W]."""

    first_time_step: bool
    """Flag to indicate whether it is the first time step of the simulation."""

    def __init__(self, asset_name: str, asset_id: str, port_ids: list[str]):
        """Initialize a ProductionCluster object.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param List[str] port_ids: List of ids of the connected ports.
        """
        super().__init__(asset_name=asset_name, asset_id=asset_id, connected_ports=port_ids)
        self.height_m = DEFAULT_NODE_HEIGHT
        # DemandCluster thermal and mass flow specifications
        self.thermal_production_required = None
        self.temperature_out = DEFAULT_TEMPERATURE
        self.temperature_in = DEFAULT_TEMPERATURE - DEFAULT_TEMPERATURE_DIFFERENCE
        # DemandCluster pressure specifications
        self.pressure_supply = DEFAULT_PRESSURE
        self.heat_demand_set_point = 0.0
        self.control_mass_flow = False
        # Controlled mass flow
        self.controlled_mass_flow = None
        self.solver_asset = HeatBoundary(
            name=self.name,
            _id=self.asset_id,
            pre_scribe_mass_flow=False,
            set_pressure=self.pressure_supply,
        )
        # Define first time step
        self.first_time_step = True

    def _set_out_temperature(self, temperature_out: float) -> None:
        """Set the outlet temperature of the asset.

        :param float temperature_out: The outlet temperature of the asset.
            The temperature should be supplied in Kelvin.
        """
        # Set the temperature of the circulation pump mass flow
        self.temperature_out = temperature_out
        self.solver_asset.supply_temperature = self.temperature_out

    def _set_in_temperature(self, temperature_in: float) -> None:
        """Set the inlet temperature of the asset.

        :param float temperature_in: The inlet temperature of the asset.
            The temperature should be supplied in Kelvin.
        """
        # Set the inlet temperature of the asset
        if self.first_time_step or self.solver_asset.prev_sol[0] == 0.0:
            self.temperature_in = temperature_in
            self.first_time_step = False
        else:
            self.temperature_in = self.solver_asset.get_temperature(0)

    def _set_heat_demand(self, heat_demand: float) -> None:
        """Set the heat demand of the asset.

        :param float heat_demand: The heat demand of the asset.
            The heat demand should be supplied in Watts.
        """
        # Calculate the mass flow rate
        self.heat_demand_set_point = heat_demand
        self.controlled_mass_flow = heat_demand_and_temperature_to_mass_flow(
            thermal_demand=heat_demand,
            temperature_in=self.temperature_in,
            temperature_out=self.temperature_out,
        )

        # Check if the mass flow rate is positive
        if self.controlled_mass_flow < 0.0:
            logger.error(
                f"The mass flow rate {self.controlled_mass_flow} of the asset {self.name}"
                + " is negative.",
                extra={"esdl_object_id": self.asset_id},
            )
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
            self.solver_asset.pre_scribe_mass_flow = True  # type: ignore

    def set_pressure_supply(self, pressure_supply: float) -> None:
        """Set the supply pressure of the asset.

        :param float pressure_supply: The supply pressure of the asset.
            The pressure should be supplied in Pascal.
        """
        # Check if the pressure is positive
        if pressure_supply < 0.0:
            logger.error(
                f"The pressure {pressure_supply} of the asset {self.name} can not be negative.",
                extra={"esdl_object_id": self.asset_id},
            )
            raise ValueError(
                f"The pressure {pressure_supply} of the asset {self.name} can not be negative."
            )
        # Set the supply pressure of the asset
        self.pressure_supply = pressure_supply
        # Set the pressure of the solver asset
        self.solver_asset.set_pressure = self.pressure_supply  # type: ignore

    def set_setpoints(self, setpoints: dict) -> None:
        """Set the setpoints of the asset.

        :param Dict setpoints: The setpoints of the asset in a dictionary,
            as "property_name": value pairs.

        """
        # Default keys required
        necessary_setpoints = {
            PROPERTY_TEMPERATURE_IN,
            PROPERTY_TEMPERATURE_OUT,
            PROPERTY_HEAT_DEMAND,
            PROPERTY_SET_PRESSURE,
        }
        # Dict to set
        setpoints_set = set(setpoints.keys())
        # Check if all setpoints are in the setpoints
        if necessary_setpoints.issubset(setpoints_set):
            # Set the setpoints
            self._set_pressure_or_mass_flow_control(setpoints[PROPERTY_SET_PRESSURE])
            self._set_out_temperature(setpoints[PROPERTY_TEMPERATURE_OUT])
            self._set_in_temperature(setpoints[PROPERTY_TEMPERATURE_IN])
            self._set_heat_demand(setpoints[PROPERTY_HEAT_DEMAND])
        else:
            # Print missing setpoints
            logger.error(
                f"The setpoints {necessary_setpoints.difference(setpoints_set)} are missing.",
                extra={"esdl_object_id": self.asset_id},
            )
            raise ValueError(
                f"The setpoints {necessary_setpoints.difference(setpoints_set)} are missing."
            )

    def update(self) -> None:
        """Update the asset properties to the results from the previous (timestep) simulation.

        Sets the values of the outlet temperature, inlet temperature and heat demand
        to the values of the previous simulation. In addition, the mass flow rate is set
        to the value of the previous simulation.
        """

    def get_actual_heat_supplied(self) -> float:
        """Get the actual heat supplied by the asset.

        :return float: The actual heat supplied by the asset [W].
        """
        return (
            self.solver_asset.get_internal_energy(1) - self.solver_asset.get_internal_energy(0)
        ) * self.solver_asset.get_mass_flow_rate(1)

    def write_to_output(self) -> None:
        """Method to write time step results to the output dict.

        The output list is a list of dictionaries, where each dictionary
        represents the output of the asset for a specific timestep.
        """
        output_dict_temp = {
            PROPERTY_HEAT_SUPPLY_SET_POINT: self.heat_demand_set_point,
            PROPERTY_HEAT_SUPPLIED: self.get_actual_heat_supplied(),
        }
        self.outputs[1][-1].update(output_dict_temp)

    def is_converged(self) -> bool:
        """Check if the asset has converged with accepted error of 0.1%.

        The convergence criteria verifies whether the heat supplied
        by the asset - based on the solver asset - matches the heat demand
        set point of the asset.

        In other words: |Q_calculated - Q_setpoint| < 0.1% * |Q_setpoint|

        :return: True if the asset has converged, False otherwise
        """
        if self.solver_asset.pre_scribe_mass_flow:  # type: ignore
            return abs(self.get_actual_heat_supplied() - self.heat_demand_set_point) < (
                abs(self.heat_demand_set_point * 0.001)
            )
        else:
            return True
