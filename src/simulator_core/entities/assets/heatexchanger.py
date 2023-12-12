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

"""Heat exchanger classes."""
from pandapipes import create_heat_exchanger, pandapipesNet

from simulator_core.entities.assets.junction import Junction


class HeatExchanger:
    """Wrapper class for pandapipes heat exchanger."""

    def __init__(
            self,
            pandapipes_net: pandapipesNet,
            diameter_m: float,
            heat_flux_w: float,
            in_service: bool = True,
            name: str = None,
            index: int = None,
    ):
        """Initialize a HeatExchanger object."""
        self.pandapipes_net = pandapipes_net
        self.diameter_m = diameter_m
        self.heat_flux_w = heat_flux_w
        self.from_junction = Junction
        self.to_junction = Junction
        self.in_service = in_service
        self.name = name
        self.index = index
        # Initialize the heat exchanger
        self._initialized = False

    def create(self) -> None:
        """Register the heat exchanger in the pandapipes network."""
        if not self._initialized:
            self._initialized = True
            # Register the heat exchanger in the pandapipes network
            self.index = create_heat_exchanger(
                net=self.pandapipes_net,
                from_junction=self.from_junction.index,
                to_junction=self.to_junction.index,
                diameter_m=self.diameter_m,
                qext_w=self.heat_flux_w,
                in_service=self.in_service,
                name=self.name,
                index=self.index,
            )
