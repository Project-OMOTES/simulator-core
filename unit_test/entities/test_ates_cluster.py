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

"""Test Ates Cluster entities."""
import unittest
from unittest.mock import Mock

from simulator_core.entities.assets.junction import Junction
from simulator_core.entities.assets.ates_cluster import AtesCluster
from simulator_core.entities.assets.asset_defaults import (
    PROPERTY_HEAT_DEMAND,
    PROPERTY_TEMPERATURE_RETURN,
    PROPERTY_TEMPERATURE_SUPPLY,
)


class AtesClusterTest(unittest.TestCase):
    """Testcase for AtesCluster class."""

    def setUp(self) -> None:
        """Set up test case."""
        # Create empty pandapipes network
        # Create two junctions
        self.from_junction = Junction(solver_node=Mock(), name="from_junction")
        self.to_junction = Junction(solver_node=Mock(), name="to_junction")
        # Create a production cluster object
        self.ates_cluster = AtesCluster(
            asset_name="ates_cluster",
            asset_id="ates_cluster_id",
        )
        self.ates_cluster.set_from_junction(from_junction=self.from_junction)
        self.ates_cluster.set_to_junction(to_junction=self.to_junction)

    def test_injection(self) -> None:
        """Test injection to ATES."""

        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: 1e6,
            PROPERTY_TEMPERATURE_SUPPLY: 353.15,
            PROPERTY_TEMPERATURE_RETURN: 313.15,
        }

        # Act
        self.ates_cluster.set_setpoints(setpoints=setpoints)

        # Assert
        assert self.ates_cluster.temperature_supply == 353.15
        self.assertAlmostEqual(self.ates_cluster.temperature_return, 285.95, delta=0.01)

    def test_production(self) -> None:
        """Test production from ATES."""

        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: -1e6,
            PROPERTY_TEMPERATURE_SUPPLY: 353.15,
            PROPERTY_TEMPERATURE_RETURN: 313.15,
        }

        # Act
        self.ates_cluster.set_setpoints(setpoints=setpoints)

        # Assert
        assert self.ates_cluster.temperature_return == 313.15
        self.assertAlmostEqual(self.ates_cluster.temperature_supply, 285.95, delta=0.01)
