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
import uuid
from datetime import datetime
from pathlib import Path
from typing import Tuple
from unittest.mock import Mock

import esdl
import numpy as np

from omotes_simulator_core.adapter.transforms.controller_mapper import EsdlControllerMapper
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.entities.simulation_configuration import SimulationConfiguration
from omotes_simulator_core.infrastructure.simulation_manager import SimulationManager
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file


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
            stop=self.end_time,
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

    def _get_in_out_port_id(self, asset) -> Tuple[str, str]:
        """Gets the in and out port ids for the given asset.

        Note that is method only works for assets with one in and one out port.
        """
        for port_check in asset.port:
            if isinstance(port_check, esdl.InPort):
                in_port_id = port_check.id
            else:
                out_port_id = port_check.id
        return in_port_id, out_port_id

    def test_pressure_drop(self) -> None:
        """
        This test checks whether the pressure drop has the correct sign.

        It does this by first computing the in and out ports of each asset,
        based on the mass flow sign. The pressure drop is computed as
        pressure out - pressure in and then asserts whether it is negaitve
        for pipes, positive for producers and negative for consumers.
        """
        for pipe in self.pipes:
            # Check which port is in and which out.
            [in_port_id, out_port_id] = self._get_in_out_port_id(pipe)
            # Compute pressure drop.
            p_out = self.result[out_port_id, "pressure"]
            p_in = self.result[in_port_id, "pressure"]
            delta_p_list = p_out - p_in
            for delta_p in delta_p_list:
                np.testing.assert_(delta_p < 0)

        for producer in self.producers:
            # Check which port is in and which out.
            [in_port_id, out_port_id] = self._get_in_out_port_id(producer)
            # Compute pressure drop.
            p_out = self.result[out_port_id, "pressure"]
            p_in = self.result[in_port_id, "pressure"]
            delta_p_list = p_out - p_in
            for delta_p in delta_p_list:
                np.testing.assert_(delta_p > 0)

        for demand in self.demands:
            # Check which port is in and which out.
            [in_port_id, out_port_id] = self._get_in_out_port_id(demand)
            # Compute pressure drop.
            p_out = self.result[out_port_id, "pressure"]
            p_in = self.result[in_port_id, "pressure"]
            delta_p_list = p_out - p_in
            for delta_p in delta_p_list:
                np.testing.assert_(delta_p < 0)
