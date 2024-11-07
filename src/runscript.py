from omotes_simulator_core.adapter.transforms.mappers import (
    EsdlControllerMapper,
    EsdlEnergySystemMapper,
)
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.entities.heat_network import HeatNetwork
from omotes_simulator_core.entities.simulation_configuration import SimulationConfiguration
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file
from omotes_simulator_core.simulation.networksimulation import NetworkSimulation
from omotes_simulator_core.infrastructure.simulation_manager import SimulationManager
from omotes_simulator_core.infrastructure.plotting import Plotting

from pathlib import Path
from unittest.mock import Mock
import uuid
from datetime import datetime

if __name__ == "__main__":
    # Arrange
    esdl_file_path = Path(__file__).parent / ".." / "testdata" / "test_ates.esdl"
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
                                     stop=datetime.strptime("2019-01-01T06:00:00",
                                                            "%Y-%m-%dT%H:%M:%S"))
    # Act
    callback = Mock()
    app = SimulationManager(EsdlObject(pyesdl_from_file(esdl_file_path)), config)

    # Act
    result = app.execute(callback)

    plotting = Plotting(esdl_object)
    plotting.simulation_output(result)
