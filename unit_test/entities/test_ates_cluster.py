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
    PROPERTY_HEAT_DEMAND,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
)
from omotes_simulator_core.entities.assets.ates_cluster import AtesCluster


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
        }

        # Act
        self.ates_cluster.set_time_step(3600 * 24 * 7)
        self.ates_cluster.first_time_step = True  # dont get temperature from solver
        self.ates_cluster.set_time(datetime(2023, 1, 1, 0, 0, 0))
        self.ates_cluster.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertAlmostEqual(self.ates_cluster.hot_well_temperature, 358.15, delta=0.1)
        self.assertAlmostEqual(self.ates_cluster.cold_well_temperature, 290.15, delta=0.1)

    def test_production_ates(self) -> None:
        """Test production to ATES."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: -1e6,
            PROPERTY_TEMPERATURE_OUT: 35 + 273.15,
            PROPERTY_TEMPERATURE_IN: 85 + 273.15,
        }

        # Act
        self.ates_cluster.set_time_step(3600 * 24 * 7)
        self.ates_cluster.first_time_step = True  # dont get temperature from solver
        self.ates_cluster.set_time(datetime(2023, 2, 1, 0, 0, 0))
        self.ates_cluster.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertAlmostEqual(self.ates_cluster.hot_well_temperature, 355.54, delta=0.1)
        self.assertAlmostEqual(self.ates_cluster.cold_well_temperature, 308.17, delta=0.1)
