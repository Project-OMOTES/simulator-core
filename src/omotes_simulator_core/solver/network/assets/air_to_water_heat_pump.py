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
"""Implementation of the HeatBoundary class."""

from omotes_simulator_core.solver.network.assets.production_asset import HeatBoundary


class AirToWaterHeatPumpAsset(HeatBoundary):
    """Matrix object for the air to water heatpump asset."""

    def __init__(
        self,
        name: str,
        _id: str,
        supply_temperature: float = 293.15,
        heat_flux: float = 0.0,
        loss_coefficient: float = 1.0,
        pre_scribe_mass_flow: bool = True,
        mass_flow_rate_set_point: float = 10.0,
        set_pressure: float = 10000.0,
    ):
        """Initializes the AirToWaterHeatPumpAsset object with the given parameters."""
        super().__init__(
            name=name,
            _id=_id,
            supply_temperature=supply_temperature,
            heat_flux=heat_flux,
            loss_coefficient=loss_coefficient,
            pre_scribe_mass_flow=pre_scribe_mass_flow,
            mass_flow_rate_set_point=mass_flow_rate_set_point,
            set_pressure=set_pressure,
        )
