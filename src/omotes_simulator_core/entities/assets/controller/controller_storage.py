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

import datetime
import logging

import pandas as pd

from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_FILL_LEVEL,
    PROPERTY_TIMESTEP,
    PROPERTY_VOLUME,
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

    _delta_temperature: float
    """The temperature difference between the supply and return temperature."""

    _average_temperature: float
    """The average temperature of the storage."""

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
        profile: pd.DataFrame,
    ):
        """Constructor for the storage.

        :param str name: Name of the storage.
        :param str identifier: Unique identifier of the consumer.
        :param float temperature_in: Temperature of the inlet.
        :param float temperature_out: Temperature of the outlet.
        :param float max_charge_power: Maximum charge power of the storage.
        :param float max_discharge_power: Maximum discharge power of the storage.
        :param pd.DataFrame profile: Profile of the storage.
        """
        super().__init__(name, identifier)
        self.temperature_out = temperature_out
        self.temperature_in = temperature_in
        self.profile: pd.DataFrame = profile
        self.start_index = 0

        # The temperature difference between the supply and return temperature.
        self._delta_temperature = temperature_in - temperature_out
        self._average_temperature = (temperature_in + temperature_out) / 2.0

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

    def get_heat_power(self, time: datetime.datetime) -> float:
        """Method to get the heat power of the storage. + is injection and - is production.

        :param datetime.datetime time: Time for which to get the heat demand.
        :return: float with the heat demand.
        """
        return 0.0

    def get_max_discharge_power(
        self,
    ) -> float:
        """Determine the effective maximum discharge power of the asset.

        The effective maximum discharge power is the maximum discharge power of the asset minus the
        volume of the asset. The effective maximum discharge power is calculated by dividing the
        available volume by the time step of the simulation. The available volume is the maximum
        volume of the asset minus the current volume. The effective maximum discharge power is
        limited by the maximum discharge power of the asset.
        """
        return 0.0

    def get_max_charge_power(
        self,
    ) -> float:
        """Determine the effective maximum charge power of the asset.

        The effective maximum charge power is the maximum charge power of the asset minus the volume
        of the asset. The effective maximum charge power is calculated by dividing the available
        volume by the time step of the simulation. The available volume is the maximum volume of
        the asset minus the current volume. The effective maximum charge power is limited by the
        maximum charge power of the asset.
        """
        return 0.0


class ControllerAtestStorage(ControllerStorageAbstract):
    """Class to store the storage for the controller asset."""

    def __init__(
        self,
        name: str,
        identifier: str,
        temperature_in: float,
        temperature_out: float,
        max_charge_power: float,
        max_discharge_power: float,
        profile: pd.DataFrame,
    ):
        """Constructor for the storage.

        :param str name: Name of the storage.
        :param str identifier: Unique identifier of the consumer.
        """
        super().__init__(
            name=name,
            identifier=identifier,
            temperature_in=temperature_in,
            temperature_out=temperature_out,
            max_charge_power=max_charge_power,
            max_discharge_power=max_discharge_power,
            profile=profile,
        )

    def get_heat_power(self, time: datetime.datetime) -> float:
        """Method to get the heat power of the storage. + is injection and - is production.

        :param datetime.datetime time: Time for which to get the heat demand.
        :return: float with the heat demand.
        """
        for index in range(self.start_index, len(self.profile)):
            if abs((self.profile["date"][index].to_pydatetime() - time).total_seconds()) < 3600:
                self.start_index = index
                if self.profile["values"][index] > self.max_charge_power:
                    logging.warning(
                        f"Storage of {self.name} is higher than maximum charge power of asset"
                        f" at time {time}."
                    )
                    return self.max_charge_power
                elif self.profile["values"][index] < self.max_discharge_power:
                    logging.warning(
                        f"Storage of {self.name} is higher than maximum discharge power of asset"
                        f" at time {time}."
                    )
                    return self.max_discharge_power
                else:
                    return float(self.profile["values"][index])
        return 0


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
        profile: pd.DataFrame,
        fill_level: float,
        max_volume: float,
    ):
        """Constructor for the storage.

        :param str name: Name of the storage.
        :param str identifier: Unique identifier of the consumer.
        """
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
        self.max_volume: float = max_volume
        self.current_volume: float = fill_level * max_volume

    def get_heat_power(self, time: datetime.datetime) -> float:
        """Method to get the heat power of the storage. + is injection and - is production.

        :param datetime.datetime time: Time for which to get the heat demand.
        :return: float with the heat demand.
        """
        # Check if the selected time is in the profile.
        # TODO: Current implementation loops over the entire profile; should be improved!
        # TODO: Unclear why there is a timestep of 1 hour in the profile.
        for index in range(self.start_index, len(self.profile)):
            if abs((self.profile["date"][index].to_pydatetime() - time).total_seconds()) < 3600:
                self.start_index = index
                if self.profile["values"][index] > self.effective_max_charge_power:
                    logging.warning(
                        "Supply to storage %s is higher than maximum charge power of asset"
                        + " at time %s.",
                        self.name,
                        time,
                    )
                    return self.effective_max_charge_power
                elif self.profile["values"][index] < self.effective_max_discharge_power:
                    logging.warning(
                        "Demand from storage %s is higher than maximum discharge power of asset"
                        + " at time %s.",
                        self.name,
                        time,
                    )
                    return self.effective_max_discharge_power
                else:
                    return float(self.profile["values"][index])
        # TODO: The loop is not complete as the asset also has a fill-level that should not surpass
        # the maximum fill-level.
        return 0.0

    def get_max_discharge_power(
        self,
    ) -> float:
        """Determine the effective maximum discharge power of the asset.

        The effective maximum discharge power is the maximum discharge power of the asset minus the
        volume of the asset. The effective maximum discharge power is calculated by dividing the
        available volume by the time step of the simulation. The available volume is the maximum
        volume of the asset minus the current volume. The effective maximum discharge power is
        limited by the maximum discharge power of the asset.

        :param float timestep: The time step of the simulation in seconds. Default is 3600 seconds.
        """
        # Calculate the effective maximum discharge power of the asset.
        available_volume = self.current_volume
        if available_volume > 0:
            effective_max_discharge_power = max(
                self.max_discharge_power,
                (
                    -1
                    * (available_volume / self.timestep)
                    * fluid_props.get_density(self._average_temperature)
                    * fluid_props.get_heat_capacity(self._average_temperature)
                    * self._delta_temperature
                ),
            )
        else:
            effective_max_discharge_power = 0.0
        return effective_max_discharge_power

    def get_max_charge_power(
        self,
    ) -> float:
        """Determine the effective maximum charge power of the asset.

        The effective maximum charge power is the maximum charge power of the asset minus the volume
        of the asset. The effective maximum charge power is calculated by dividing the available
        volume by the time step of the simulation. The available volume is the maximum volume of
        the asset minus the current volume. The effective maximum charge power is limited by the
        maximum charge power of the asset.

        :param float timestep: The time step of the simulation in seconds. Default is 3600 seconds.
        """
        # Calculate the effective maximum charge power of the asset.
        available_volume = self.max_volume - self.current_volume
        if available_volume > 0:
            effective_max_charge_power = min(
                self.max_charge_power,
                (
                    (available_volume / self.timestep)
                    * fluid_props.get_density(self._average_temperature)
                    * fluid_props.get_heat_capacity(self._average_temperature)
                    * self._delta_temperature
                ),
            )
        else:
            effective_max_charge_power = 0.0
        return effective_max_charge_power

    def set_state(self, state: dict[str, float]) -> None:
        """Set the state of the controller.

        :param dict[str, float] state: State of the controller from the asset_abstract
            get_state method.
        """
        # Check available state keys
        available_state_keys = {
            PROPERTY_FILL_LEVEL,
            PROPERTY_VOLUME,
            PROPERTY_TIMESTEP,
        }

        if available_state_keys.issubset(state.keys()):
            self.fill_level = state[PROPERTY_FILL_LEVEL]
            self.current_volume = state[PROPERTY_VOLUME]
            self.timestep = state[PROPERTY_TIMESTEP]
        else:
            missing_keys = sorted(available_state_keys.difference(state.keys()))
            raise ValueError(f"State keys {missing_keys} are missing.")

        # Update the effective maximum charge and discharge power of the asset.
        self.effective_max_charge_power = self.get_max_charge_power()
        self.effective_max_discharge_power = self.get_max_discharge_power()
