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
from unittest.mock import Mock, patch

from scipy.constants import g

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
        self.assertAlmostEqual(self.ates_cluster.hot_well_temperature, 358.66, delta=0.1)
        self.assertAlmostEqual(self.ates_cluster.cold_well_temperature, 290.155, delta=0.1)

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
            self.ates_cluster.solver_asset.mass_flow_rate_set_point,
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
        self.assertAlmostEqual(self.ates_cluster.hot_well_temperature, 290.15, delta=0.1)
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
            self.ates_cluster.solver_asset.mass_flow_rate_set_point,
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
            min(
                ATES_DEFAULTS.maximum_flow_charge,
                self.ates_cluster._get_max_flowrate_extraction_norm(
                    self.ates_cluster._get_saline_density(101325, 333.15) * g * self.aquifer_depth,
                    self.ates_cluster.cold_well_temperature,
                ),
            )
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


class AtesClusterNvoeTest(unittest.TestCase):
    """Test sand-production restrictions independently of the Java aquifer model."""

    def setUp(self) -> None:
        """Create an ATES without initializing ROSIM."""
        with (
            patch.object(AtesCluster, "_init_rosim"),
            patch("omotes_simulator_core.entities.assets.ates_cluster.PyjniusLoader.get_loader"),
        ):
            self.asset = AtesCluster(
                asset_name="ates",
                asset_id="ates_id",
                port_ids=["hot", "cold"],
                aquifer_depth=300.0,
                aquifer_thickness=45.0,
                aquifer_mid_temperature=17.0,
                aquifer_net_to_gross=1.0,
                aquifer_porosity=0.3,
                aquifer_permeability=10000.0,
                aquifer_anisotropy=4.0,
                salinity=10000.0,
                well_casing_size=13.0,
                well_distance=150.0,
                hot_well_temperature=358.15,
                cold_well_temperature=308.15,
            )

    def test_saline_properties(self) -> None:
        """Retain the legacy saline correlations with Pa and K inputs."""
        self.assertAlmostEqual(self.asset._get_saline_density(1e7, 323.15), 998.98665)
        self.assertAlmostEqual(
            self.asset._get_saline_viscosity(323.15), 0.0005853902867162903, places=12
        )

    def test_extraction_norm_units_and_depth_factor(self) -> None:
        """Convert casing inches and permeability mD before applying the depth factor."""
        with (
            patch.object(self.asset, "_get_saline_density", return_value=1000.0),
            patch.object(self.asset, "_get_saline_viscosity", return_value=0.001),
        ):
            expected_flow = (
                3.141592653589793
                * (13.0 * 0.0254)
                * 45.0
                * (2 * 3600 * 10000.0 * 9.8692326671601e-16 * 1000.0 * g / 0.001)
                * 3.0
            )
            self.assertAlmostEqual(
                self.asset._get_max_flowrate_extraction_norm(1e7, 323.15), expected_flow
            )

    def test_producing_well_limits_both_modes(self) -> None:
        """Use the cold well during charging and the hot well during discharging."""
        for charging, temperature in [(True, 308.15), (False, 358.15)]:
            with (
                self.subTest(charging=charging),
                patch.object(self.asset, "_get_saline_density", return_value=1000.0),
                patch.object(
                    self.asset, "_get_max_flowrate_extraction_norm", return_value=40.0
                ) as extraction_norm,
            ):
                self.asset.charging = charging
                maximum_mass_flow = self.asset._get_maximum_mass_flow_rate()
                extraction_norm.assert_called_once_with(1000.0 * g * 300.0, temperature)
                self.assertAlmostEqual(
                    maximum_mass_flow, 40.0 / 3600 * fluid_props.get_density(333.15)
                )

    def test_existing_capacity_remains_an_upper_bound(self) -> None:
        """The NVOE restriction never raises either existing capacity cap."""
        for charging, volume_flow in [
            (True, ATES_DEFAULTS.maximum_flow_charge),
            (False, ATES_DEFAULTS.maximum_flow_discharge),
        ]:
            with (
                self.subTest(charging=charging),
                patch.object(self.asset, "_get_max_flowrate_extraction_norm", return_value=1e6),
            ):
                self.asset.charging = charging
                self.assertAlmostEqual(
                    self.asset._get_maximum_mass_flow_rate(),
                    volume_flow / 3600 * fluid_props.get_density(333.15),
                )

    def test_limited_flow_reaches_solver_and_rosim(self) -> None:
        """Limit flow before passing it to either model and reduce the thermal allocation."""
        for charging in [True, False]:
            with (
                self.subTest(charging=charging),
                patch.object(self.asset, "_get_max_flowrate_extraction_norm", return_value=40.0),
            ):
                self.asset.first_time_step = True
                self.asset.rosim = Mock()
                self.asset.rosim.calcTimeStepAndGetTemps.return_value = [85.0, 35.0]
                self.asset.set_time(datetime(2024, 1, 1 if charging else 2))
                self.asset.set_time_step(3600)
                self.asset.set_setpoints(
                    {
                        PROPERTY_HEAT_DEMAND: 1e9 if charging else -1e9,
                        PROPERTY_TEMPERATURE_IN: 358.15 if charging else 308.15,
                        PROPERTY_TEMPERATURE_OUT: 308.15 if charging else 358.15,
                        PROPERTY_SET_PRESSURE: False,
                    }
                )
                expected_mass_flow = 40.0 / 3600 * fluid_props.get_density(333.15)
                if not charging:
                    expected_mass_flow *= -1
                self.assertAlmostEqual(self.asset.mass_flowrate, expected_mass_flow)
                self.assertAlmostEqual(
                    self.asset.solver_asset.mass_flow_rate_set_point, expected_mass_flow
                )
                self.assertLess(abs(self.asset.thermal_power_allocation), 1e9)
                self.assertGreater(self.asset.thermal_power_allocation * expected_mass_flow, 0.0)
                volume_flow = expected_mass_flow * 3600 / 1027
                self.asset.rosim.calcTimeStepAndGetTemps.assert_called_once_with(
                    [volume_flow, -volume_flow],
                    [85.0, -1] if charging else [-1, 35.0],
                    1.0,
                )

    def test_extraction_limit_tracks_well_temperature(self) -> None:
        """Warmer water has a higher extraction limit through reduced viscosity."""
        cold_limit = self.asset._get_max_flowrate_extraction_norm(1e7, 308.15)
        hot_limit = self.asset._get_max_flowrate_extraction_norm(1e7, 358.15)
        self.assertGreater(hot_limit, cold_limit)

    def test_zero_permeability_stops_flow(self) -> None:
        """An impermeable aquifer cannot exchange flow or thermal power."""
        self.asset.aquifer_permeability = 0.0
        self.asset.thermal_power_allocation = 1e6
        self.asset._calculate_massflowrate()
        self.assertEqual(self.asset.mass_flowrate, 0.0)
        self.assertEqual(self.asset.thermal_power_allocation, 0.0)
