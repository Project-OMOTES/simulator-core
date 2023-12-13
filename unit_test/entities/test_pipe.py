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

"""Test Entitites."""
import unittest
from pathlib import Path

import pandapipes as pp

from simulator_core.adapter.transforms.mappers import EsdlEnergySystemMapper
from simulator_core.entities.assets import Junction, Pipe
from simulator_core.entities.esdl_object import EsdlObject
from simulator_core.infrastructure.utils import pyesdl_from_file


class PipeTest(unittest.TestCase):
    """Testcase for HeatNetwork class."""

    def setUp(self):
        # Create empty pandapipes network
        self.network = pp.create_empty_network()
        # Create two junctions
        self.from_juction = Junction("from_junction", "from_junction_id", self.network)
        self.to_junction = Junction("to_junction", "to_junction_id", self.network)

    def test_pipe_init(self):
        """Generic/template test for Pipe."""
        # Arrange
        pipe = Pipe("pipe", "pipe_id", self.network)
        # Assert
        self.assertIsInstance(pipe, Pipe)
        self.assertEqual(pipe.name, "pipe")
        self.assertEqual(pipe.id, "pipe_id")
        self.assertEqual(pipe.network, self.network)
