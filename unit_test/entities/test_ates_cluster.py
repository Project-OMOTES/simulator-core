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
from datetime import datetime

from omotes_simulator_core.entities.assets.asset_defaults import (
    ATES_DEFAULTS,
    PROPERTY_COLD_WELL_TEMPERATURE,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_HOT_WELL_TEMPERATURE,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
    PROPERTY_TIMESTEP,
)
from omotes_simulator_core.entities.assets.ates_cluster import AtesCluster
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


class AtesClusterTest(unittest.TestCase):
    """Testcase for AtesCluster class."""

    def setUp(self) -> None:
        """Set up for the test case."""
        self.aquifer_depth = ATES_DEFAULTS.aquifer_depth
        self.aquifer_thickness = ATES_DEFAULTS.aquifer_thickness
        self.aquifer_mid_temperature = ATES_DEFAULTS.aquifer_mid_temperature
        self.aquifer_net_to_gross = ATES_DEFAULTS.aquifer_net_to_gross
        self.aquifer_porosity = ATES_DEFAULTS.aquifer_porosity
        self.aquifer_permeability = ATES_DEFAULTS.aquifer_permeability
        self.aquifer_anisotropy = ATES_DEFAULTS.aquifer_anisotropy
        self.salinity = ATES_DEFAULTS.salinity
        self.well_casing_size = ATES_DEFAULTS.well_casing_size
        self.well_distance = ATES_DEFAULTS.well_distance
        # Create a production cluster object
        self.ates_cluster = AtesCluster(
            asset_name="ates_cluster",
            asset_id="ates_cluster_id",
            port_ids=["test1", "test2"],
            aquifer_depth=self.aquifer_depth,
            aquifer_thickness=self.aquifer_thickness,
            aquifer_mid_temperature=self.aquifer_mid_temperature,
            aquifer_net_to_gross=self.aquifer_net_to_gross,
            aquifer_porosity=self.aquifer_porosity,
            aquifer_permeability=self.aquifer_permeability,
            aquifer_anisotropy=self.aquifer_anisotropy,
            salinity=self.salinity,
            well_casing_size=self.well_casing_size,
            well_distance=self.well_distance,
        )

    def test_injection_ates(self) -> None:
        """Test injection to ATES."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: 1e6,
            PROPERTY_TEMPERATURE_OUT: 35 + 273.15,
            PROPERTY_TEMPERATURE_IN: 85 + 273.15,
            PROPERTY_SET_PRESSURE: False,
        }

        # Act
        self.ates_cluster.set_time_step(3600 * 24 * 7)
        self.ates_cluster.first_time_step = True  # dont get temperature from solver
        self.ates_cluster.set_time(datetime(2023, 1, 1, 0, 0, 0))
        self.ates_cluster.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertAlmostEqual(self.ates_cluster.hot_well_temperature, 358.15, delta=0.1)
        self.assertAlmostEqual(self.ates_cluster.cold_well_temperature, 290.15, delta=0.1)

    def test_injection_ates_sign_conventions(self) -> None:
        """Test the sign and temperature conventions of a charging ATES."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: 1e6,
            PROPERTY_TEMPERATURE_OUT: 35 + 273.15,
            PROPERTY_TEMPERATURE_IN: 85 + 273.15,
            PROPERTY_SET_PRESSURE: False,
        }

        # Act
        self.ates_cluster.set_time_step(3600 * 24 * 7)
        self.ates_cluster.first_time_step = True  # dont get temperature from solver
        self.ates_cluster.set_time(datetime(2023, 1, 1, 0, 0, 0))
        self.ates_cluster.set_setpoints(setpoints=setpoints)

        # Assert
        # Charging: connection point 0 is the supply (hot) side and the inflow of the asset.
        self.assertEqual(self.ates_cluster.thermal_power_allocation, 1e6)
        self.assertEqual(self.ates_cluster.temperature_connection_0, 85 + 273.15)
        self.assertEqual(self.ates_cluster.temperature_connection_1, 35 + 273.15)
        # Charging: flow from connection point 0 to 1, so a positive mass flow rate set point.
        self.assertGreater(self.ates_cluster.mass_flowrate, 0.0)
        self.assertEqual(
            self.ates_cluster.solver_asset.mass_flow_rate_set_point,  # type: ignore
            self.ates_cluster.mass_flowrate,
        )
        # Charging: the flow leaves the asset at connection point 1 at the cold well temperature.
        self.assertEqual(
            self.ates_cluster.solver_asset.supply_temperature,
            self.ates_cluster.cold_well_temperature,
        )

    def test_production_ates(self) -> None:
        """Test production to ATES."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: -1e6,
            PROPERTY_TEMPERATURE_OUT: 85 + 273.15,
            PROPERTY_TEMPERATURE_IN: 35 + 273.15,
            PROPERTY_SET_PRESSURE: False,
        }

        # Act
        self.ates_cluster.set_time_step(3600 * 24 * 7)
        self.ates_cluster.first_time_step = True  # dont get temperature from solver
        self.ates_cluster.set_time(datetime(2023, 2, 1, 0, 0, 0))
        self.ates_cluster.set_setpoints(setpoints=setpoints)

        # Assert
        # The hot well is produced, so it cools down slightly with respect to the charged state.
        self.assertAlmostEqual(self.ates_cluster.hot_well_temperature, 355.54, delta=0.1)
        # The cold well is injected with the return temperature of the network.
        self.assertAlmostEqual(self.ates_cluster.cold_well_temperature, 308.17, delta=0.1)

    def test_production_ates_sign_conventions(self) -> None:
        """Test the sign and temperature conventions of a discharging ATES."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: -1e6,
            PROPERTY_TEMPERATURE_OUT: 85 + 273.15,
            PROPERTY_TEMPERATURE_IN: 35 + 273.15,
            PROPERTY_SET_PRESSURE: False,
        }

        # Act
        self.ates_cluster.set_time_step(3600 * 24 * 7)
        self.ates_cluster.first_time_step = True  # dont get temperature from solver
        self.ates_cluster.set_time(datetime(2023, 2, 1, 0, 0, 0))
        self.ates_cluster.set_setpoints(setpoints=setpoints)

        # Assert
        # Discharging: connection point 0 is the supply (hot) side and the outflow of the asset.
        self.assertEqual(self.ates_cluster.thermal_power_allocation, -1e6)
        self.assertEqual(self.ates_cluster.temperature_connection_0, 85 + 273.15)
        self.assertEqual(self.ates_cluster.temperature_connection_1, 35 + 273.15)
        # Discharging: flow from connection point 1 to 0, so a negative mass flow rate set point.
        self.assertLess(self.ates_cluster.mass_flowrate, 0.0)
        self.assertEqual(
            self.ates_cluster.solver_asset.mass_flow_rate_set_point,  # type: ignore
            self.ates_cluster.mass_flowrate,
        )
        # Discharging: the flow leaves the asset at connection point 0 at the hot well temperature.
        self.assertEqual(
            self.ates_cluster.solver_asset.supply_temperature,
            self.ates_cluster.hot_well_temperature,
        )

    def test_zero_temperature_difference(self) -> None:
        """Test that a negligible temperature difference results in a zero mass flow rate."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: 1e6,
            PROPERTY_TEMPERATURE_OUT: 85 + 273.15,
            PROPERTY_TEMPERATURE_IN: 85 + 273.15,
            PROPERTY_SET_PRESSURE: False,
        }

        # Act
        self.ates_cluster.set_time_step(3600 * 24 * 7)
        self.ates_cluster.first_time_step = True  # dont get temperature from solver
        self.ates_cluster.set_time(datetime(2023, 3, 1, 0, 0, 0))
        self.ates_cluster.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertEqual(self.ates_cluster.mass_flowrate, 0.0)

    def test_get_state(self) -> None:
        """Test that the asset reports the well temperatures to the controller."""
        # Act
        state = self.ates_cluster.get_state()

        # Assert
        self.assertEqual(
            state[PROPERTY_HOT_WELL_TEMPERATURE], self.ates_cluster.hot_well_temperature
        )
        self.assertEqual(
            state[PROPERTY_COLD_WELL_TEMPERATURE], self.ates_cluster.cold_well_temperature
        )
        self.assertEqual(state[PROPERTY_TIMESTEP], self.ates_cluster.time_step)

    def test_mass_flow_rate_is_limited(self) -> None:
        """Test that the mass flow rate is limited to the capacity of the wells."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: 1e9,  # far more than the wells can handle
            PROPERTY_TEMPERATURE_OUT: 35 + 273.15,
            PROPERTY_TEMPERATURE_IN: 85 + 273.15,
            PROPERTY_SET_PRESSURE: False,
        }
        maximum_mass_flow_rate = (
            ATES_DEFAULTS.maximum_flow_charge
            / 3600
            * fluid_props.get_density((85 + 273.15 + 35 + 273.15) / 2)
        )

        # Act
        self.ates_cluster.set_time_step(3600 * 24 * 7)
        self.ates_cluster.first_time_step = True  # dont get temperature from solver
        self.ates_cluster.set_time(datetime(2023, 4, 1, 0, 0, 0))
        self.ates_cluster.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertAlmostEqual(self.ates_cluster.mass_flowrate, maximum_mass_flow_rate)
        # The thermal power allocation is reduced to the power the asset can exchange.
        self.assertLess(self.ates_cluster.thermal_power_allocation, 1e9)
        self.assertGreater(self.ates_cluster.thermal_power_allocation, 0.0)
