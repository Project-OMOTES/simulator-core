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

from simulator_core.entities import EsdlObject, SimulationConfiguration
from simulator_core.adapter.transforms.mappers import EsdlEnergySystemMapper, EsdlControllerMapper
from simulator_core.simulation import NetworkSimulation
from simulator_core.entities import HeatNetwork
import pandas as pd
import numpy as np


class SimulationManager:
    """Manager class for managing the simulation."""

    def __init__(self, esdl: EsdlObject, config: SimulationConfiguration):
        """Constructor for SimulationManager class.

        :param EsdlObject esdl: Esdlobject, which stores the network information
        :param SimulationConfiguration config: Config object to hold the simulation start, stop, end
        """
        self.esdl = esdl
        self.config = config

    def execute(self):
        """Method to simulate the network.

        First the network is converted to pandapipes and then the simulation is run.

        :return:
        """
        # convert ESDL to Heat Network, NetworkController
        network = HeatNetwork(EsdlEnergySystemMapper(self.esdl).to_entity)
        controller = EsdlControllerMapper().to_entity(self.esdl)

        worker = NetworkSimulation(network, controller)
        worker.run(self.config)

        # Run output presenter that iterates over het network (/controller?) and
        # gathers the output into a single data object

        # return dataframe.
        return pd.DataFrame(
            np.random.randn(10, 3),
            index=pd.date_range("1/1/2001", periods=10, freq="H"),
            columns=['DEMO flowrate', 'DEMO Pressure', 'DEMO Temperature'],
        )
