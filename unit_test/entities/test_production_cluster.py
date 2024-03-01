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
    PROPERTY_MASSFLOW,
    PROPERTY_PRESSURE_RETURN,
    PROPERTY_PRESSURE_SUPPLY,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_RETURN,
    PROPERTY_TEMPERATURE_SUPPLY,
)
from simulator_core.entities.assets.junction import Junction
from simulator_core.entities.assets.production_cluster import ProductionCluster
from simulator_core.entities.assets.utils import (
    heat_demand_and_temperature_to_mass_flow,
)


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
            PROPERTY_TEMPERATURE_SUPPLY: 353.15,
            PROPERTY_TEMPERATURE_RETURN: 333.15,
            PROPERTY_SET_PRESSURE: False,
        }
        self.production_cluster.set_setpoints(setpoints=setpoints)

        # Act
        mass_flow = heat_demand_and_temperature_to_mass_flow(
            temperature_supply=setpoints[PROPERTY_TEMPERATURE_SUPPLY],
            temperature_return=setpoints[PROPERTY_TEMPERATURE_RETURN],
            thermal_demand=setpoints[PROPERTY_HEAT_DEMAND],
        )

        # Assert
        assert self.production_cluster.temperature_supply == 353.15
        assert self.production_cluster.temperature_return == 333.15
        assert self.production_cluster.controlled_mass_flow == mass_flow
        assert (
            self.production_cluster.solver_asset.mass_flow_rate_set_point
            == self.production_cluster.controlled_mass_flow
        )
        assert (
            self.production_cluster.solver_asset.pre_scribe_mass_flow
            is not setpoints[PROPERTY_SET_PRESSURE]
        )

    def test_production_cluster_set_setpoints_missing_setpoint(self) -> None:
        """Test raise ValueError with missing setpoint."""
        # Arrange
        necessary_setpoints = set(
            [PROPERTY_HEAT_DEMAND, PROPERTY_TEMPERATURE_SUPPLY, PROPERTY_TEMPERATURE_RETURN]
        )
        setpoints = {
            PROPERTY_TEMPERATURE_SUPPLY: 353.15,
            PROPERTY_TEMPERATURE_RETURN: 333.15,
            PROPERTY_SET_PRESSURE: False,
        }

        # Act
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
            PROPERTY_TEMPERATURE_SUPPLY: 353.15,
            PROPERTY_TEMPERATURE_RETURN: 333.15,
            PROPERTY_SET_PRESSURE: False,
        }

        # Act
        mass_flow = heat_demand_and_temperature_to_mass_flow(
            temperature_supply=setpoints[PROPERTY_TEMPERATURE_SUPPLY],
            temperature_return=setpoints[PROPERTY_TEMPERATURE_RETURN],
            thermal_demand=setpoints[PROPERTY_HEAT_DEMAND],
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

    def test_production_cluster_set_setpoints_pressure_or_mass_flow_control(self) -> None:
        """Test setting pressure setpoint of a production cluster."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: 1e6,
            PROPERTY_TEMPERATURE_SUPPLY: 353.15,
            PROPERTY_TEMPERATURE_RETURN: 333.15,
            PROPERTY_SET_PRESSURE: True,
        }

        # Act
        self.production_cluster.set_setpoints(setpoints=setpoints)

        # Assert
        assert self.production_cluster.control_mass_flow is not setpoints[PROPERTY_SET_PRESSURE]
        assert (
            self.production_cluster.solver_asset.pre_scribe_mass_flow
            is not setpoints[PROPERTY_SET_PRESSURE]
        )

    def test_production_cluster_set_pressure_supply(self) -> None:
        """Test setting pressure of a production cluster."""
        # Arrange
        pressure_supply = 2e5  # [Pa]

        # Act
        self.production_cluster.set_pressure_supply(pressure_supply=pressure_supply)

        # Assert
        assert self.production_cluster.pressure_supply == pressure_supply
        assert self.production_cluster.solver_asset.set_pressure == pressure_supply

    def test_production_cluster_set_pressure_supply_negative(self) -> None:
        """Test raise ValueError with negative pressure."""
        # Arrange
        pressure_supply = -2e5  # [Pa]

        # Act
        with self.assertRaises(ValueError) as cm:
            self.production_cluster.set_pressure_supply(pressure_supply=pressure_supply)

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            cm.exception.args[0],
            f"The pressure {pressure_supply} of the asset {self.production_cluster.name}"
            + " can not be negative.",
        )

    def test_production_cluster_write_to_output(self) -> None:
        """Test writing the output of a production cluster."""
        # Arrange
        self.production_cluster.solver_asset.get_mass_flow_rate = Mock(return_value=1e6)
        self.production_cluster.solver_asset.get_pressure = Mock(return_value=2e5)
        self.production_cluster.solver_asset.get_temperature = Mock(return_value=333.15)

        # Act
        self.production_cluster.write_to_output()

        # Assert
        assert len(self.production_cluster.output) == 1
        assert self.production_cluster.output[0] == {
            PROPERTY_TEMPERATURE_SUPPLY: 333.15,
            PROPERTY_TEMPERATURE_RETURN: 333.15,
            PROPERTY_MASSFLOW: 1e6,
            PROPERTY_PRESSURE_SUPPLY: 2e5,
            PROPERTY_PRESSURE_RETURN: 2e5,
        }
