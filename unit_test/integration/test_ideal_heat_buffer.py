#  Copyright (c) 2025. Deltares & TNO
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

from omotes_simulator_core.solver.network.assets.buffer_asset import HeatBufferAsset
from omotes_simulator_core.solver.network.assets.production_asset import HeatBoundary
from omotes_simulator_core.solver.network.network import Network
from omotes_simulator_core.solver.solver import Solver
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


class HeatBufferAssetIntegrationTest(unittest.TestCase):
    """Testcase for HeatBufferAsset class."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Create a HeatBuffer object
        self.heat_buffer_asset = HeatBufferAsset(
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
        self.network.add_existing_asset(self.heat_buffer_asset)
        self.network.add_existing_asset(self.production_asset)
        self.network.add_existing_asset(self.demand_asset)

        # Connect assets in the network
        # - Production -> Heat Buffer
        node_hot = self.network.connect_assets(
            asset1_id=self.production_asset.name,
            connection_point_1=1,
            asset2_id=self.heat_buffer_asset.name,
            connection_point_2=0,
        )
        # - Production -> Demand
        self.network.connect_assets(
            asset1_id=self.production_asset.name,
            connection_point_1=1,
            asset2_id=self.demand_asset.name,
            connection_point_2=0,
        )
        # - Heat buffer -> Production
        node_cold = self.network.connect_assets(
            asset1_id=self.production_asset.name,
            connection_point_1=0,
            asset2_id=self.heat_buffer_asset.name,
            connection_point_2=1,
        )
        # - Demand -> Production
        self.network.connect_assets(
            asset1_id=self.demand_asset.name,
            connection_point_1=1,
            asset2_id=self.production_asset.name,
            connection_point_2=0,
        )

        # Set temperature of nodes
        self.temperature_hot = 70.0 + 273.15  # K
        self.temperature_cold = 40.0 + 273.15  # K
        self.network.get_node(node_hot).initial_temperature = self.temperature_hot
        self.network.get_node(node_cold).initial_temperature = self.temperature_cold

        # Set default mass flow for production and demand assets
        self.mass_flow_production = 20.0  # kg/s
        self.mass_flow_demand = 15.0  # kg/s
        self.mass_flow_storage = self.mass_flow_production - self.mass_flow_demand  # kg/s

        # - Heat buffer
        self.heat_buffer_asset.inlet_massflow = self.mass_flow_storage
        self.heat_buffer_asset.inlet_temperature = self.temperature_hot
        self.heat_buffer_asset.outlet_temperature = self.temperature_cold

        # - Production asset
        self.production_asset.pre_scribe_mass_flow = False
        self.production_asset.mass_flow_rate_set_point = self.mass_flow_production
        self.production_asset.supply_temperature = self.temperature_hot

        # - Demand asset
        self.demand_asset.pre_scribe_mass_flow = True
        self.demand_asset.mass_flow_rate_set_point = self.mass_flow_demand
        self.demand_asset.supply_temperature = self.temperature_cold

    def test_setup(self):
        """Test if the setup is correct."""
        # Check if the assets are added to the network
        self.assertTrue(self.network.exists_asset(self.heat_buffer_asset.name))
        self.assertTrue(self.network.exists_asset(self.production_asset.name))
        self.assertTrue(self.network.exists_asset(self.demand_asset.name))

        # Check if the assets are connected correctly
        self.assertEqual(len(self.network.nodes), 2)

    def test_simulation_run(self):
        """Test if the simulation runs without errors."""
        # Arrange
        solver = Solver(network=self.network)

        # Act
        solver.solve()

        # Assert
        # - Production
        # -- Upstream temperature
        self.assertAlmostEqual(
            fluid_props.get_t(
                self.production_asset.prev_sol[
                    self.production_asset.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=0,
                        use_relative_indexing=True,
                    )
                ]
            ),
            self.temperature_cold,
            places=2,
        )
        # -- Downstream temperature
        self.assertAlmostEqual(
            fluid_props.get_t(
                self.production_asset.prev_sol[
                    self.production_asset.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=1,
                        use_relative_indexing=True,
                    )
                ]
            ),
            self.temperature_hot,
            places=2,
        )
        # -- Mass flow rate
        self.assertAlmostEqual(
            self.production_asset.prev_sol[
                self.production_asset.get_index_matrix(
                    property_name="mass_flow_rate",
                    connection_point=1,
                    use_relative_indexing=True,
                )
            ],
            self.mass_flow_production,
            places=2,
        )

        # - Demand
        # -- Upstream temperature
        self.assertAlmostEqual(
            fluid_props.get_t(
                self.demand_asset.prev_sol[
                    self.demand_asset.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=0,
                        use_relative_indexing=True,
                    )
                ]
            ),
            self.temperature_hot,
            places=2,
        )
        # -- Downstream temperature
        self.assertAlmostEqual(
            fluid_props.get_t(
                self.demand_asset.prev_sol[
                    self.demand_asset.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=1,
                        use_relative_indexing=True,
                    )
                ]
            ),
            self.temperature_cold,
            places=2,
        )
        # -- Mass flow rate
        self.assertAlmostEqual(
            self.demand_asset.prev_sol[
                self.demand_asset.get_index_matrix(
                    property_name="mass_flow_rate",
                    connection_point=1,
                    use_relative_indexing=True,
                )
            ],
            self.mass_flow_demand,
            places=2,
        )

        # - Heat Buffer
        # -- Upstream temperature
        self.assertAlmostEqual(
            fluid_props.get_t(
                self.heat_buffer_asset.prev_sol[
                    self.heat_buffer_asset.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=0,
                        use_relative_indexing=True,
                    )
                ]
            ),
            self.temperature_hot,
            places=2,
        )
        # -- Downstream temperature
        self.assertAlmostEqual(
            fluid_props.get_t(
                self.heat_buffer_asset.prev_sol[
                    self.heat_buffer_asset.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=1,
                        use_relative_indexing=True,
                    )
                ]
            ),
            self.temperature_cold,
            places=2,
        )
        # -- Mass flow rate
        self.assertAlmostEqual(
            self.heat_buffer_asset.prev_sol[
                self.heat_buffer_asset.get_index_matrix(
                    property_name="mass_flow_rate",
                    connection_point=1,
                    use_relative_indexing=True,
                )
            ],
            self.mass_flow_storage,
            places=2,
        )
