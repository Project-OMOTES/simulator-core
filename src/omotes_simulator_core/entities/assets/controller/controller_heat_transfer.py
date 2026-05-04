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

from enum import Enum

from omotes_simulator_core.entities.assets.asset_defaults import (
    PRIMARY,
    PROPERTY_BYPASS,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
    SECONDARY,
)
from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
    AssetControllerAbstract,
)


class HeatTransferAssetType(Enum):
    """Enum to distinguish heat transfer asset types."""

    HEAT_PUMP = "heat_pump"
    HEAT_EXCHANGER = "heat_exchanger"


class ControllerHeatTransferAsset(AssetControllerAbstract):
    """Class for controlling a heat transfer asset."""

    heat_transfer_type: HeatTransferAssetType
    """Type of heat transfer asset (heat pump or heat exchanger)."""

    max_electrical_power: float | None
    """Maximum electrical power of the heat pump [W]. None means no limit."""

    def __init__(
        self,
        name: str,
        identifier: str,
        factor: float,
        heat_transfer_type: HeatTransferAssetType,
        max_electrical_power: float | None = None,
    ):
        """Constructor of the class, which sets all attributes.

        :param str name: Name of the consumer.
        :param str identifier: Unique identifier of the consumer.
        :param float factor: The COP (heat pump) or efficiency (heat exchanger) factor.
        :param HeatTransferAssetType heat_transfer_type: Type of heat transfer asset.
        :param float | None max_electrical_power: Maximum electrical power for heat pump [W].
        """
        super().__init__(name, identifier)
        self.factor = factor
        self.heat_transfer_type = heat_transfer_type
        self.max_electrical_power = max_electrical_power

    def set_asset_prim(
        self, heat_demand: float, bypass: bool = False
    ) -> dict[str, dict[str, float]]:
        """Method to set the asset to the given heat demand.

        The supply and return temperatures are also set.
        :param float heat_demand: Heat demand to set.
        :param bypass: When true the heat exchange is bypassed, so the heat demand is not
        reduced by the factor. Default is False.
        """
        if bypass:
            return {
                self.id: {
                    PRIMARY + PROPERTY_HEAT_DEMAND: -1 * heat_demand,
                    PRIMARY + PROPERTY_TEMPERATURE_OUT: 273.15 + 80,
                    PRIMARY + PROPERTY_TEMPERATURE_IN: 273.15 + 50,
                    SECONDARY + PROPERTY_HEAT_DEMAND: heat_demand,
                    SECONDARY + PROPERTY_TEMPERATURE_OUT: 273.15 + 80,
                    SECONDARY + PROPERTY_TEMPERATURE_IN: 273.15 + 50,
                    SECONDARY + PROPERTY_SET_PRESSURE: False,
                    PRIMARY + PROPERTY_SET_PRESSURE: False,
                    PROPERTY_BYPASS: True,
                }
            }
        else:
            return {
                self.id: {
                    PRIMARY + PROPERTY_HEAT_DEMAND: -1 * heat_demand,
                    PRIMARY + PROPERTY_TEMPERATURE_OUT: 273.15 + 30,
                    PRIMARY + PROPERTY_TEMPERATURE_IN: 273.15 + 50,
                    SECONDARY + PROPERTY_HEAT_DEMAND: heat_demand * self.factor,
                    SECONDARY + PROPERTY_TEMPERATURE_OUT: 273.15 + 80,
                    SECONDARY + PROPERTY_TEMPERATURE_IN: 273.15 + 40,
                    SECONDARY + PROPERTY_SET_PRESSURE: False,
                    PRIMARY + PROPERTY_SET_PRESSURE: False,
                    PROPERTY_BYPASS: False,
                }
            }

    def set_asset_sec(
        self, heat_demand: float, bypass: bool = False
    ) -> dict[str, dict[str, float]]:
        """Method to set the asset to the given heat demand.

        The supply and return temperatures are also set.
        :param float heat_demand: Heat demand to set.
        :param bypass: When true the heat exchange is bypassed, so the heat demand is not
        reduced by the factor. Default is False.
        """
        if bypass:
            return {
                self.id: {
                    PRIMARY + PROPERTY_HEAT_DEMAND: heat_demand,
                    PRIMARY + PROPERTY_TEMPERATURE_OUT: 273.15 + 80,
                    PRIMARY + PROPERTY_TEMPERATURE_IN: 273.15 + 50,
                    SECONDARY + PROPERTY_HEAT_DEMAND: -1 * heat_demand,
                    SECONDARY + PROPERTY_TEMPERATURE_OUT: 273.15 + 80,
                    SECONDARY + PROPERTY_TEMPERATURE_IN: 273.15 + 50,
                    SECONDARY + PROPERTY_SET_PRESSURE: False,
                    PRIMARY + PROPERTY_SET_PRESSURE: False,
                    PROPERTY_BYPASS: True,
                }
            }
        else:
            return {
                self.id: {
                    PRIMARY + PROPERTY_HEAT_DEMAND: heat_demand / self.factor,
                    PRIMARY + PROPERTY_TEMPERATURE_OUT: 273.15 + 30,
                    PRIMARY + PROPERTY_TEMPERATURE_IN: 273.15 + 50,
                    SECONDARY + PROPERTY_HEAT_DEMAND: -1 * heat_demand,
                    SECONDARY + PROPERTY_TEMPERATURE_OUT: 273.15 + 80,
                    SECONDARY + PROPERTY_TEMPERATURE_IN: 273.15 + 40,
                    SECONDARY + PROPERTY_SET_PRESSURE: False,
                    PRIMARY + PROPERTY_SET_PRESSURE: False,
                    PROPERTY_BYPASS: False,
                }
            }
