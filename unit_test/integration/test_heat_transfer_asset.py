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
from omotes_simulator_core.solver.network.assets.production_asset import HeatBoundary
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
        self.production_asset = HeatBoundary(
            name=str(uuid4()),
            _id=str(uuid4()),
        )
        # Create DemandAsset object
        self.demand_asset = HeatBoundary(
            name=str(uuid4()),
            _id=str(uuid4()),
        )
        # Create a Network object
        self.network = Network()
        # Add assets to the network
        self.network.add_existing_asset(self.heat_transfer_asset)
        self.network.add_existing_asset(self.production_asset)
        self.network.add_existing_asset(self.demand_asset)
    
    def _get_matrix_idx_mass_flow_ie(self):
        
        idx_dict = {
            "mass_flow_0" : 0,
            "mass_flow_1" : 0,
            "mass_flow_2" : 0,
            "mass_flow_3" : 0,
            "internal_energy_0" : 0,
            "internal_energy_1" : 0,
            "internal_energy_2" : 0,
            "internal_energy_3" : 0
        }

        idx_dict["mass_flow_0"] = self.heat_transfer_asset.get_index_matrix(
            property_name="mass_flow_rate",
            connection_point=0,
            use_relative_indexing=False
        )
        idx_dict["mass_flow_1"] = self.heat_transfer_asset.get_index_matrix(
            property_name="mass_flow_rate",
            connection_point=1,
            use_relative_indexing=False
        )
        idx_dict["mass_flow_2"] = self.heat_transfer_asset.get_index_matrix(
            property_name="mass_flow_rate",
            connection_point=2,
            use_relative_indexing=False
        )
        idx_dict["mass_flow_3"] = self.heat_transfer_asset.get_index_matrix(
            property_name="mass_flow_rate",
            connection_point=3,
            use_relative_indexing=False
        )
        idx_dict["internal_energy_0"] = self.heat_transfer_asset.get_index_matrix(
            property_name="internal_energy",
            connection_point=0,
            use_relative_indexing=False
        )
        idx_dict["internal_energy_1"] = self.heat_transfer_asset.get_index_matrix(
            property_name="internal_energy",
            connection_point=1,
            use_relative_indexing=False
        )
        idx_dict["internal_energy_2"] = self.heat_transfer_asset.get_index_matrix(
            property_name="internal_energy",
            connection_point=2,
            use_relative_indexing=False
        )
        idx_dict["internal_energy_3"] = self.heat_transfer_asset.get_index_matrix(
            property_name="internal_energy",
            connection_point=3,
            use_relative_indexing=False
        )

        return idx_dict
    
    def _compute_primary_massflow(self, c, m_dot_2, m_dot_3, u_2, u_3, u_0, u_1):

        m_0 =  -c * (m_dot_2 * u_2 - m_dot_3 * u_3) / (u_0 - u_1)
        
        return m_0

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
        matrix_idx = self._get_matrix_idx_mass_flow_ie()
        
        c = self.heat_transfer_asset.heat_transfer_coefficient
        m2 = -self.demand_asset.mass_flow_rate_set_point
        u2 = fluid_props.get_ie(self.demand_asset.supply_temperature)
        m3 = m2
        u3 = fluid_props.get_ie(self.heat_transfer_asset.supply_temperature_secondary)
        u0 = fluid_props.get_ie(self.production_asset.supply_temperature)
        u1 = fluid_props.get_ie(self.heat_transfer_asset.supply_temperature_primary)
        m0 = self._compute_primary_massflow(c, m2, m3, u2, u3, u0, u1)

        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["mass_flow_0"]], m0, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["mass_flow_2"]], m2, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["internal_energy_0"]], fluid_props.get_ie(303.15), 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["internal_energy_2"]], fluid_props.get_ie(313.15), 2)

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
        matrix_idx = self._get_matrix_idx_mass_flow_ie()

        c = self.heat_transfer_asset.heat_transfer_coefficient
        m2 = self.demand_asset.mass_flow_rate_set_point
        u2 = fluid_props.get_ie(self.demand_asset.supply_temperature)
        m3 = m2
        u3 = fluid_props.get_ie(self.heat_transfer_asset.supply_temperature_secondary)
        u0 = fluid_props.get_ie(self.production_asset.supply_temperature)
        u1 = fluid_props.get_ie(self.heat_transfer_asset.supply_temperature_primary)
        m0 = self._compute_primary_massflow(c, m2, m3, u2, u3, u0, u1)

        #self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["mass_flow_0"]], +77.59, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["mass_flow_2"]], -38.76, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["internal_energy_0"]], fluid_props.get_ie(293.15), 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["internal_energy_2"]], fluid_props.get_ie(313.15), 2)

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
        # This probably fails because the internal energy was computed using a way that is no longer used in the solver.
        # TODO: add missing tests: zero flow for example or more.
        c = self.heat_transfer_asset.heat_transfer_coefficient
        m2 = -self.demand_asset.mass_flow_rate_set_point
        u2 = fluid_props.get_ie(self.demand_asset.supply_temperature)
        m3 = m2
        u3 = fluid_props.get_ie(self.heat_transfer_asset.supply_temperature_secondary)
        u0 = fluid_props.get_ie(self.production_asset.supply_temperature)
        u1 = fluid_props.get_ie(self.heat_transfer_asset.supply_temperature_primary)
        
        # Assert
        matrix_idx = self._get_matrix_idx_mass_flow_ie()
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["mass_flow_0"]], -77.59, 2) # mass flow at connection point 0
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["mass_flow_2"]], +38.76, 2) # mass flow at connection point 2
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["internal_energy_0"]], fluid_props.get_ie(303.15), 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["internal_energy_2"]], fluid_props.get_ie(343.15), 2)

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
        matrix_idx = self._get_matrix_idx_mass_flow_ie()
        #self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["mass_flow_0"]], -93.10, 2)
        #self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["mass_flow_2"]], -38.76, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["internal_energy_0"]], fluid_props.get_ie(303.15), 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["internal_energy_2"]], fluid_props.get_ie(313.15), 2)

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
        matrix_idx = self._get_matrix_idx_mass_flow_ie()
        #self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["mass_flow_0"]], -38.76, 2)
        #self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["mass_flow_2"]], -38.76, 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["internal_energy_0"]], fluid_props.get_ie(313.15), 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["internal_energy_2"]], fluid_props.get_ie(313.15), 2)
        
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
        matrix_idx = self._get_matrix_idx_mass_flow_ie()
        #self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["mass_flow_0"]], -93.10, 2)
        #self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["mass_flow_2"]], -38.76, 2)
        # u_0 < u_1 on the primary side
        self.assertTrue(self.heat_transfer_asset.prev_sol[matrix_idx["internal_energy_0"]] < self.heat_transfer_asset.prev_sol[5])
        # u_2 > u_3 on the secondary side
        self.assertTrue(
            self.heat_transfer_asset.prev_sol[matrix_idx["internal_energy_2"]] > self.heat_transfer_asset.prev_sol[11]
        )
        # verify temperature
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["internal_energy_0"]], fluid_props.get_ie(293.15), 2)
        self.assertAlmostEqual(self.heat_transfer_asset.prev_sol[matrix_idx["internal_energy_2"]], fluid_props.get_ie(343.15), 2)

if __name__=="__main__":
    heat_transfer_test = HeatTransferAssetIntegrationTest()
    heat_transfer_test.setUp()
    heat_transfer_test.test_heat_transfer_asset_primary_positive_secondary_positive_flow()
    #heat_transfer_test.test_heat_transfer_asset_primary_negative_secondary_positive_flow()
    #heat_transfer_test.test_heat_transfer_asset_primary_positive_secondary_negative_flow()
    #heat_transfer_test.test_heat_transfer_asset_positive_heat_transfer_coefficient()
    #heat_transfer_test.test_heat_transfer_asset_heat_transfer_coefficient_of_one()
    #heat_transfer_test.test_heat_transfer_asset_negative_heat_transfer_coefficient()