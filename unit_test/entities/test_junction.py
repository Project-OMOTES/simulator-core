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

"""Test Pipe entities."""
import unittest

import pandapipes as pp

from simulator_core.entities.assets.junction import Junction
from simulator_core.entities.assets.asset_defaults import DEFAULT_NODE_HEIGHT, DEFAULT_PRESSURE


class JunctionTest(unittest.TestCase):
    """Testcase for HeatNetwork class."""

    def setUp(self):
        """Set up test case."""
        # Create empty pandapipes network
        self.network = pp.create_empty_network()

    def test_junction_create(self):
        """Generic/template test for Junction."""
        # Arrange

        # Act
        from_junction = Junction(name="from_junction", pandapipes_net=self.network)  # act

        # Assert
        assert isinstance(from_junction, Junction)
        assert from_junction._initialized
        assert from_junction.name == "from_junction"
        assert from_junction.height_m == DEFAULT_NODE_HEIGHT
        assert from_junction.pn_bar == DEFAULT_PRESSURE
