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

from simulator_core.solver.network.assets.heat_transfer_asset import HeatTransferAsset
from simulator_core.solver.network.assets.production_asset import ProductionAsset
from simulator_core.solver.network.network import Network
from simulator_core.solver.solver import Solver
from simulator_core.solver.utils.fluid_properties import fluid_props


class HeatTransferAssetIntegrationTest(unittest.TestCase):
    """Testcase for HeatTransferAsset class."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Create a HeatPump object
        self.heat_transfer_asset = HeatTransferAsset(
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
        self.network.add_existing_asset(self.heat_transfer_asset)
        self.network.add_existing_asset(self.production_asset)
        self.network.add_existing_asset(self.demand_asset)

    def test_heat_transfer_asset_positive_flow(self) -> None:
        """Test the heat transfer asset for a positive flow state with [0, 1] as primary side."""
        # Arrange
        # Connect assets
        self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=0,
            asset2_id=self.production_asset.name,
            connection_point_2=1,
        )
        self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=1,
            asset2_id=self.production_asset.name,
            connection_point_2=0,
        )
        self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=2,
            asset2_id=self.demand_asset.name,
            connection_point_2=1,
        )
        self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=3,
            asset2_id=self.demand_asset.name,
            connection_point_2=0,
        )
        # Create a Solver Object
        self.solver = Solver(network=self.network)
        # Set the temperatures and cop for HP
        self.heat_transfer_asset.supply_temperature_primary = 20 + 273.15
        self.heat_transfer_asset.supply_temperature_secondary = 70 + 273.15
        self.heat_transfer_asset.heat_transfer_coefficient = 1.0 - 1.0 / 3.0
        # Set the temperature of the demand
        self.demand_asset.supply_temperature = 40 + 273.15
        self.demand_asset.mass_flow_rate_set_point = 38.76
        self.demand_asset.pre_scribe_mass_flow = True
        # Set the temperature of the production
        self.production_asset.pre_scribe_mass_flow = False
        self.production_asset.supply_temperature = 30 + 273.15
        # Act
        self.solver.solve()
        # Assert
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[0], -77.59, 2)
        self.assertEqual(self.heat_transfer_asset.prev_sol[2], fluid_props.get_ie(303.15))
        self.assertEqual(self.heat_transfer_asset.prev_sol[8], fluid_props.get_ie(313.15))

    def test_heat_transfer_asset_negative_flow(self) -> None:
        """Test the heat transfer asset for a positive flow state with [0, 1] as primary side."""
        # Arrange
        # Connect assets
        self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=1,
            asset2_id=self.production_asset.name,
            connection_point_2=0,
        )
        self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=0,
            asset2_id=self.production_asset.name,
            connection_point_2=1,
        )
        self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=2,
            asset2_id=self.demand_asset.name,
            connection_point_2=1,
        )
        self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=3,
            asset2_id=self.demand_asset.name,
            connection_point_2=0,
        )
        # Create a Solver Object
        self.solver = Solver(network=self.network)
        # Set the temperatures and cop for HP
        self.heat_transfer_asset.supply_temperature_primary = 20 + 273.15
        self.heat_transfer_asset.supply_temperature_secondary = 70 + 273.15
        self.heat_transfer_asset.heat_transfer_coefficient = 1.0 - 1.0 / 3.0
        # Set the temperature of the demand
        self.demand_asset.supply_temperature = 40 + 273.15
        self.demand_asset.mass_flow_rate_set_point = 38.76
        self.demand_asset.pre_scribe_mass_flow = True
        # Set the temperature of the production
        self.production_asset.pre_scribe_mass_flow = False
        self.production_asset.supply_temperature = 30 + 273.15
        # Act
        self.solver.solve()
        # Assert
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[0], 77.59, 2)
        self.assertEqual(self.heat_transfer_asset.prev_sol[2], fluid_props.get_ie(293.15))
        self.assertEqual(self.heat_transfer_asset.prev_sol[8], fluid_props.get_ie(303.15))
