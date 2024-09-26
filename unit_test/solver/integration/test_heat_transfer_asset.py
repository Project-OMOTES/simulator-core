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

from omotes_simulator_core.solver.network.assets.heat_transfer_asset import HeatTransferAsset
from omotes_simulator_core.solver.network.assets.production_asset import ProductionAsset
from omotes_simulator_core.solver.network.network import Network
from omotes_simulator_core.solver.solver import Solver
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


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

    def test_heat_transfer_asset_primary_positive_secondary_positive_flow(self) -> None:
        """Primary (index=0) positive and secondary (index=2) positive flow state.

        The primary side is defined as [0, 1] and the secondary side is defined as [2, 3].
        """
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
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[6], -38.76, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[2], fluid_props.get_ie(303.15), 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[8], fluid_props.get_ie(313.15), 2)

    def test_heat_transfer_asset_primary_negative_secondary_positive_flow(self) -> None:
        """Primary (index=0) negative and secondary (index=2) positive flow state.

        The primary side is defined as [0, 1] and the secondary side is defined as [2, 3].
        """
        # Arrange
        # Connect assets
        self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=1,
            asset2_id=self.production_asset.name,
            connection_point_2=1,
        )
        self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=0,
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
        self.heat_transfer_asset.primary_side_inflow = 1
        self.heat_transfer_asset.primary_side_outflow = 0
        self.heat_transfer_asset.secondary_side_inflow = 2
        self.heat_transfer_asset.secondary_side_outflow = 3
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
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[0], +77.59, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[6], -38.76, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[2], fluid_props.get_ie(293.15), 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[8], fluid_props.get_ie(313.15), 2)

    def test_heat_transfer_asset_primary_positive_secondary_negative_flow(self) -> None:
        """Primary (index=0) positive and secondary (index=2) negative flow state.

        The primary side is defined as [0, 1] and the secondary side is defined as [2, 3].
        """
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
            connection_point_2=0,
        )
        self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=3,
            asset2_id=self.demand_asset.name,
            connection_point_2=1,
        )
        # Create a Solver Object
        self.solver = Solver(network=self.network)
        # Set the temperatures and cop for HP
        self.heat_transfer_asset.supply_temperature_primary = 20 + 273.15
        self.heat_transfer_asset.supply_temperature_secondary = 70 + 273.15
        self.heat_transfer_asset.heat_transfer_coefficient = 1.0 - 1.0 / 3.0
        self.heat_transfer_asset.primary_side_inflow = 0
        self.heat_transfer_asset.primary_side_outflow = 1
        self.heat_transfer_asset.secondary_side_inflow = 3
        self.heat_transfer_asset.secondary_side_outflow = 2
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
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[6], +38.76, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[2], fluid_props.get_ie(303.15), 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[8], fluid_props.get_ie(343.15), 2)

    def test_heat_transfer_asset_positive_heat_transfer_coefficient(self) -> None:
        """Test a positive heat transfer coefficient.

        The primary side is defined as [0, 1] and the secondary side is defined as [2, 3].
        Primary (index=0) positive and secondary (index=2) positive flow state.
        """
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
        self.heat_transfer_asset.heat_transfer_coefficient = 1.0 - 1.0 / 5.0
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
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[0], -93.10, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[6], -38.76, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[2], fluid_props.get_ie(303.15), 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[8], fluid_props.get_ie(313.15), 2)

    def test_heat_transfer_asset_heat_transfer_coefficient_of_one(self) -> None:
        """Test a heat transfer coefficient equal to one.

        The primary side is defined as [0, 1] and the secondary side is defined as [2, 3].
        Primary (index=0) positive and secondary (index=2) positive flow state.
        """
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
        self.heat_transfer_asset.supply_temperature_primary = 70 + 273.15
        self.heat_transfer_asset.supply_temperature_secondary = 70 + 273.15
        self.heat_transfer_asset.heat_transfer_coefficient = 1.0  # - 1.0 / 5.0
        # Set the temperature of the demand
        self.demand_asset.supply_temperature = 40 + 273.15
        self.demand_asset.mass_flow_rate_set_point = 38.76
        self.demand_asset.pre_scribe_mass_flow = True
        # Set the temperature of the production
        self.production_asset.pre_scribe_mass_flow = False
        self.production_asset.supply_temperature = 40 + 273.15
        # Act
        self.solver.solve()
        # Assert
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[0], -38.76, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[6], -38.76, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[2], fluid_props.get_ie(313.15), 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[8], fluid_props.get_ie(313.15), 2)

    def test_heat_transfer_asset_negative_heat_transfer_coefficient(self) -> None:
        """Test a negative heat transfer coefficient.

        The primary side is defined as [0, 1] and the secondary side is defined as [2, 3].
        Primary (index=0) positive and secondary (index=2) positive flow state.
        """
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
        self.heat_transfer_asset.supply_temperature_primary = 30 + 273.15
        self.heat_transfer_asset.supply_temperature_secondary = 40 + 273.15
        self.heat_transfer_asset.heat_transfer_coefficient = -1 * (1.0 - 1.0 / 5.0)
        # Set the temperature of the demand
        self.demand_asset.supply_temperature = 70 + 273.15
        self.demand_asset.mass_flow_rate_set_point = 38.76
        self.demand_asset.pre_scribe_mass_flow = True
        # Set the temperature of the production
        self.production_asset.pre_scribe_mass_flow = False
        self.production_asset.supply_temperature = 20 + 273.15
        # Act
        self.solver.solve()
        # Assert
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[0], -93.10, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[6], -38.76, 2)
        # u_0 < u_1 on the primary side
        self.assertTrue(self.heat_transfer_asset.prev_sol[2] < self.heat_transfer_asset.prev_sol[5])
        # u_2 > u_3 on the secondary side
        self.assertTrue(
            self.heat_transfer_asset.prev_sol[8] > self.heat_transfer_asset.prev_sol[11]
        )
        # verify temperature
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[2], fluid_props.get_ie(293.15), 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[8], fluid_props.get_ie(343.15), 2)
