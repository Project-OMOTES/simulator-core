#  Copyright (c) 2026. Deltares & TNO
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

"""GasHeater class."""
import logging

from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_ELECTRICITY_CONSUMPTION,
    PROPERTY_HEAT_SUPPLIED,
    PROPERTY_HEAT_SUPPLY_SET_POINT,
    HeatPumpDefaults,
)
from omotes_simulator_core.entities.assets.production_cluster import ProductionCluster
from omotes_simulator_core.solver.network.assets.production_asset import HeatBoundary

logger = logging.getLogger(__name__)


class GasHeater(ProductionCluster):
    """A gas heater asset.

    It represents a two port gas heater that adds heat to the network by consuming gas.
    """

    efficiency: float
    """The efficiency of the gas heater [-]."""

    def __init__(
        self,
        asset_name: str,
        asset_id: str,
        port_ids: list[str],
        efficiency: float = HeatPumpDefaults.coefficient_of_performance, #TODO: Make sure this takes a default of 1.0.
    ) -> None:
        """
        Initialize the GasHeater asset.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param List[str] port_ids: List of ids of the connected ports.
        """
        super().__init__(
            asset_name=asset_name,
            asset_id=asset_id,
            port_ids=port_ids,
        )
        self.efficiency = efficiency
        self.solver_asset = HeatBoundary(
            name=self.name,
            _id=self.asset_id,
            pre_scribe_mass_flow=False,
            set_pressure=self.pressure_supply,
        )

    def get_gas_consumption(self) -> float:
        """Calculate the gas power consumption of the gas heater.

        The gas power consumption is calculated as the ratio between the heat
        supplied by the heater to the network and the efficiency of the heater.

        :return: float
            The gas power consumption of the gas heater.
        """

        			# self.Gas_demand_mass_flow / 1000.0 * self.energy_content * self.efficiency
                    # - self.Heat_source

        return 1.0 # TODO: Fix this, it needs a gas energy content value. Check if it is already used somewhere else. 

    def write_to_output(self) -> None:
        """Method to write time step results to the output dict.

        The output list is a list of dictionaries, where each dictionary
        represents the output of the asset for a specific timestep.
        """
        output_dict_temp = {
            PROPERTY_HEAT_SUPPLY_SET_POINT: self.heat_demand_set_point,
            PROPERTY_HEAT_SUPPLIED: self.get_actual_heat_supplied(),
            PROPERTY_ELECTRICITY_CONSUMPTION: (self.get_gas_consumption()),
        }
        self.outputs[1][-1].update(output_dict_temp)  # Outputs appended to the out port.