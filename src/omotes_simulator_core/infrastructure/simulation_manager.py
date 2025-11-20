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

"""Simulation manager creates and controls the simulation objects."""
import logging
from typing import Callable

import pandas as pd

from omotes_simulator_core.adapter.transforms.controller_mapper import EsdlControllerMapper
from omotes_simulator_core.adapter.transforms.mappers import EsdlEnergySystemMapper
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.entities.heat_network import HeatNetwork
from omotes_simulator_core.entities.simulation_configuration import SimulationConfiguration
from omotes_simulator_core.simulation.networksimulation import NetworkSimulation

logger = logging.getLogger(__name__)


class SimulationManager:
    """Manager class for managing the simulation."""

    def __init__(self, esdl: EsdlObject, config: SimulationConfiguration):
        """Constructor for SimulationManager class.

        :param EsdlObject esdl: Esdlobject, which stores the network information
        :param SimulationConfiguration config: Config object to hold the simulation start, stop, end
        """
        self.esdl = esdl
        self.config = config

    def execute(self, progress_calback: Callable[[float, str], None]) -> pd.DataFrame:
        """Method to simulate the network.

        First the network is converted to an internal object model and then the simulation is run.

        :return: DataFrame with the result of the simulations
        """
        try:
            # convert ESDL to Heat Network, NetworkController
            network = HeatNetwork(EsdlEnergySystemMapper(self.esdl).to_entity)
            controller = EsdlControllerMapper().to_entity(self.esdl, timestep=self.config.timestep)

            worker = NetworkSimulation(network, controller)
            worker.run(self.config, progress_calback)
        except Exception as error:
            logger.error(
                f"Error occured: {error}"
            )  # Asset ID is not set,  error is reported for the entire ESDL/run
            raise error

        # Run output presenter that iterates over het network (/controller?) and
        # gathers the output into a single data object
        return worker.gather_output()
