#  Copyright (c) 2024. Deltares & TNO
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
"""Module containing the classes for the controller."""

import logging
from typing import Optional

import numpy as np
import pandas as pd

from omotes_simulator_core.entities.assets.asset_defaults import (
    ATES_DEFAULTS,
    PROPERTY_BUFFER_COLD_TEMPERATURE,
    PROPERTY_BUFFER_HOT_TEMPERATURE,
    PROPERTY_COLD_WELL_TEMPERATURE,
    PROPERTY_FILL_LEVEL,
    PROPERTY_HOT_WELL_TEMPERATURE,
    PROPERTY_TIMESTEP,
)
from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
    AssetControllerAbstract,
)
from omotes_simulator_core.entities.assets.controller.temperature_data import Temperatures
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props

logger = logging.getLogger(__name__)

MINIMUM_USABLE_TEMPERATURE_FRACTION = 0.9
"""Minimum fraction of the temperature difference of the network an aquifer needs to deliver.

The aquifer supplies its water at the temperature of its hot well. When that temperature drops too
far below the supply temperature of the network, the supply side of the network is diluted and the
consumers cannot be supplied anymore. The aquifer is therefore only discharged while its hot well
still covers this fraction of the temperature difference of the network.
"""


class ControllerStorageAbstract(AssetControllerAbstract):
    """Abstract class to store the storage for the controller asset."""

    effective_max_charge_power: float
    """The effective maximum charge power of the storage."""

    effective_max_discharge_power: float
    """The effective maximum discharge power of the storage."""

    timestep: float
    """The timestep of the simulation or asset."""

    start_index: int
    """The start index for the profile lookup."""

    def __init__(
        self,
        name: str,
        identifier: str,
        temperatures: Temperatures,
        max_charge_power: float,
        max_discharge_power: float,
        profile: Optional[pd.DataFrame] = None,
    ):
        """Constructor for the storage.

        :param str name: Name of the storage.
        :param str identifier: Unique identifier of the consumer.
        :param float temperatures: Temperatures of the storage.
        :param float max_charge_power: Maximum charge power of the storage.
        :param float max_discharge_power: Maximum discharge power of the storage.
        :param Optional[pd.DataFrame] profile: Profile of the storage.
        """
        super().__init__(name, identifier)
        self.temperatures = temperatures

        # Profile of the storage.
        if profile is None:
            profile = pd.DataFrame()
        self.profile: pd.DataFrame = profile
        self.start_index = 0

        # Timestep of the simulation or asset.
        self.timestep: float = 3600  # [s]

        # Theoretical maximum charge and discharge power of the storage.
        self.max_charge_power: float = max_charge_power
        self.max_discharge_power: float = max_discharge_power

        # Effective maximum charge and discharge power of the storage.
        self.effective_max_charge_power: float = max_charge_power
        self.effective_max_discharge_power: float = max_discharge_power

    def set_state(self, state: dict[str, float]) -> None:
        """Set the state of the controller.

        :param dict[str, float] state: State of the controller from the asset_abstract
            get_state method.
        """

    def delta_temperature(self) -> float:
        """Get the temperature difference between the inlet and outlet.

        :return: float with the temperature difference.
        """
        return self.temperatures.in_flow - self.temperatures.out_flow

    def average_temperature(self) -> float:
        """Get the average temperature of the storage.

        :return: float with the average temperature.
        """
        return (self.temperatures.in_flow + self.temperatures.out_flow) / 2.0

    def get_effective_max_discharge_power(
        self,
    ) -> float:
        """Determine the effective maximum discharge power of the asset.

        The effective maximum discharge power is the maximum discharge power of the asset minus the
        volume of the asset. The effective maximum discharge power is calculated by dividing the
        available volume by the time step of the simulation. The available volume is the maximum
        volume of the asset minus the current volume. The effective maximum discharge power is
        limited by the maximum discharge power of the asset.
        """
        return self.effective_max_discharge_power

    def get_effective_max_charge_power(
        self,
    ) -> float:
        """Determine the effective maximum charge power of the asset.

        The effective maximum charge power is the maximum charge power of the asset minus the volume
        of the asset. The effective maximum charge power is calculated by dividing the available
        volume by the time step of the simulation. The available volume is the maximum volume of
        the asset minus the current volume. The effective maximum charge power is limited by the
        maximum charge power of the asset.
        """
        return self.effective_max_charge_power


class ControllerAtesStorage(ControllerStorageAbstract):
    """Class to store the storage for the controller asset."""

    hot_well_temperature: float
    """The temperature of the hot well of the aquifer [K]."""

    cold_well_temperature: float
    """The temperature of the cold well of the aquifer [K]."""

    def __init__(
        self,
        name: str,
        identifier: str,
        temperatures: Temperatures,
        max_charge_power: float,
        max_discharge_power: float,
        profile: Optional[pd.DataFrame] = None,
    ):
        """Constructor for the storage.

        :param str name: Name of the storage.
        :param str identifier: Unique identifier of the consumer.
        :param float temperatures: Temperatures of the storage.
        :param float max_charge_power: Maximum charge power of the storage.
        :param float max_discharge_power: Maximum discharge power of the storage.
        :param pd.DataFrame profile: Profile of the storage, defaults to empty DataFrame.
        """
        if profile is None:
            profile = pd.DataFrame()

        super().__init__(
            name=name,
            identifier=identifier,
            temperatures=temperatures,
            max_charge_power=max_charge_power,
            max_discharge_power=max_discharge_power,
            profile=profile,
        )

        # Well temperatures of the aquifer, updated with the state of the asset.
        self.hot_well_temperature = temperatures.out_flow
        self.cold_well_temperature = temperatures.in_flow

    def _power_from_maximum_flow(
        self,
        maximum_volume_flow: float,
        temperature_hot: float,
        temperature_cold: float,
    ) -> float:
        """Calculate the power that can be exchanged with the maximum flow of the wells.

        :param float maximum_volume_flow: Maximum volume flow of the well [m3/h].
        :param float temperature_hot: Temperature of the hot side of the asset [K].
        :param float temperature_cold: Temperature of the cold side of the asset [K].
        :return: float with the power which can be exchanged [W].
        """
        if temperature_hot <= temperature_cold:
            return 0.0
        average_temperature = (temperature_hot + temperature_cold) / 2.0
        mass_flow = (
            maximum_volume_flow / 3600.0 * fluid_props.get_density(average_temperature)
        )  # kg/s
        return mass_flow * (
            fluid_props.get_ie(temperature_hot) - fluid_props.get_ie(temperature_cold)
        )

    def get_minimum_discharge_temperature(self) -> float:
        """Determine the lowest hot well temperature which can still supply the network.

        :return: float with the minimum temperature of the hot well [K].
        """
        return self.temperatures.in_flow + MINIMUM_USABLE_TEMPERATURE_FRACTION * (
            self.temperatures.out_flow - self.temperatures.in_flow
        )

    def get_effective_max_discharge_power(self) -> float:
        """Determine the effective maximum discharge power of the asset.

        Discharging cools the hot well down. The asset delivers its water at the temperature of
        the hot well, so it can only supply the network while that temperature is close enough to
        the supply temperature of the network. Below that temperature the asset would dilute the
        supply side of the network and no power is available. The power is further limited by the
        maximum flow of the wells and by the temperature difference between the hot well and the
        return temperature of the network.

        :return: float with the effective maximum discharge power [W].
        """
        if self.hot_well_temperature < self.get_minimum_discharge_temperature():
            return 0.0
        return min(
            self.max_discharge_power,
            self._power_from_maximum_flow(
                maximum_volume_flow=ATES_DEFAULTS.maximum_flow_discharge,
                temperature_hot=self.hot_well_temperature,
                temperature_cold=self.temperatures.in_flow,
            ),
        )

    def get_effective_max_charge_power(self) -> float:
        """Determine the effective maximum charge power of the asset.

        Charging heats the hot well up with water from the supply side of the network. The power
        which can be charged is limited by the maximum flow of the wells and by the temperature
        difference between the supply temperature of the network and the cold well.

        :return: float with the effective maximum charge power [W].
        """
        return min(
            self.max_charge_power,
            self._power_from_maximum_flow(
                maximum_volume_flow=ATES_DEFAULTS.maximum_flow_charge,
                temperature_hot=self.temperatures.out_flow,
                temperature_cold=self.cold_well_temperature,
            ),
        )

    def set_state(self, state: dict[str, float]) -> None:
        """Set the state of the controller.

        :param dict[str, float] state: State of the controller from the asset_abstract
            get_state method.
        """
        available_state_keys = {
            PROPERTY_HOT_WELL_TEMPERATURE,
            PROPERTY_COLD_WELL_TEMPERATURE,
            PROPERTY_TIMESTEP,
        }
        if not available_state_keys.issubset(state.keys()):
            missing_keys = sorted(available_state_keys.difference(state.keys()))
            raise KeyError(f"State keys {missing_keys} are missing for storage {self.name}.")

        self.hot_well_temperature = state[PROPERTY_HOT_WELL_TEMPERATURE]
        self.cold_well_temperature = state[PROPERTY_COLD_WELL_TEMPERATURE]
        self.timestep = state[PROPERTY_TIMESTEP]

        # Update the effective maximum charge and discharge power of the asset.
        self.effective_max_charge_power = self.get_effective_max_charge_power()
        self.effective_max_discharge_power = self.get_effective_max_discharge_power()


class ControllerIdealHeatStorage(ControllerStorageAbstract):
    """Class to store the storage for the controller asset."""

    def __init__(
        self,
        name: str,
        identifier: str,
        temperatures: Temperatures,
        max_charge_power: float,
        max_discharge_power: float,
        fill_level: float,
        volume: float,
        profile: Optional[pd.DataFrame] = None,
    ):
        """Constructor for the storage.

        :param str name: Name of the storage.
        :param str identifier: Unique identifier of the consumer.
        :param float fill_level: Fill level of the storage [0-1].
        :param float volume: Volume of the storage [m3].
        """
        if profile is None:
            profile = pd.DataFrame()

        super().__init__(
            name=name,
            identifier=identifier,
            temperatures=temperatures,
            max_charge_power=max_charge_power,
            max_discharge_power=max_discharge_power,
            profile=profile,
        )

        # Fill level and max volume of the storage.
        self.fill_level: float = fill_level
        self.volume: float = volume
        self.volume_hot: float = fill_level * volume

        # Buffer temperatures
        self.buffer_temperature_hot: float = temperatures.in_flow
        self.buffer_temperature_cold: float = temperatures.out_flow

    def _calculate_power_from_volume(self, volume: float, is_discharge: bool) -> float:
        """Calculate power from available volume.

        :param float volume: Available volume in m3.
        :param bool is_discharge: True for discharge, False for charge.
        :return: Calculated power in W.
        """
        power = (
            (volume / self.timestep)  # (m3/s)
            * fluid_props.get_density(self.average_temperature())  # (kg/m3)
            * fluid_props.get_heat_capacity(self.average_temperature())  # (J/(kg K))
            * self.delta_temperature()  # (K)
        )  # W

        if is_discharge:
            return 1 * power
        return power

    def get_effective_max_discharge_power(
        self,
    ) -> float:
        """Determine the effective maximum discharge power of the asset.

        The effective maximum discharge power is the maximum discharge power of the asset minus the
        volume of the asset. The effective maximum discharge power is calculated by dividing the
        available volume by the time step of the simulation. The available volume is the maximum
        volume of the asset minus the current volume. The effective maximum discharge power is
        limited by the maximum discharge power of the asset.
        """
        # Calculate available volume
        available_volume = self.volume_hot

        if available_volume <= 0:
            return 0.0

        # Calculate power from available volume if dT > 0
        if (self.delta_temperature() == 0) and (self.fill_level > 0) and (self.fill_level < 1):
            return self.max_discharge_power
        elif self.delta_temperature() == 0:
            return 0.0
        else:
            power_from_volume = self._calculate_power_from_volume(
                available_volume, is_discharge=True
            )
            return min(self.max_discharge_power, power_from_volume)

    def get_effective_max_charge_power(
        self,
    ) -> float:
        """Determine the effective maximum charge power of the asset.

        The effective maximum charge power is the maximum charge power of the asset minus the volume
        of the asset. The effective maximum charge power is calculated by dividing the available
        volume by the time step of the simulation. The available volume is the maximum volume of
        the asset minus the current volume. The effective maximum charge power is limited by the
        maximum charge power of the asset.
        """
        # Calculate available volume
        available_volume = self.volume - self.volume_hot

        if available_volume <= 0 or self.fill_level >= 1.0:
            return 0.0

        # Calculate power from available volume if dT > 0
        # if (self.delta_temperature() == 0) and (self.fill_level > 0) and (self.fill_level < 1):
        #     return self.max_charge_power
        if self.delta_temperature() == 0:
            return 0.0
        else:
            power_from_volume = self._calculate_power_from_volume(
                available_volume, is_discharge=False
            )
            return min(self.max_charge_power, power_from_volume)

    def set_state(self, state: dict[str, float]) -> None:
        """Set the state of the controller.

        :param dict[str, float] state: State of the controller from the asset_abstract
            get_state method.
        """
        # Check available state keys
        available_state_keys = {
            PROPERTY_FILL_LEVEL,
            PROPERTY_BUFFER_HOT_TEMPERATURE,
            PROPERTY_BUFFER_COLD_TEMPERATURE,
            PROPERTY_TIMESTEP,
        }

        if available_state_keys.issubset(state.keys()):
            # Check limits fill level
            self._set_fill_level(state[PROPERTY_FILL_LEVEL])
            self.timestep = state[PROPERTY_TIMESTEP]
            # Set buffer temperatures
            self.buffer_temperature_hot = state[PROPERTY_BUFFER_HOT_TEMPERATURE]
            self.buffer_temperature_cold = state[PROPERTY_BUFFER_COLD_TEMPERATURE]
            # Update derived properties
            self.temperatures.in_flow = self.buffer_temperature_hot
            self.temperatures.out_flow = self.buffer_temperature_cold
        else:
            missing_keys = sorted(available_state_keys.difference(state.keys()))
            raise KeyError(f"State keys {missing_keys} are missing for storage {self.name}.")

        # Update the effective maximum charge and discharge power of the asset.
        self.effective_max_charge_power = self.get_effective_max_charge_power()
        self.effective_max_discharge_power = self.get_effective_max_discharge_power()

    def _set_fill_level(self, fill_level: float) -> None:
        """Set the fill level of the storage.

        :param float fill_level: Fill level of the storage between 0 and 1.
        """
        if 0.0 <= np.round(fill_level, 2) <= (1.0 + 0.01):
            self.fill_level = np.min([fill_level, 1.0])
            self.volume_hot = self.fill_level * self.volume
        else:
            raise ValueError(
                f"Fill level {fill_level} for storage {self.name} is out of bounds [0, 1]."
            )
