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
import logging
from datetime import timedelta, timezone
from typing import Callable

from pandas import DataFrame

from omotes_simulator_core.entities.heat_network import HeatNetwork
from omotes_simulator_core.entities.network_controller import NetworkController
from omotes_simulator_core.entities.simulation_configuration import SimulationConfiguration

logger = logging.getLogger(__name__)

MAX_NUMBER_MESSAGES = 15


class NetworkSimulation:
    """NetworkSimulation connects the controller and HeatNetwork (incl. assets)."""

    def __init__(self, network: HeatNetwork, controller: NetworkController):
        """Instantiate the NetworkSimulation object."""
        self.network = network
        self.controller = controller

    def run(
        self,
        config: SimulationConfiguration,
        progress_calback: Callable[[float, str], None],
        max_number_messages: int = MAX_NUMBER_MESSAGES,
    ) -> None:
        """Run the simulation.

        :param SimulationConfiguration config: Configuration parameters for simulation.
        :param Callable[[float, str], None] progress_calback: Callback function to report progress.
        :param int max_number_messages: Maximum number of messages to report progress.
        """
        # time loop
        number_of_time_steps = int((config.stop - config.start).total_seconds() / config.timestep)
        logger.info("Number of time steps: " + str(number_of_time_steps))

        # Set interval for progress messages
        progress_interval = max(round(number_of_time_steps / max_number_messages), 1)

        for time_step in range(number_of_time_steps):
            # Update time to current time step
            time = (config.start + timedelta(seconds=time_step * config.timestep)).replace(
                tzinfo=timezone.utc
            )

            # Link controller to network
            self.controller.update_network_state(heat_network=self.network)

            # Update controller to current time
            controller_input = self.controller.update_setpoints(time)
            logger.debug("Simulating for timestep " + str(time))

            # Iteration loop to ensure convergence
            max_iterations = 20
            iteration = 0
            is_converged = False

            while not is_converged and iteration < max_iterations:
                # Run time step
                self.network.run_time_step(
                    time=time, time_step=config.timestep, controller_input=controller_input
                )

                # Check convergence
                is_converged = self.network.check_convergence()
                iteration += 1

            # Log warning if not converged
            logger.debug("Convergence time step reached after %d iterations", iteration)
            self.network.store_output()

            if (time_step % progress_interval) == 0:
                progress_calback((float(time_step) / float(number_of_time_steps)), "calculating")

    def gather_output(self) -> DataFrame:
        """Gathers all output and return a dict with this output.

        :return: DataFrame with all the results for the simulation
        """
        result = self.network.gather_output()
        return result
