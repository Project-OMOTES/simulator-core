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

import simulator_core.entities.heat_network
from simulator_core.entities import HeatNetwork
import unittest


class HeatNetworkTest(unittest.TestCase):
    """Testcase for HeatNetwork class."""

    def test_heat_network(self) -> None:
        """Generic/template test for Heatnetwork."""
        # Arrange
        assets = []
        junctions = []
        # Act
        result = HeatNetwork(assets, junctions)

        # Assert
        assert isinstance(result, simulator_core.entities.heat_network.HeatNetwork)
