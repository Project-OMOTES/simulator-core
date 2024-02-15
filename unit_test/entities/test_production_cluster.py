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

import pandapipes as pp

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

    def setUp(self):
        """Set up test case."""
        # Create empty pandapipes network
        self.network = pp.create_empty_network(fluid="water")
        # Create two junctions
        self.from_junction = Junction(name="from_junction", pandapipes_net=self.network)
        self.to_junction = Junction(name="to_junction", pandapipes_net=self.network)
        # Create a production cluster object
        self.production_cluster = ProductionCluster(
            asset_name="production_cluster",
            asset_id="production_cluster_id",
            pandapipe_net=self.network,
        )
        self.production_cluster.set_from_junction(from_junction=self.from_junction)
        self.production_cluster.set_to_junction(to_junction=self.to_junction)

    def test_production_cluster_create(self):
        """Evaluate the creation of a production_cluster object."""
        # Arrange

        # Act
        self.production_cluster.create()  # act

        # Assert
        assert isinstance(self.production_cluster, ProductionCluster)
        assert self.production_cluster.name == "production_cluster"
        assert self.production_cluster.asset_id == "production_cluster_id"
        assert any(self.network.flow_control.name == "flow_control_production_cluster")

    def test_production_cluster_set_setpoints(self):
        """Test setting setpoints of a production cluster."""
        # Arrange
        self.production_cluster.create()
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
            thermal_demand=setpoints[PROPERTY_HEAT_DEMAND],
            pandapipes_net=self.network,
        )  # act

        # Assert
        assert self.production_cluster.temperature_supply == 80
        assert self.production_cluster.temperature_return == 60
        assert self.production_cluster._controlled_mass_flow == mass_flow
        assert (
            self.production_cluster.pandapipes_net["flow_control"]["controlled_mdot_kg_per_s"][0]
            == self.production_cluster._controlled_mass_flow
        )

    def test_production_cluster_set_setpoints_missing_setpoint(self):
        """Test raise ValueError with missing setpoint."""
        # Arrange
        self.production_cluster.create()

        # Act
        necessary_setpoints = set(
            [PROPERTY_HEAT_DEMAND, PROPERTY_TEMPERATURE_SUPPLY, PROPERTY_TEMPERATURE_RETURN]
        )
        setpoints = {
            PROPERTY_TEMPERATURE_SUPPLY: 80,
            PROPERTY_TEMPERATURE_RETURN: 60,
            PROPERTY_SET_PRESSURE: False,
        }

        # Assert
        with self.assertRaises(
            ValueError,
            match=f"The setpoints {necessary_setpoints.difference(set(setpoints))} "
            f"are missing.",
        ):
            self.production_cluster.set_setpoints(setpoints=setpoints)

    def test_production_cluster_set_setpoints_negative_mass_flow(self):
        """Test raise ValueError with negative mass flow."""
        # Arrange
        self.production_cluster.create()
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
            thermal_demand=setpoints[PROPERTY_HEAT_DEMAND],
            pandapipes_net=self.network,
        )

        # Assert
        with self.assertRaises(
            ValueError,
            match=f"The mass flow rate {mass_flow} of the asset {self.production_cluster.name}"
            + " is negative.",
        ):
            self.production_cluster.set_setpoints(setpoints=setpoints)
