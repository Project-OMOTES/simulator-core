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

"""Test Junction entities."""
import unittest
import uuid
from datetime import datetime
from pathlib import Path

from omotes_simulator_core.adapter.transforms.controller_mapper import EsdlControllerMapper
from omotes_simulator_core.adapter.transforms.mappers import EsdlEnergySystemMapper
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.entities.heat_network import HeatNetwork
from omotes_simulator_core.entities.simulation_configuration import SimulationConfiguration
from omotes_simulator_core.infrastructure.plotting import Plotting
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file
from omotes_simulator_core.simulation.networksimulation import NetworkSimulation


class PlottingTest(unittest.TestCase):
    """Test class for plotting object."""

    def test_plotting(self):
        """Test for plotting simulation results."""
        # Arrange
        esdl_file_path = Path(__file__).parent / ".." / ".." / "testdata" / "test1.esdl"
        esdl_file_path = str(esdl_file_path)
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        network = HeatNetwork(EsdlEnergySystemMapper(esdl_object).to_entity)
        controller = EsdlControllerMapper().to_entity(esdl_object)
        network_simulation = NetworkSimulation(network, controller)
        config = SimulationConfiguration(
            simulation_id=uuid.uuid1(),
            name="test run",
            timestep=3600,
            start=datetime.strptime("2019-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S"),
            stop=datetime.strptime("2019-01-01T01:00:00", "%Y-%m-%dT%H:%M:%S"),
        )
        network_simulation.run(config, lambda fraction, msg: None)
        result = network_simulation.gather_output()

        # Act
        plotting = Plotting(esdl_object)
        plotting.simulation_output(result)

        # Assert
        self.assertTrue(Path("./map.html").is_file())
