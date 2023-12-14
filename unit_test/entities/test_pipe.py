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
from unittest.mock import Mock

import pandapipes as pp

from simulator_core.entities.assets import Junction, Pipe


class PipeTest(unittest.TestCase):
    """Testcase for HeatNetwork class."""

    def setUp(self):
        """Set up test case."""
        # Create empty pandapipes network
        self.network = pp.create_empty_network()
        # Create two junctions
        self.from_junction = Junction(name="from_junction", pandapipes_net=self.network)
        self.to_junction = Junction(name="to_junction", pandapipes_net=self.network)

    def test_pipe_create(self):
        """Evaluate the creation of a pipe object."""
        # Arrange
        pipe = Pipe(asset_name="pipe", asset_id="pipe_id", pandapipe_net=self.network)
        pipe.from_junction = self.from_junction
        pipe.to_junction = self.to_junction

        # Act
        pipe.create()

        # Assert
        assert isinstance(pipe, Pipe)
        assert pipe.name == "pipe"
        assert pipe.asset_id == "pipe_id"
        assert pipe.pandapipes_net == self.network
        assert any(self.network.pipe.name == "Pipe_pipe")

    def test_pipe_unit_conversion(self):
        """Evaluate the unit conversion of the pipe object."""
        # Arrange
        pipe = Pipe(asset_name="pipe", asset_id="pipe_id", pandapipe_net=self.network)
        pipe.from_junction = self.from_junction
        pipe.to_junction = self.to_junction
        pipe.create()

        # Act
        pp_pipe_dataframe = self.network.pipe.iloc[pipe._pipe_index]

        # Assert
        assert pp_pipe_dataframe["length_km"] == pipe.length * 1e-3
        assert pp_pipe_dataframe["k_mm"] == pipe.roughness * 1e3

    def test_pipe_get_property_diameter(self):
        """Evaluate the get property diameter method to retrieve diameters."""
        # Arrange
        pipe = Pipe(asset_name="pipe", asset_id="pipe_id", pandapipe_net=self.network)
        pipe.from_junction = self.from_junction
        pipe.to_junction = self.to_junction
        esdl_asset_mock = Mock()
        esdl_asset_mock.get_property.return_value = (1.0, True)

        # Act
        pipe.create()

        # Assert
        assert pipe._get_diameter(esdl_asset=esdl_asset_mock) == 1.0

    def test_pipe_get_property_diameter_failed(self):
        """Evaluate failure to retrieve diameter from ESDL asset."""
        # Arrange
        pipe = Pipe(asset_name="pipe", asset_id="pipe_id", pandapipe_net=self.network)
        pipe.from_junction = self.from_junction
        pipe.to_junction = self.to_junction
        esdl_asset_mock = Mock()
        esdl_asset_mock.get_property.return_value = (1.0, False)

        # Act
        pipe.create()

        # Assert
        with self.assertRaises(NotImplementedError):
            pipe._get_diameter(esdl_asset=esdl_asset_mock)
