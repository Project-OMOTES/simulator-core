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

"""Pump classes."""
from pandapipes import create_circ_pump_const_mass_flow, pandapipesNet

from simulator_core.entities.assets.junction import Junction

# TODO: Do we need to define a "general" pump class?


class CirculationPumpConstantMass:
    """Wrapper class for pandapipes circulation pumps with constant mass flow."""

    def __init__(
        self,
        pandapipes_net: pandapipesNet,
        from_junction: Junction,
        to_junction: Junction,
        p_to_junction: float,
        mdot_kg_per_s: float,
        t_to_junction: float,
        in_service: bool = True,
        name: str = None,
        index: int = None,
    ):
        """Initialize a CirculationPumpConstantMass object."""
        self.pandapipes_net = pandapipes_net
        self.from_junction = from_junction
        self.to_junction = to_junction
        self.p_to_junction = p_to_junction
        self.mdot_kg_per_s = mdot_kg_per_s
        self.t_to_junction = t_to_junction
        self.in_service = in_service
        self.name = name
        self.index = index
        # Initialize the pump
        self._initialized = False
        self._create()

    def _create(self) -> None:
        if not self._initialized:
            self._initialized = True
            # Register the pump in the pandapipes network
            self.index = create_circ_pump_const_mass_flow(
                net=self.pandapipes_net,
                return_junction=self.from_junction.index,
                flow_junction=self.to_junction.index,
                p_flow_bar=self.p_to_junction,
                mdot_flow_kg_per_s=self.mdot_kg_per_s,
                t_flow_k=self.t_to_junction,
                in_service=self.in_service,
                name=self.name,
                index=self.index,
            )
