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

"""ProductionCluster class."""
import logging

from omotes_simulator_core.entities.assets.production_cluster import ProductionCluster
from omotes_simulator_core.entities.assets.asset_defaults import (
    DEFAULT_NODE_HEIGHT,
    DEFAULT_PRESSURE,
    DEFAULT_TEMPERATURE,
    DEFAULT_TEMPERATURE_DIFFERENCE,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_HEAT_SUPPLIED,
    PROPERTY_HEAT_SUPPLY_SET_POINT,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
)
from omotes_simulator_core.entities.assets.utils import (
    heat_demand_and_temperature_to_mass_flow,
)
#from omotes_simulator_core.solver.network.assets.production_asset import HeatBoundary
from omotes_simulator_core.solver.network.assets.air_to_water_heat_pump import AirToWaterHeatPumpAsset

logger = logging.getLogger(__name__)

class AirToWaterHeatPump(ProductionCluster):
    def __init__(
        self,
        asset_name: str,
        asset_id: str,
        port_ids: list[str],
        coefficient_of_performance: float = 1 - 1 / 4.0,
    ) -> None:  
        super().__init__(
            asset_name=asset_name,
            asset_id=asset_id, 
            port_ids=port_ids,
            )
        self.solver_asset = AirToWaterHeatPumpAsset(
            name=self.name,
            _id=self.asset_id,
            pre_scribe_mass_flow=False,
            set_pressure=self.pressure_supply,
        )
        

# TODO: Add power requirement calculations here. Check how it is done witht he Production cluster here.
