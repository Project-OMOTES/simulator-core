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

"""Test Heat Pump Solver Asset."""
import unittest
from uuid import uuid4

import numpy.testing as npt

from simulator_core.solver.matrix.core_enum import NUMBER_CORE_QUANTITIES, IndexEnum
from simulator_core.solver.matrix.matrix import Matrix
from simulator_core.solver.network.assets.heat_pump import HeatPumpAsset
from simulator_core.solver.network.assets.node import Node
from simulator_core.solver.network.assets.production_asset import ProductionAsset
from simulator_core.solver.network.network import Network
from simulator_core.solver.solver import Solver
from simulator_core.solver.utils.fluid_properties import fluid_props


class HeatPumpIntegrationTest(unittest.TestCase):
    """Testcase for HeatPumpAsset class."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Create a HeatPump object
        self.heatpump_asset = HeatPumpAsset(
            name=str(uuid4()),
            _id=str(uuid4()),
        )
        # Create ProductionAsset object
        self.production_asset = ProductionAsset(
            name=str(uuid4()),
            _id=str(uuid4()),
        )
        # Create DemandAsset object
        self.demand_asset = ProductionAsset(
            name=str(uuid4()),
            _id=str(uuid4()),
        )
        # Create a Network object
        self.network = Network()
        # Add assets to the network
        self.network.add_existing_asset(self.heatpump_asset)
        self.network.add_existing_asset(self.production_asset)
        self.network.add_existing_asset(self.demand_asset)
        # Connect assets
        self.network.connect_assets(
            asset1_id=self.heatpump_asset.name,
            connection_point_1=0,
            asset2_id=self.production_asset.name,
            connection_point_2=1,
        )
        self.network.connect_assets(
            asset1_id=self.heatpump_asset.name,
            connection_point_1=1,
            asset2_id=self.production_asset.name,
            connection_point_2=0,
        )
        self.network.connect_assets(
            asset1_id=self.heatpump_asset.name,
            connection_point_1=2,
            asset2_id=self.demand_asset.name,
            connection_point_2=1,
        )
        self.network.connect_assets(
            asset1_id=self.heatpump_asset.name,
            connection_point_1=3,
            asset2_id=self.demand_asset.name,
            connection_point_2=0,
        )
        # Create a Solver Object
        self.solver = Solver(network=self.network)

    def test_heat_pump_positive_flow(self) -> None:
        """Test the heat pump equations for a positive flow state."""
        # Arrange
        self.production_asset.pre_scribe_mass_flow = False
        # Set the temperatures and cop for HP
        self.heatpump_asset.supply_temperature_primary = 20 + 273.15
        self.heatpump_asset.supply_temperature_secondary = 70 + 273.15
        self.heatpump_asset.cop_h = 3.0
        self.heatpump_asset._cop_heat_pump = 1 - 1 / self.heatpump_asset.cop_h
        self.heatpump_asset.pre_scribe_mass_flow = False
        self.heatpump_asset.mass_flow_rate_set_point = 85.15
        # Set the temperature of the demand
        self.demand_asset.supply_temperature = 40 + 273.15
        self.demand_asset.mass_flow_rate_set_point = 38.76
        self.demand_asset.pre_scribe_mass_flow = True
        # Set the temperature of the production
        self.production_asset.supply_temperature = 30 + 273.15
        # Act
        self.solver.solve()
        # Assert
        self.assertAlmostEqual(abs(self.heatpump_asset.prev_sol[0]), 77.59, 2)
        self.assertAlmostEqual(self.heatpump_asset.prev_sol[2], 125699.50, 2)
        self.assertAlmostEqual(self.heatpump_asset.prev_sol[8], 167482.00, 2)

    def test_heat_pump_negative_flow(self) -> None:
        """Test the heat pump equations for a negative flow state."""
        # Arrange
        self.heatpump_asset.pre_scribe_mass_flow = False
        self.demand_asset.pre_scribe_mass_flow = False
        # Set the temperatures and cop for HP
        self.heatpump_asset.supply_temperature_primary = 70 + 273.15
        self.heatpump_asset.supply_temperature_secondary = 20 + 273.15
        self.heatpump_asset.cop_h = 3.0
        # Set the temperature of the demand
        self.production_asset.supply_temperature = 40 + 273.15
        self.production_asset.mass_flow_rate_set_point = 38.76
        self.production_asset.pre_scribe_mass_flow = True
        # Set the temperature of the production
        self.demand_asset.supply_temperature = 30 + 273.15
        # Act
        self.solver.solve(
            filename=r"c:\Users\meerkerk\OneDrive - Stichting Deltares\Desktop\matrix_dump.csv"
        )
        # Assert
        self.assertAlmostEqual(abs(self.heatpump_asset.prev_sol[6]), 85.15, 2)
        self.assertAlmostEqual(self.heatpump_asset.prev_sol[8], 125699.50, 2)
        self.assertAlmostEqual(self.heatpump_asset.prev_sol[2], 167482.00, 2)

    def test_heat_pump_cop_higher(self) -> None:
        """Test the heat pump equations for a higher COP in a positive flow state."""
        # Arrange
        self.heatpump_asset.pre_scribe_mass_flow = False
        self.production_asset.pre_scribe_mass_flow = False
        # Set the temperatures and cop for HP
        self.heatpump_asset.supply_temperature_primary = 20 + 273.15
        self.heatpump_asset.supply_temperature_secondary = 70 + 273.15
        self.heatpump_asset.cop_h = 6.0
        # Set the temperature of the demand
        self.demand_asset.supply_temperature = 40 + 273.15
        self.demand_asset.mass_flow_rate_set_point = 38.76
        self.demand_asset.pre_scribe_mass_flow = True
        # Set the temperature of the production
        self.production_asset.supply_temperature = 30 + 273.15
        # Act
        self.solver.solve()
        # Assert
        self.assertAlmostEqual(abs(self.heatpump_asset.prev_sol[0]), 85.15, 2)
        self.assertAlmostEqual(self.heatpump_asset.prev_sol[2], 125699.50, 2)
        self.assertAlmostEqual(self.heatpump_asset.prev_sol[8], 167482.00, 2)


# TODO: COP variation test
# TODO: Flow direction reversal test; what does it mean?
