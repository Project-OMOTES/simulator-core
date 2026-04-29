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
    PROPERTY_BUFFER_COLD_TEMPERATURE,
    PROPERTY_BUFFER_HOT_TEMPERATURE,
    PROPERTY_FILL_LEVEL,
    PROPERTY_TIMESTEP,
)
from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
    AssetControllerAbstract,
)
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props

logger = logging.getLogger(__name__)


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
        temperature_in: float,
        temperature_out: float,
        max_charge_power: float,
        max_discharge_power: float,
        profile: Optional[pd.DataFrame] = None,
    ):
        """Constructor for the storage.

        :param str name: Name of the storage.
        :param str identifier: Unique identifier of the consumer.
        :param float temperature_in: Temperature of the inlet.
        :param float temperature_out: Temperature of the outlet.
        :param float max_charge_power: Maximum charge power of the storage.
        :param float max_discharge_power: Maximum discharge power of the storage.
        :param Optional[pd.DataFrame] profile: Profile of the storage.
        """
        super().__init__(name, identifier)
        self.temperature_out = temperature_out
        self.temperature_in = temperature_in

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
        return self.temperature_in - self.temperature_out

    def average_temperature(self) -> float:
        """Get the average temperature of the storage.

        :return: float with the average temperature.
        """
        return (self.temperature_in + self.temperature_out) / 2.0

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

    def __init__(
        self,
        name: str,
        identifier: str,
        temperature_in: float,
        temperature_out: float,
        max_charge_power: float,
        max_discharge_power: float,
        profile: Optional[pd.DataFrame] = None,
    ):
        """Constructor for the storage.

        :param str name: Name of the storage.
        :param str identifier: Unique identifier of the consumer.
        :param float temperature_in: Temperature of the inlet.
        :param float temperature_out: Temperature of the outlet.
        :param float max_charge_power: Maximum charge power of the storage.
        :param float max_discharge_power: Maximum discharge power of the storage.
        :param pd.DataFrame profile: Profile of the storage, defaults to empty DataFrame.
        """
        if profile is None:
            profile = pd.DataFrame()

        super().__init__(
            name=name,
            identifier=identifier,
            temperature_in=temperature_in,
            temperature_out=temperature_out,
            max_charge_power=max_charge_power,
            max_discharge_power=max_discharge_power,
            profile=profile,
        )

    def set_state(self, state: dict[str, float]) -> None:
        """Update maximum charge and discharge power."""
        if bool(state):
            self.effective_max_charge_power = state["max_charge_power"]
            self.effective_max_discharge_power = state["max_discharge_power"]


class ControllerIdealHeatStorage(ControllerStorageAbstract):
    """Class to store the storage for the controller asset."""

    def __init__(
        self,
        name: str,
        identifier: str,
        temperature_in: float,
        temperature_out: float,
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
            temperature_in=temperature_in,
            temperature_out=temperature_out,
            max_charge_power=max_charge_power,
            max_discharge_power=max_discharge_power,
            profile=profile,
        )

        # Fill level and max volume of the storage.
        self.fill_level: float = fill_level
        self.volume: float = volume
        self.volume_hot: float = fill_level * volume

        # Buffer temperatures
        self.buffer_temperature_hot: float = temperature_in
        self.buffer_temperature_cold: float = temperature_out

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
            self.temperature_in = self.buffer_temperature_hot
            self.temperature_out = self.buffer_temperature_cold
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
