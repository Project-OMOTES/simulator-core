#  Copyright (c) 2024. Deltares & TNO
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
import esdl
import uuid
import numpy as np
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock
import pandas as pd

from typing import Tuple

from omotes_simulator_core.adapter.transforms.mappers import (
    EsdlControllerMapper
)
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.entities.simulation_configuration import SimulationConfiguration
from omotes_simulator_core.infrastructure.simulation_manager import SimulationManager
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


class PressureDropTest(unittest.TestCase):
    """Class to store the heat demand tests."""

    def setUp(self) -> None:
        """Setting up and running the simulation used for the tests."""
        esdl_file_path = str(Path(__file__).parent / ".." / ".." / "testdata" / "test1.esdl")
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        self.controller = EsdlControllerMapper().to_entity(esdl_object)
        self.start_time = datetime.strptime("2019-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
        self.end_time = datetime.strptime("2019-01-01T06:00:00", "%Y-%m-%dT%H:%M:%S")
        config = SimulationConfiguration(
            simulation_id=uuid.uuid1(),
            name="test run",
            timestep=3600,
            start=self.start_time,
            stop=self.end_time
        )
        callback = Mock()
        app = SimulationManager(EsdlObject(pyesdl_from_file(esdl_file_path)), config)
        self.result = app.execute(callback)

        energy_system = esdl_object.energy_system_handler.energy_system

        # Collect demands, producers and pipes
        self.demands = []
        self.producers = []
        self.pipes = []
        
        for element in energy_system.eAllContents():
            if isinstance(element, esdl.HeatingDemand):
                self.demands.append(element)
            elif isinstance(element, esdl.GenericProducer):
                self.producers.append(element)
            elif isinstance(element, esdl.Pipe):
                self.pipes.append(element)

        # Collect id of in and out ports of each demand.
        self.in_out_demand_dict = dict()
        for demand in self.demands:
            self.in_out_demand_dict[demand.id] = dict()
            for port in demand.port:
                if isinstance(port, esdl.InPort):
                    self.in_out_demand_dict[demand.id]["InPort"] = port.id
                elif isinstance(port, esdl.OutPort):
                    self.in_out_demand_dict[demand.id]["OutPort"] = port.id

if __name__ == '__main__':
    test = PressureDropTest()
    test.setUp()