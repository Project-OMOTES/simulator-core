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
"""Module containing the class for a heat trasnfer asset."""

from omotes_simulator_core.entities.assets.asset_defaults import (
    PRIMARY,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
    SECONDARY,
)
from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
    AssetControllerAbstract,
)


class ControllerHeatTransferAsset(AssetControllerAbstract):
    """Class for controlling a heat transfer asset."""

    max_power: float | None
    """Maximum electrical power of the heat pump [W]. None means no limit."""

    def __init__(
        self,
        name: str,
        identifier: str,
        factor: float,
        max_power: float | None = None,
    ):
        """Constructor of the class, which sets all attributes.

        :param str name: Name of the consumer.
        :param str identifier: Unique identifier of the consumer.
        :param float factor: The COP (heat pump) or efficiency (heat exchanger) factor.
        :param float | None max_power: Maximum electrical power for heat pump [W].
        """
        super().__init__(name, identifier)
        self.factor = factor
        self.max_power = max_power

    def get_max_secondary_power(self) -> float | None:
        """Get the maximum secondary (hot) side power output.

        For heat pump: max_secondary = max_electrical_power * COP.
        :return: Maximum secondary power [W], or None if no limit.
        """
        if self.max_power is None:
            return None
        return self.max_power * self.factor

    def set_asset(self, heat_demand: float) -> dict[str, dict[str, float]]:
        """Method to set the asset to the given heat demand.

        The supply and return temperatures are also set.
        :param float heat_demand: Heat demand to set.
        """
        # TODO set correct values also for prim and secondary side.
        return {
            self.id: {
                PRIMARY + PROPERTY_HEAT_DEMAND: heat_demand,
                PRIMARY + PROPERTY_TEMPERATURE_OUT: 273.15 + 30,
                PRIMARY + PROPERTY_TEMPERATURE_IN: 273.15 + 40,
                SECONDARY + PROPERTY_HEAT_DEMAND: heat_demand * self.factor,
                SECONDARY + PROPERTY_TEMPERATURE_OUT: 273.15 + 80,
                SECONDARY + PROPERTY_TEMPERATURE_IN: 273.15 + 50,
                PROPERTY_SET_PRESSURE: False,
            }
        }
