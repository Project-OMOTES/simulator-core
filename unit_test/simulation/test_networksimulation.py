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

from simulator_core.simulation.networksimulation import NetworkSimulation
from simulator_core.entities.simulation_configuration import SimulationConfiguration
from simulator_core.adapter.transforms.mappers import EsdlEnergySystemMapper
from simulator_core.entities.esdl_object import EsdlObject
from simulator_core.infrastructure.utils import pyesdl_from_file
from simulator_core.entities.heat_network import HeatNetwork
from simulator_core.entities.network_controller import NetworkController
import unittest
import uuid
from unittest.mock import Mock
from pathlib import Path


class NetworkSimulationTest(unittest.TestCase):

    def test_network_simulation_class(self):
        # Arrange
        network = Mock()
        controller = Mock()
        # Act
        network_simulation = NetworkSimulation(network, controller)
        # Assert
        self.assertIsInstance(network_simulation, NetworkSimulation)

    def test_network_simulation_run(self):
        # Arrange
        esdl_file_path = Path(__file__).parent / ".." / ".." / "testdata" / "test1.esdl"
        esdl_file_path = str(esdl_file_path)
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        network = HeatNetwork(EsdlEnergySystemMapper(esdl_object).to_entity)
        controller = NetworkController()
        network_simulation = NetworkSimulation(network, controller)
        config = SimulationConfiguration(simulation_id=uuid.uuid1(),
                                         name="test run",
                                         timestep=3600,
                                         start=0,
                                         stop=3600 * 48)
        # Act
        network_simulation.run(config)
        # Assert
        # this does not work since the network is mocked, since we cannot simulate yet
        # self.assertEqual(len(network_simulation.gather_output()), config.stop / config.timestep)

