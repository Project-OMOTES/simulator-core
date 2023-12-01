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

"""Simulates an heat network for the specified duration."""

from simulator_core.entities import HeatNetwork, NetworkController, SimulationConfiguration
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class NetworkSimulation:
    """NetworkSimulation connects the controller and HeatNetwork (incl. assets)."""

    def __init__(self, network: HeatNetwork, controller: NetworkController):
        """Instantiate the NetworkSimulation object."""
        self.network = network
        self.controller = controller

    def run(self, config: SimulationConfiguration):
        """Run the simulation.

        :param SimulationConfiguration config: Configuration to run the simulation with.
        """
        # time loop
        for time in range(config.start, config.stop, config.timestep):
            not_converged = True
            controller_input = self.controller.run_time_step(time)
            while not_converged:
                not_converged = False  # for the moment we do not check on convergence,
                # to get stuff running. Also need to add break after 10 iteration.
                logger.debug("Simulating for timestep " + str(time))
                self.network.run_time_step(time, controller_input)
            self.network.store_output()

    def gather_output(self) -> Dict[str, Dict[str, List[float]]]:
        """Gathers all output and return a dict with this output.

        :return: Dict with all output from all assets.
        """
        result = self.network.gather_output()
        return result
