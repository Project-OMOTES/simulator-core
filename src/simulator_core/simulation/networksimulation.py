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

""" Simulates an heat network for the specified duration."""

from simulator_core.entities import HeatNetwork, NetworkController, SimulationConfiguration


class NetworkSimulation:
    """NetworkSimulation connects the controller and HeatNetwork (incl. assets). """
    def __init__(self, network: HeatNetwork, controller: NetworkController):
        """Instantiate the NetworkSimulation object"""
        self.config = None
        self.network = network
        self.controller = controller

    def run(self, config: SimulationConfiguration):
        """Run the simulation.

        :param SimulationConfiguration"""
        self.config = config
