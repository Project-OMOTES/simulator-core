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
from datetime import datetime, timedelta, timezone
from typing import Callable

from pandas import DataFrame

from omotes_simulator_core.entities.heat_network import HeatNetwork
from omotes_simulator_core.entities.network_controller import NetworkController
from omotes_simulator_core.entities.simulation_configuration import (
    SimulationConfiguration,
)

logger = logging.getLogger(__name__)

MAX_NUMBER_MESSAGES = 15


class NetworkSimulation:
    """NetworkSimulation connects the controller and HeatNetwork (incl. assets)."""

    def __init__(self, network: HeatNetwork, controller: NetworkController):
        """Instantiate the NetworkSimulation object."""
        self.network = network
        self.controller = controller

        # Define hidden attributes
        self._max_iterations = 20
        self._iteration = 0
        self._is_converged = False

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
        # Determine parameters of the time loop
        number_of_time_steps = int((config.stop - config.start).total_seconds() / config.timestep)
        logger.info("Number of time steps: %s", str(number_of_time_steps))
        progress_interval = max(round(number_of_time_steps / max_number_messages), 1)

        for time_step in range(number_of_time_steps):
            # Set the time for the current step
            time = (config.start + timedelta(seconds=time_step * config.timestep)).replace(
                tzinfo=timezone.utc
            )
            # Establish link between controller and network
            self.controller.update_network_state(network=self.network)

            # Update the controller with the current time
            controller_input = self.controller.update_setpoints(time=time)

            # Run step of the simulation
            self._step(time=time, timestep=config.timestep, controller_input=controller_input)

            # Store the output of the network
            self.network.store_output()

            # Progress callback
            if (time_step % progress_interval) == 0:
                progress_calback((float(time_step) / float(number_of_time_steps)), "calculating")

    def _step(self, time: datetime, timestep: float, controller_input: dict) -> None:
        """Run one step of the simulation.

        :param time: The time of the simulation step.
        :param timestep: The time step for the simulation.
        :param controller_input: The input from the controller.
        """
        # Log the simulation step
        logger.debug("Simulating for timestep %s", str(time))

        # Reset iteration and convergence status
        self._iteration = 0
        self._is_converged = False
        # Iteration loop to ensure convergence
        while not self._is_converged and self._iteration < self._max_iterations:
            self.network.run_time_step(
                time=time, time_step=timestep, controller_input=controller_input
            )
            self._is_converged = self.network.check_convergence()
            self._iteration += 1

    def gather_output(self) -> DataFrame:
        """Gathers all output and return a dict with this output.

        :return: DataFrame with all the results for the simulation
        """
        result = self.network.gather_output()
        return result
