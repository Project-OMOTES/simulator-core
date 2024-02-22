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

import unittest
import uuid
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

from simulator_core.adapter.transforms.mappers import (
    EsdlControllerMapper,
    EsdlEnergySystemMapper,
)
from simulator_core.entities.esdl_object import EsdlObject
from simulator_core.entities.heat_network import HeatNetwork
from simulator_core.entities.simulation_configuration import SimulationConfiguration
from simulator_core.infrastructure.utils import pyesdl_from_file
from simulator_core.simulation.networksimulation import NetworkSimulation


class NetworkSimulationTest(unittest.TestCase):
    """Test clas for network simulation object."""

    def test_network_simulation_class(self):
        """Test for network simulation class creation."""
        # Arrange
        network = Mock()
        controller = Mock()

        # Act
        network_simulation = NetworkSimulation(network, controller)  # act

        # Assert
        self.assertIsInstance(network_simulation, NetworkSimulation)

    def test_network_simulation_run(self):
        """Test for network simulation."""
        # Arrange
        esdl_file_path = Path(__file__).parent / ".." / ".." / "testdata" / "test1.esdl"
        esdl_file_path = str(esdl_file_path)
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        network = HeatNetwork(EsdlEnergySystemMapper(esdl_object).to_entity)
        controller = EsdlControllerMapper().to_entity(esdl_object)
        network_simulation = NetworkSimulation(network, controller)
        config = SimulationConfiguration(simulation_id=uuid.uuid1(),
                                         name="test run",
                                         timestep=3600,
                                         start=datetime.strptime("2019-01-01T00:00:00",
                                                                 "%Y-%m-%dT%H:%M:%S"),
                                         stop=datetime.strptime("2019-01-01T01:00:00",
                                                                "%Y-%m-%dT%H:%M:%S"))
        # Act
        network_simulation.run(config)  # act

        # Assert
        # this does not work since the network is mocked, since we cannot simulate yet
        # self.assertEqual(len(network_simulation.gather_output()), config.stop / config.timestep)
