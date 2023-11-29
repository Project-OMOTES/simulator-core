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
import unittest
import uuid
from unittest.mock import Mock


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
        network = Mock()
        controller = Mock()
        network_simulation = NetworkSimulation(network, controller)
        config = SimulationConfiguration(simulation_id=uuid.uuid1(),
                                         name="test run",
                                         timestep=3600,
                                         start=0,
                                         stop=3600 * 48)
        # Act
        network_simulation.run(config)
        # Assert
        self.assertEqual(len(network_simulation.output), config.stop / config.timestep)

