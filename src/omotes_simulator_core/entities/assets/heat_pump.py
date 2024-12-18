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

"""HeatPump class."""
from typing import Dict

from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.asset_defaults import (
    DEFAULT_PRESSURE,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_RETURN,
    PROPERTY_TEMPERATURE_SUPPLY,
)
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.entities.assets.utils import (
    heat_demand_and_temperature_to_mass_flow,
)
from omotes_simulator_core.solver.network.assets.heat_transfer_asset import HeatTransferAsset


class HeatPump(AssetAbstract):
    """A HeatPump represents a combination of assets that produce heat."""

    temperature_supply_primary: float
    """The supply temperature of the heat pump on the primary side [K]."""

    temperature_return_primary: float
    """The return temperature of the heat pump on the primary side [K]."""

    temperature_supply_secondary: float
    """The supply temperature of the heat pump on the secondary side [K]."""

    temperature_return_secondary: float
    """The return temperature of the heat pump on the secondary side [K]."""

    mass_flow_primary: float
    """The mass flow of the heat pump on the primary side [kg/s]."""

    mass_flow_secondary: float
    """The mass flow of the heat pump on the secondary side [kg/s]."""

    control_mass_flow_secondary: bool
    """Flag to indicate whether the mass flow rate on the secondary side is controlled.
    If True, the mass flow rate is controlled. If False, the mass flow rate is not controlled
    and the pressure is predescribed.
    """

    coefficient_of_performance: float
    """Coefficient of perfomance for the heat pump."""

    def __init__(self, asset_name: str, asset_id: str, connected_ports: list[str]):
        """Initialize a new HeatPump instance.

        :param asset_name: The name of the asset.
        :param asset_id: The unique identifier of the asset.
        :param port_ids: The unique identifiers of the ports of the asset.
        """
        super().__init__(
            asset_name=asset_name,
            asset_id=asset_id,
            connected_ports=connected_ports,
        )

        # Set default values for the temperatures
        # TODO: What are the default values for the temperatures?

        # Set default values for the mass flows
        # TODO: What are the default values for the mass flows?

        # Set the coefficient of performance
        # TODO: Include default value for the coefficient of performance
        self.coefficient_of_performance = 1 - 1 / 4.0

        # Define solver asset
        self.solver_asset = HeatTransferAsset(
            name=self.name,
            _id=self.asset_id,
            pre_scribe_mass_flow_secondary=False,
            pressure_set_point_secondary=DEFAULT_PRESSURE,
            heat_transfer_coefficient=self.coefficient_of_performance,
        )

    def add_physical_data(self, esdl_asset: EsdlAssetObject) -> None:
        """Method to add physical data to the asset.

        :param EsdlAssetObject esdl_asset: The ESDL asset object containing the physical data.
        :return:
        """
        # TODO: Do we want to set the coefficient of performance here?
        self.coefficient_of_performance, _ = esdl_asset.get_property(
            esdl_property_name="coefficient_of_performance",
            default_value=self.coefficient_of_performance,
        )

    def _set_setpoints_secondary(self, setpoints_secondary: Dict) -> None:
        """The secondary side of the heat pump acts as a producer of heat.

        The necessary setpoints are:
        - PROPERTY_TEMPERATURE_SUPPLY
        - PROPERTY_TEMPERATURE_RETURN
        - PROPERTY_HEAT_DEMAND
        - PROPERTY_SET_PRESSURE
        """
        # Default keys required
        necessary_setpoints = {
            PROPERTY_TEMPERATURE_SUPPLY,
            PROPERTY_TEMPERATURE_RETURN,
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
        self.temperature_supply_secondary = setpoints_secondary[PROPERTY_TEMPERATURE_SUPPLY]
        self.temperature_return_secondary = setpoints_secondary[PROPERTY_TEMPERATURE_RETURN]
        self.mass_flow_secondary = heat_demand_and_temperature_to_mass_flow(
            thermal_demand=setpoints_secondary[PROPERTY_HEAT_DEMAND],
            temperature_supply=self.temperature_supply_secondary,
            temperature_return=self.temperature_return_secondary,
        )
        self.control_mass_flow_secondary = setpoints_secondary[PROPERTY_SET_PRESSURE]

        # Assign setpoints to the HeatTransferAsset solver asset
        self.solver_asset.supply_temperature_secondary = (  # type: ignore
            self.temperature_supply_secondary
        )
        self.solver_asset.return_temperature_secondary = (  # type: ignore
            self.temperature_return_secondary
        )
        self.solver_asset.mass_flow_rate_secondary = self.mass_flow_secondary  # type: ignore
        self.solver_asset.pre_scribe_mass_flow_secondary = (  # type: ignore
            self.control_mass_flow_secondary
        )

    def _set_setpoints_primary(self, setpoints_primary: Dict) -> None:
        """The primary side of the heat pump acts as a consumer of heat.

        The necessary setpoints are:
        - PROPERTY_TEMPERATURE_SUPPLY
        - PROPERTY_TEMPERATURE_RETURN
        - PROPERTY_HEAT_DEMAND

        :param Dict setpoints_primary: The setpoints of the primary side of the heat pump.
        """
        # TODO: Create a method that checks if the necessary setpoints are present in the setpoints
        #          in the DefaultAsset class and call this method here.
        # Default keys required
        necessary_setpoints = {
            PROPERTY_TEMPERATURE_SUPPLY,
            PROPERTY_TEMPERATURE_RETURN,
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
        self.temperature_supply_primary = setpoints_primary[PROPERTY_TEMPERATURE_SUPPLY]
        self.temperature_return_primary = setpoints_primary[PROPERTY_TEMPERATURE_RETURN]
        self.mass_flow_primary = heat_demand_and_temperature_to_mass_flow(
            thermal_demand=setpoints_primary[PROPERTY_HEAT_DEMAND],
            temperature_supply=self.temperature_supply_primary,
            temperature_return=self.temperature_return_primary,
        )

        # Assign setpoints to the HeatTransferAsset solver asset
        self.solver_asset.supply_temperature_primary = (  # type: ignore
            self.temperature_supply_primary
        )
        self.solver_asset.return_temperature_primary = (  # type: ignore
            self.temperature_return_primary
        )
        self.solver_asset.mass_flow_rate_primary = self.mass_flow_primary  # type: ignore

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
        """Placeholder to write the asset to the output.

        The output list is a list of dictionaries, where each dictionary
        represents the output of its asset for a specific timestep.
        """
        pass
