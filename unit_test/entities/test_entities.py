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

from simulator_core.adapter.transforms.mappers import EsdlEnergySystemMapper
from simulator_core.entities.esdl_object import EsdlObject
from simulator_core.entities.heat_network import HeatNetwork
from simulator_core.infrastructure.utils import pyesdl_from_file


class HeatNetworkTest(unittest.TestCase):
    """Testcase for HeatNetwork class."""

    def test_heat_network(self) -> None:
        """Generic/template test for Heatnetwork."""
        # Arrange
        esdl_file_path = Path(__file__).parent / ".." / ".." / "testdata" / "test1.esdl"
        esdl_file_path = str(esdl_file_path)
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))

        # Act
        network = HeatNetwork(EsdlEnergySystemMapper(esdl_object).to_entity)  # act

        # Assert
        self.assertIsInstance(network, HeatNetwork)
        self.assertEqual(len(network.assets), 4)
        self.assertEqual(len(network.junctions), 4)
