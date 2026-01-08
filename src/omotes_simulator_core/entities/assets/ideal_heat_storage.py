#  Copyright (c) 2025. Deltares & TNO
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
from enum import Enum
from typing import Dict

import numpy as np

from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.asset_defaults import (
    DEFAULT_TEMPERATURE,
    PROPERTY_FILL_LEVEL,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
    PROPERTY_TIMESTEP,
)
from omotes_simulator_core.entities.assets.utils import heat_demand_and_temperature_to_mass_flow
from omotes_simulator_core.solver.network.assets.buffer_asset import HeatBufferAsset
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


class ChargeState(Enum):
    """Enum class to define the charge state of the heat buffer."""

    CHARGING = 1
    DISCHARGING = 2
    IDLE = 3


class IdealHeatStorage(AssetAbstract):
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
        initial_fill_level: float = 0.5,
    ) -> None:
        """Initialize a HeatBuffer object.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        """
        super().__init__(asset_name=asset_name, asset_id=asset_id, connected_ports=port_ids)

        # Supply and return temperature of the asset [K]
        self.temperature_connection_0 = DEFAULT_TEMPERATURE
        self.temperature_connection_1 = DEFAULT_TEMPERATURE

        # Temperature states
        self.buffer_temperature_hot = DEFAULT_TEMPERATURE
        self.buffer_temperature_cold = DEFAULT_TEMPERATURE

        # Volume properties of the asset: volume [m3], fill level [fraction 0-1]
        self.max_volume = volume
        self.fill_level = initial_fill_level
        self.current_volume_hot = self.max_volume * self.fill_level
        self.charge_state = ChargeState.IDLE

        # HeatBoundary since heat buffer acts either as producer or consumer,
        # positive flow is discharge and negative flow is charge
        self.solver_asset = HeatBufferAsset(
            name=self.name,
            _id=self.asset_id,
        )

        self.accumulation_time = 3600
        self.output: list = []
        self.first_time_step = True

    def set_charge_state(self, heat_demand: float) -> None:
        """Set the charge state of the heat buffer based on the heat demand.

        :param float heat_demand: The heat demand of the asset [W].
        """
        if heat_demand > 0:
            self.charge_state = ChargeState.DISCHARGING
        elif heat_demand < 0:
            self.charge_state = ChargeState.CHARGING
        else:
            self.charge_state = ChargeState.IDLE

    def update_state(self) -> None:
        """Placeholder to update the state of the asset after a simulation time step."""
        raise NotImplementedError("Method not implemented yet.")

    def set_setpoints(self, setpoints: Dict) -> None:
        """Controller input to the asset for each iteration until convergence.

        :param Dict setpoints: Controller setpoints for the asset.
        """
        # Check if all necessary setpoints are provided
        self.check_setpoints(setpoints)

        # Set charge state based on heat demand
        self.set_charge_state(setpoints[PROPERTY_HEAT_DEMAND])

        # Set temperatures based on charge state
        self.set_temperature_setpoints(setpoints)

        # Massflow rate based on heat demand and temperature setpoints
        mass_flowrate = heat_demand_and_temperature_to_mass_flow(
            setpoints[PROPERTY_HEAT_DEMAND],
            self.temperature_connection_0,
            self.temperature_connection_1,
        )

        # TODO: Move below to controller
        # Volumetric flow rate based on mass flow rate and density of the inlet temperature
        volumetric_flow_rate = mass_flowrate / fluid_props.get_density(
            self.temperature_connection_0
        )

        # Limit volumetric flow rate based on fill level and accumulation time
        if self.charge_state == ChargeState.CHARGING:
            available_volume = self.max_volume * (1 - self.fill_level)
        elif self.charge_state == ChargeState.DISCHARGING:
            available_volume = self.max_volume * self.fill_level
        else:  # IDLE
            available_volume = 0

        max_volumetric_flow_rate = available_volume / self.accumulation_time

        if abs(volumetric_flow_rate) > abs(max_volumetric_flow_rate):
            volumetric_flow_rate = np.sign(volumetric_flow_rate) * max_volumetric_flow_rate
            mass_flowrate = volumetric_flow_rate * fluid_props.get_density(
                self.temperature_connection_0
            )

        # Set solver asset setpoints
        self.solver_asset.inlet_massflow = mass_flowrate  # type: ignore
        self.solver_asset.temperature_connection_0 = self.temperature_connection_0  # type: ignore
        self.solver_asset.temperature_connection_1 = self.temperature_connection_1  # type: ignore

    def check_setpoints(self, setpoints: Dict) -> None:
        """Check if all necessary setpoints are provided.

        :param Dict setpoints: The setpoints that should be set for the asset.
        """
        # Default keys required
        necessary_setpoints = {
            PROPERTY_TEMPERATURE_IN,
            PROPERTY_TEMPERATURE_OUT,
            PROPERTY_HEAT_DEMAND,
        }
        # Create set of keys in the provided setpoints
        setpoints_set = set(setpoints.keys())
        # Check if all setpoints are in the setpoints
        if any(necessary_setpoints.difference(setpoints_set)):
            # Print missing setpoints
            raise ValueError(
                f"The setpoints {necessary_setpoints.difference(setpoints_set)} are missing."
            )

    def set_temperature_setpoints(self, setpoints: Dict) -> None:
        """Set the temperature setpoints of the asset prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the asset.
        The keys of the dictionary are the names of the setpoints and the values are the values
        """
        if self.first_time_step:
            self.temperature_connection_0 = setpoints[PROPERTY_TEMPERATURE_IN]
            self.temperature_connection_1 = setpoints[PROPERTY_TEMPERATURE_OUT]
            # Initialize state of buffer temperatures
            self.buffer_temperature_hot = self.temperature_connection_0
            self.buffer_temperature_cold = self.temperature_connection_1
            # Set first time step to False
            self.first_time_step = False
            # Exit the function after the first time step
            return

        # Define temperatures based on charge state
        if self.charge_state == ChargeState.CHARGING:
            # Massflow from connection point 0 to 1
            self.temperature_connection_0 = self.solver_asset.get_temperature(0)
            self.temperature_connection_1 = self.buffer_temperature_cold
        elif self.charge_state == ChargeState.DISCHARGING:
            # Massflow from connection point 1 to 0
            self.temperature_connection_0 = self.buffer_temperature_hot
            self.temperature_connection_1 = self.solver_asset.get_temperature(1)
        else:  # IDLE
            self.temperature_connection_0 = self.buffer_temperature_hot
            self.temperature_connection_1 = self.buffer_temperature_cold

    def _update_fill_level(self) -> None:
        """Update the fill level of the heat buffer based on mass flow rate and time step.

        math: fill_level = fill_level_previous + (m_dot / rho) * time_step / max_volume

        :return: None
        """
        # Volume change over time (dV/dt = m_dot / rho)
        dVdt = (-1 * self.solver_asset.get_mass_flow_rate(0)) / fluid_props.get_density(
            self.temperature_connection_0
        )
        # Update fill level (fill_level = level_previous + dV/dt * time_step / max_volume)
        self.fill_level = self.fill_level + (dVdt * self.time_step) / self.max_volume

    def _update_buffer_temperatures(self) -> None:
        """Update buffer temperature using a simple energy balance.

        :return: None
        """
        # Get internal energies and mass flows at connection points
        u_connection_0 = self.solver_asset.get_internal_energy(0)
        u_connection_1 = self.solver_asset.get_internal_energy(1)
        mass_flow_0 = -1 * self.solver_asset.get_mass_flow_rate(0)
        mass_flow_1 = -1 * self.solver_asset.get_mass_flow_rate(1)

        rho_hot = fluid_props.get_density(self.buffer_temperature_hot)
        rho_cold = fluid_props.get_density(self.buffer_temperature_cold)

        # Compute masses
        mass_hot = self.current_volume_hot * rho_hot
        mass_cold = (self.max_volume - self.current_volume_hot) * rho_cold
        mass_0 = mass_flow_0 * self.time_step
        mass_1 = mass_flow_1 * self.time_step

        # Get internal energy in buffer
        u_buffer_hot_old = fluid_props.get_ie(self.buffer_temperature_hot)
        u_buffer_cold_old = fluid_props.get_ie(self.buffer_temperature_cold)

        # Calculate new specific internal energies (J/kg)
        # Energy: u_old * mass_old + u_in * m_dot * time_step
        # Divide by new mass: mass_old + m_dot * time_step to get new specific internal energy
        u_buffer_hot_new = (
            u_buffer_hot_old * mass_hot + (u_connection_0 * mass_flow_0 * self.time_step)
        ) / (mass_hot + mass_0)
        u_buffer_cold_new = (
            u_buffer_cold_old * mass_cold + (u_connection_1 * mass_flow_1 * self.time_step)
        ) / (mass_cold + mass_1)

        # Update buffer temperatures based on new internal energies
        self.buffer_temperature_hot = fluid_props.get_t(u_buffer_hot_new)
        self.buffer_temperature_cold = fluid_props.get_t(u_buffer_cold_new)

    def get_state(self) -> dict[str, float]:
        """Get the state of the asset.

        :return: dict[str, float]
            A dictionary containing the state of the asset.
        """
        # Return the fill level and time step
        state = {
            PROPERTY_FILL_LEVEL: self.fill_level,
            PROPERTY_TIMESTEP: self.time_step,  # accumulation time
        }
        return state

    def write_to_output(self) -> None:
        """Write additional output properties of the asset."""
        pass

    def postprocess(self) -> None:
        """Postprocess after a simulation time step to update internal states.

        Method updates:
        - Buffer temperatures based on charge state
        - Fill level based on mass flow rate and time step
        - Current volume hot based on fill level

        :return: None
        """
        # Update buffer temperatures based on charge state
        self._update_buffer_temperatures()
        # Update fill level
        self._update_fill_level()
        # Update current volume hot
        self.current_volume_hot = self.max_volume * self.fill_level
