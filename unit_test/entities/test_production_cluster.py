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

from simulator_core.entities.assets.asset_defaults import (
    PROPERTY_HEAT_DEMAND,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_RETURN,
    PROPERTY_TEMPERATURE_SUPPLY,
)
from simulator_core.entities.assets.junction import Junction
from simulator_core.entities.assets.production_cluster import ProductionCluster
from simulator_core.entities.assets.utils import heat_demand_and_temperature_to_mass_flow


class ProductionClusterTest(unittest.TestCase):
    """Testcase for ProductionCluster class."""

    def setUp(self) -> None:
        """Set up test case."""
        # Create empty pandapipes network
        # Create two junctions
        self.from_junction = Junction(solver_node=Mock(), name="from_junction")
        self.to_junction = Junction(solver_node=Mock(), name="to_junction")
        # Create a production cluster object
        self.production_cluster = ProductionCluster(
            asset_name="production_cluster",
            asset_id="production_cluster_id",
        )
        self.production_cluster.set_from_junction(from_junction=self.from_junction)
        self.production_cluster.set_to_junction(to_junction=self.to_junction)

    def test_production_cluster_create(self) -> None:
        """Evaluate the creation of a production_cluster object."""
        # Arrange

        # Act
        # Assert
        assert isinstance(self.production_cluster, ProductionCluster)
        assert self.production_cluster.name == "production_cluster"
        assert self.production_cluster.asset_id == "production_cluster_id"

    def test_production_cluster_set_setpoints(self) -> None:
        """Test setting setpoints of a production cluster."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: 1e6,
            PROPERTY_TEMPERATURE_SUPPLY: 80,
            PROPERTY_TEMPERATURE_RETURN: 60,
            PROPERTY_SET_PRESSURE: False,
        }
        self.production_cluster.set_setpoints(setpoints=setpoints)

        # Act
        mass_flow = heat_demand_and_temperature_to_mass_flow(
            temperature_supply=setpoints[PROPERTY_TEMPERATURE_SUPPLY],
            temperature_return=setpoints[PROPERTY_TEMPERATURE_RETURN],
            thermal_demand=setpoints[PROPERTY_HEAT_DEMAND]

        )  # act

        # Assert
        assert self.production_cluster.temperature_supply == 80
        assert self.production_cluster.temperature_return == 60
        assert self.production_cluster._controlled_mass_flow == mass_flow
        assert (
            self.production_cluster.solver_asset.mass_flow_rate_set_point
            == self.production_cluster._controlled_mass_flow
        )

    def test_production_cluster_set_setpoints_missing_setpoint(self) -> None:
        """Test raise ValueError with missing setpoint."""
        # Arrange

        # Act
        necessary_setpoints = set(
            [PROPERTY_HEAT_DEMAND, PROPERTY_TEMPERATURE_SUPPLY, PROPERTY_TEMPERATURE_RETURN]
        )
        setpoints = {
            PROPERTY_TEMPERATURE_SUPPLY: 80,
            PROPERTY_TEMPERATURE_RETURN: 60,
            PROPERTY_SET_PRESSURE: False,
        }

        with self.assertRaises(ValueError) as cm:
            self.production_cluster.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            cm.exception.args[0],
            f"The setpoints {necessary_setpoints.difference(set(setpoints))} are missing.",
        )

    def test_production_cluster_set_setpoints_negative_mass_flow(self) -> None:
        """Test raise ValueError with negative mass flow."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: -1e6,
            PROPERTY_TEMPERATURE_SUPPLY: 80,
            PROPERTY_TEMPERATURE_RETURN: 60,
            PROPERTY_SET_PRESSURE: False,
        }

        # Act
        mass_flow = heat_demand_and_temperature_to_mass_flow(
            temperature_supply=setpoints[PROPERTY_TEMPERATURE_SUPPLY],
            temperature_return=setpoints[PROPERTY_TEMPERATURE_RETURN],
            thermal_demand=setpoints[PROPERTY_HEAT_DEMAND]
        )

        with self.assertRaises(ValueError) as cm:
            self.production_cluster.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            cm.exception.args[0],
            f"The mass flow rate {mass_flow} of the asset {self.production_cluster.name}"
            + " is negative.",
        )
