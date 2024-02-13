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

from pandas import DataFrame
from simulator_core.entities.heat_network import HeatNetwork
from simulator_core.entities.network_controller import NetworkController
from simulator_core.entities.simulation_configuration import SimulationConfiguration
from datetime import timedelta, timezone

import logging

logger = logging.getLogger(__name__)


class NetworkSimulation:
    """NetworkSimulation connects the controller and HeatNetwork (incl. assets)."""

    def __init__(self, network: HeatNetwork, controller: NetworkController):
        """Instantiate the NetworkSimulation object."""
        self.network = network
        self.controller = controller

    def run(self, config: SimulationConfiguration) -> None:
        """Run the simulation.

        :param SimulationConfiguration config: Configuration to run the simulation with.
        """
        # time loop
        number_of_time_steps = int((config.stop - config.start).total_seconds() / config.timestep)
        for time_step in range(number_of_time_steps):
            not_converged = True
            time = (config.start + timedelta(seconds=time_step * config.timestep)
                    ).replace(tzinfo=timezone.utc)
            controller_input = self.controller.run_time_step(time)

            while not_converged:
                not_converged = False  # for the moment we do not check on convergence,
                # to get stuff running. Also need to add break after 10 iteration.
                logger.debug("Simulating for timestep " + str(time))
                self.network.run_time_step(time, controller_input)
            self.network.store_output()

    def gather_output(self) -> DataFrame:
        """Gathers all output and return a dict with this output.

        :return: DataFrame with all the results for the simulation
        """
        result = self.network.gather_output()
        return result
