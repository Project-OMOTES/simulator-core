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

"""HeatPump class."""
import logging
from typing import Dict

from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.asset_defaults import (
    DEFAULT_PRESSURE,
    PRIMARY,
    PROPERTY_ELECTRICITY_CONSUMPTION,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_HEAT_POWER_PRIMARY,
    PROPERTY_HEAT_POWER_SECONDARY,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
    SECONDARY,
    HeatPumpDefaults,
)
from omotes_simulator_core.entities.assets.utils import heat_demand_and_temperature_to_mass_flow
from omotes_simulator_core.solver.network.assets.heat_transfer_asset import HeatTransferAsset

logger = logging.getLogger(__name__)


class HeatPump(AssetAbstract):
    """A HeatPump represents a combination of assets that produce heat."""

    temperature_in_primary: float
    """The inlet temperature of the heat pump on the primary side [K]."""

    temperature_out_primary: float
    """The outlet temperature of the heat pump on the primary side [K]."""

    temperature_in_secondary: float
    """The inlet temperature of the heat pump on the secondary side [K]."""

    temperature_out_secondary: float
    """The outlet temperature of the heat pump on the secondary side [K]."""

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

    maximum_power: float | None
    """Maximum electrical input power of the heat pump [W]. """

    _heat_demand_secondary_capped: float | None
    """Capped secondary heat demand setpoint [W]."""

    def __init__(
        self,
        asset_name: str,
        asset_id: str,
        connected_ports: list[str],
        coefficient_of_performance: float = HeatPumpDefaults.coefficient_of_performance,
        maximum_power: float | None = None,
    ) -> None:
        r"""Initialize a new HeatPump instance.

        The heat transfer coefficient of the heat pump is derived from the coefficient of
        performance using the relationship between the cold side (primary side) and hot
        side (secondary side).

        **Relationship between the COP and the heat transfer coefficient as defined in the heat
        transfer asset:**

        Starting from the energy balance and COP definition:

        .. math::

            Q_{hot} = W_{el} + Q_{cold}\\
            c = \frac{Q_{cold}}{Q_{hot}} \\
            W_{el} = \frac{Q_{hot}}{COP}\\
            Q_{hot} = \frac{Q_{hot}}{COP} + Q_{cold}\\
            1 = \frac{1}{COP} + c\\
            c = 1 - \frac{1}{COP}

        The dimensionless ratio :math:`c = Q_{cold}/Q_{hot}` is used in the heat transfer asset as
        the heat transfer coefficient to couple the primary and secondary sides.


        :param asset_name: The name of the asset.
        :param asset_id: The unique identifier of the asset.
        :connected_ports: The unique identifiers of the ports of the asset.
        :param coefficient_of_performance: The COP of the heat pump [-].
        :param maximum_power: Maximum electrical input power [W].
        """
        super().__init__(
            asset_name=asset_name,
            asset_id=asset_id,
            connected_ports=connected_ports,
        )
        # Set the coefficient of performance
        self.coefficient_of_performance = coefficient_of_performance
        self.maximum_power = maximum_power
        self._heat_demand_secondary_capped = None

        # Define solver asset
        self.solver_asset = HeatTransferAsset(
            name=self.name,
            _id=self.asset_id,
            pre_scribe_mass_flow_secondary=False,
            pressure_set_point_secondary=DEFAULT_PRESSURE,
            heat_transfer_coefficient=1.0 - 1.0 / self.coefficient_of_performance,
        )

    def _set_setpoints_secondary(self, setpoints_secondary: Dict) -> None:
        """The secondary side of the heat pump acts as a producer of heat.

        The necessary setpoints are:
        - PROPERTY_TEMPERATURE_IN
        - PROPERTY_TEMPERATURE_OUT
        - PROPERTY_HEAT_DEMAND
        - PROPERTY_SET_PRESSURE
        """
        # Default keys required
        necessary_setpoints = {
            SECONDARY + PROPERTY_TEMPERATURE_IN,
            SECONDARY + PROPERTY_TEMPERATURE_OUT,
            SECONDARY + PROPERTY_HEAT_DEMAND,
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
        self.temperature_in_secondary = setpoints_secondary[SECONDARY + PROPERTY_TEMPERATURE_IN]
        self.temperature_out_secondary = setpoints_secondary[SECONDARY + PROPERTY_TEMPERATURE_OUT]
        heat_demand_secondary = setpoints_secondary[SECONDARY + PROPERTY_HEAT_DEMAND]

        # Limit heat demand based on maximum electrical power cap
        if self.maximum_power is not None:
            required_electric_power = heat_demand_secondary / self.coefficient_of_performance
            if required_electric_power > self.maximum_power:
                capped_heat_demand_secondary = self.maximum_power * self.coefficient_of_performance
                logger.warning(
                    f"maximum electrical power of heat pump {self.name} exceeded. "
                    f"maximum power input {self.maximum_power} W is used. ",
                    extra={"esdl_object_id": self.asset_id},
                )
                heat_demand_secondary = capped_heat_demand_secondary

        self._heat_demand_secondary_capped = heat_demand_secondary
        self.mass_flow_secondary = heat_demand_and_temperature_to_mass_flow(
            thermal_demand=heat_demand_secondary,
            temperature_in=self.temperature_in_secondary,
            temperature_out=self.temperature_out_secondary,
        )
        self.control_mass_flow_secondary = not (setpoints_secondary[PROPERTY_SET_PRESSURE])

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
        """The primary side of the heat pump acts as a consumer of heat.

        The necessary setpoints are:
        - PROPERTY_TEMPERATURE_IN
        - PROPERTY_TEMPERATURE_OUT
        - PROPERTY_HEAT_DEMAND

        :param Dict setpoints_primary: The setpoints of the primary side of the heat pump.
        """
        # TODO: Create a method that checks if the necessary setpoints are present in the setpoints
        #          in the DefaultAsset class and call this method here.
        # Default keys required
        necessary_setpoints = {
            PRIMARY + PROPERTY_TEMPERATURE_IN,
            PRIMARY + PROPERTY_TEMPERATURE_OUT,
            PRIMARY + PROPERTY_HEAT_DEMAND,
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
        self.temperature_in_primary = setpoints_primary[PRIMARY + PROPERTY_TEMPERATURE_IN]
        self.temperature_out_primary = setpoints_primary[PRIMARY + PROPERTY_TEMPERATURE_OUT]
        self.mass_flow_initialization_primary = heat_demand_and_temperature_to_mass_flow(
            thermal_demand=setpoints_primary[PRIMARY + PROPERTY_HEAT_DEMAND],
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
        # Set the secondary side first to apply electrical power capping if necessary.
        self._set_setpoints_secondary(setpoints_secondary=setpoints)
        # Set primary setpoint based on capped secondary side using c=Q_cold/Q_hot = 1 - 1/COP.
        setpoints_primary = dict(setpoints)
        if self._heat_demand_secondary_capped is not None:
            setpoints_primary[PRIMARY + PROPERTY_HEAT_DEMAND] = (
                self._heat_demand_secondary_capped * (1.0 - 1.0 / self.coefficient_of_performance)
            )
        self._set_setpoints_primary(setpoints_primary=setpoints_primary)

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
                PROPERTY_ELECTRICITY_CONSUMPTION: (
                    self.solver_asset.get_electric_power_consumption()  # type: ignore
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
