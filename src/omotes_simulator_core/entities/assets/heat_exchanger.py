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

"""HeatExchanger class."""
from typing import Dict

from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.asset_defaults import (
    DEFAULT_PRESSURE,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_HEAT_LOSS,
    PROPERTY_HEAT_POWER_PRIMARY,
    PROPERTY_HEAT_POWER_SECONDARY,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
)
from omotes_simulator_core.entities.assets.utils import heat_demand_and_temperature_to_mass_flow
from omotes_simulator_core.solver.network.assets.heat_transfer_asset import HeatTransferAsset


class HeatExchanger(AssetAbstract):
    """A HeatExchanger represents an asset that transfers heat between two sides of the network.

    The heat transfer efficiency from the ESDL asset is translated to a heat transfer coefficient
    or coefficient of performance (COP) used in the heat transfer solver asset.
    """

    temperature_in_primary: float
    """The inlet temperature of the heat exchanger on the primary side [K]."""

    temperature_out_primary: float
    """The outlet temperature of the heat exchanger on the primary side [K]."""

    temperature_in_secondary: float
    """The inlet temperature of the heat exchanger on the secondary side [K]."""

    temperature_out_secondary: float
    """The outlet temperature of the heat exchanger on the secondary side [K]."""

    mass_flow_primary: float
    """The mass flow of the heat exchanger on the primary side [kg/s]."""

    mass_flow_secondary: float
    """The mass flow of the heat exchanger on the secondary side [kg/s]."""

    control_mass_flow_secondary: bool
    """Flag to indicate whether the mass flow rate on the secondary side is controlled.
    If True, the mass flow rate is controlled. If False, the mass flow rate is not controlled
    and the pressure is predescribed.
    """

    heat_transfer_efficiency: float
    """Heat transfer efficiency of the heat exchanger [W/K]."""

    def __init__(
        self,
        asset_name: str,
        asset_id: str,
        connected_ports: list[str],
        heat_transfer_efficiency: float = 1,
    ) -> None:
        """Initialize a new HeatExchanger instance.

        :param asset_name: The name of the asset.
        :param asset_id: The unique identifier of the asset.
        :param connected_ports: The unique identifiers of the ports of the asset.
        :param heat_transfer_efficiency: The heat transfer efficiency of the heat exchanger.
        :type heat_transfer_efficiency: float
        """
        super().__init__(
            asset_name=asset_name,
            asset_id=asset_id,
            connected_ports=connected_ports,
        )
        # Set the heat transfer efficiency
        self.heat_transfer_efficiency = heat_transfer_efficiency

        # Define solver asset, which translates the efficiency of the ESDL asset to a
        # COP used in the heat transfer solver asset.
        self.solver_asset = HeatTransferAsset(
            name=self.name,
            _id=self.asset_id,
            pre_scribe_mass_flow_secondary=False,
            pressure_set_point_secondary=DEFAULT_PRESSURE,
            heat_transfer_coefficient=1 / self.heat_transfer_efficiency,
        )

    def _set_setpoints_secondary(self, setpoints_secondary: Dict) -> None:
        """The secondary side of the heat exchanger acts as a producer of heat.

        The necessary setpoints are:
        - PROPERTY_TEMPERATURE_IN
        - PROPERTY_TEMPERATURE_OUT
        - PROPERTY_HEAT_DEMAND
        - PROPERTY_SET_PRESSURE
        """
        # Default keys required
        necessary_setpoints = {
            PROPERTY_TEMPERATURE_IN,
            PROPERTY_TEMPERATURE_OUT,
            PROPERTY_HEAT_DEMAND,
            PROPERTY_SET_PRESSURE,
        }
        # Dict to set
        setpoints_set = set(setpoints_secondary.keys())
        # Check if all setpoints are in the setpoints
        if not necessary_setpoints.issubset(setpoints_set):
            # Print missing setpoints
            raise ValueError(
                f"The setpoints {necessary_setpoints.difference(setpoints_set)} are missing."
            )

        # Assign setpoints to the HeatPump asset
        self.temperature_in_secondary = setpoints_secondary[PROPERTY_TEMPERATURE_IN]
        self.temperature_out_secondary = setpoints_secondary[PROPERTY_TEMPERATURE_OUT]
        self.mass_flow_secondary = heat_demand_and_temperature_to_mass_flow(
            thermal_demand=setpoints_secondary[PROPERTY_HEAT_DEMAND],
            temperature_in=self.temperature_in_secondary,
            temperature_out=self.temperature_out_secondary,
        )
        self.control_mass_flow_secondary = setpoints_secondary[PROPERTY_SET_PRESSURE]

        # Assign setpoints to the HeatTransferAsset solver asset
        self.solver_asset.temperature_in_secondary = self.temperature_in_secondary  # type: ignore
        self.solver_asset.temperature_out_secondary = (  # type: ignore
            self.temperature_out_secondary
        )
        self.solver_asset.mass_flow_rate_secondary = self.mass_flow_secondary  # type: ignore
        self.solver_asset.pre_scribe_mass_flow_secondary = (  # type: ignore
            self.control_mass_flow_secondary
        )

    def _set_setpoints_primary(self, setpoints_primary: Dict) -> None:
        """The primary side of the heat exchanger acts as a consumer of heat.

        The necessary setpoints are:
        - PROPERTY_TEMPERATURE_IN
        - PROPERTY_TEMPERATURE_OUT
        - PROPERTY_HEAT_DEMAND

        :param Dict setpoints_primary: The setpoints of the primary side of the heat exchanger.
        """
        # TODO: Create a method that checks if the necessary setpoints are present in the setpoints
        #          in the DefaultAsset class and call this method here.
        # Default keys required
        necessary_setpoints = {
            PROPERTY_TEMPERATURE_IN,
            PROPERTY_TEMPERATURE_OUT,
            PROPERTY_HEAT_DEMAND,
        }
        # Dict to set
        setpoints_set = set(setpoints_primary.keys())
        # Check if all setpoints are in the setpoints
        if not necessary_setpoints.issubset(setpoints_set):
            # Print missing setpoints
            raise ValueError(
                f"The setpoints {necessary_setpoints.difference(setpoints_set)} are missing."
            )

        # Assign setpoints to the HeatPump asset
        self.temperature_in_primary = setpoints_primary[PROPERTY_TEMPERATURE_IN]
        self.temperature_out_primary = setpoints_primary[PROPERTY_TEMPERATURE_OUT]
        self.mass_flow_initialization_primary = heat_demand_and_temperature_to_mass_flow(
            thermal_demand=setpoints_primary[PROPERTY_HEAT_DEMAND],
            temperature_in=self.temperature_in_primary,
            temperature_out=self.temperature_out_primary,
        )

        # Assign setpoints to the HeatTransferAsset solver asset
        self.solver_asset.temperature_in_primary = self.temperature_in_primary  # type: ignore
        self.solver_asset.temperature_out_primary = self.temperature_out_primary  # type: ignore
        self.solver_asset.mass_flow_initialization_primary = (  # type: ignore
            self.mass_flow_initialization_primary
        )

    def set_setpoints(self, setpoints: Dict) -> None:
        """Placeholder to set the setpoints of an asset prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the asset.
            The keys of the dictionary are the names of the setpoints and the values are the values
        """
        # Set the setpoints for the primary side of the heat pump
        self._set_setpoints_primary(setpoints_primary=setpoints)
        # Set the setpoints for the secondary side of the heat pump
        self._set_setpoints_secondary(setpoints_secondary=setpoints)

    def write_to_output(self) -> None:
        """Get output power and electricity consumption of the asset.

        The output list is a list of dictionaries, where each dictionary
        represents the output of its asset for a specific timestep.
        """
        # Primary side output
        self.outputs[1][-1].update(
            {
                PROPERTY_HEAT_POWER_PRIMARY: (
                    self.solver_asset.get_heat_power_primary()  # type: ignore
                ),
                PROPERTY_HEAT_LOSS: (
                    self.solver_asset.get_heat_power_primary()  # type: ignore
                    - self.solver_asset.get_heat_power_secondary()  # type: ignore
                ),
            }
        )

        # Secondary side output
        self.outputs[0][-1].update(
            {
                PROPERTY_HEAT_POWER_SECONDARY: (
                    self.solver_asset.get_heat_power_secondary()  # type: ignore
                )
            }
        )
