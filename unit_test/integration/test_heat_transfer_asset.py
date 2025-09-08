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

from omotes_simulator_core.solver.network.assets.heat_transfer_asset import (
    HeatTransferAsset,
)
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

    def test_heat_transfer_asset_primary_positive_secondary_positive_flow(self) -> None:
        """Primary (index=0) positive and secondary (index=2) positive flow state.

        The primary side is defined as [0, 1] and the secondary side is defined as [2, 3].
        """
        # Arrange
        # Connect assets
        primary_in = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=0,
            asset2_id=self.production_asset.name,
            connection_point_2=1,
        )
        primary_out = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=1,
            asset2_id=self.production_asset.name,
            connection_point_2=0,
        )
        secondary_in = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=2,
            asset2_id=self.demand_asset.name,
            connection_point_2=1,
        )
        secondary_out = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=3,
            asset2_id=self.demand_asset.name,
            connection_point_2=0,
        )

        # Create a Solver Object
        solver = Solver(network=self.network)

        # Set the temperatures and cop for HP
        self.heat_transfer_asset.temperature_out_primary = 20 + 273.15
        self.heat_transfer_asset.temperature_out_secondary = 70 + 273.15
        self.heat_transfer_asset.heat_transfer_coefficient = 1.0 - 1.0 / 3.0
        self.heat_transfer_asset.mass_flow_initialization_primary = -1
        self.heat_transfer_asset.mass_flow_rate_rate_set_point_secondary = -1

        # Set the temperature of the demand
        self.demand_asset.supply_temperature = 40 + 273.15
        self.demand_asset.mass_flow_rate_set_point = 38.76
        self.demand_asset.pre_scribe_mass_flow = True

        # Set the temperature of the production
        self.production_asset.pre_scribe_mass_flow = False
        self.production_asset.supply_temperature = 30 + 273.15

        # -- Set associated node temperature
        self.network.get_node(primary_in).initial_temperature = 30 + 273.15
        self.network.get_node(primary_out).initial_temperature = 20 + 273.15
        self.network.get_node(secondary_in).initial_temperature = 40 + 273.15
        self.network.get_node(secondary_out).initial_temperature = 70 + 273.15

        # Act
        solver.solve()

        # Assert
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=0, use_relative_indexing=False
                )
            ],
            -77.55,
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=2, use_relative_indexing=False
                )
            ],
            -38.76,
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=0, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(primary_in).initial_temperature),
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=2, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(secondary_in).initial_temperature),
            2,
        )

    def test_heat_transfer_asset_primary_negative_secondary_positive_flow(self) -> None:
        """Primary (index=0) negative and secondary (index=2) positive flow state.

        The primary side is defined as [0, 1] and the secondary side is defined as [2, 3].
        """
        # Arrange
        # Connect assets
        primary_in = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=0,
            asset2_id=self.production_asset.name,
            connection_point_2=0,
        )
        primary_out = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=1,
            asset2_id=self.production_asset.name,
            connection_point_2=1,
        )
        secondary_in = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=2,
            asset2_id=self.demand_asset.name,
            connection_point_2=1,
        )
        secondary_out = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=3,
            asset2_id=self.demand_asset.name,
            connection_point_2=0,
        )
        # Create a Solver Object
        solver = Solver(network=self.network)

        # Set the temperatures and cop for HP
        self.heat_transfer_asset.temperature_out_primary = 20 + 273.15
        self.heat_transfer_asset.temperature_out_secondary = 70 + 273.15
        self.heat_transfer_asset.heat_transfer_coefficient = 1.0 - 1.0 / 3.0
        self.heat_transfer_asset.mass_flow_initialization_primary = +1
        self.heat_transfer_asset.mass_flow_rate_rate_set_point_secondary = -1

        # Set the temperature of the demand
        self.demand_asset.supply_temperature = 40 + 273.15
        self.demand_asset.mass_flow_rate_set_point = 38.76
        self.demand_asset.pre_scribe_mass_flow = True

        # Set the temperature of the production
        self.production_asset.pre_scribe_mass_flow = False
        self.production_asset.supply_temperature = 30 + 273.15

        # -- Set associated node temperature
        self.network.get_node(primary_in).initial_temperature = 20 + 273.15
        self.network.get_node(primary_out).initial_temperature = 30 + 273.15
        self.network.get_node(secondary_in).initial_temperature = 40 + 273.15
        self.network.get_node(secondary_out).initial_temperature = 70 + 273.15

        # Act
        solver.solve()

        # Assert
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=0, use_relative_indexing=False
                )
            ],
            77.55,
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=2, use_relative_indexing=False
                )
            ],
            -38.76,
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=0, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(primary_in).initial_temperature),
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=2, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(secondary_in).initial_temperature),
            2,
        )

    def test_heat_transfer_asset_primary_positive_secondary_negative_flow(self) -> None:
        """Primary (index=0) positive and secondary (index=2) negative flow state.

        The primary side is defined as [0, 1] and the secondary side is defined as [2, 3].
        """
        # Arrange
        # Connect assets
        primary_in = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=0,
            asset2_id=self.production_asset.name,
            connection_point_2=1,
        )
        primary_out = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=1,
            asset2_id=self.production_asset.name,
            connection_point_2=0,
        )
        secondary_in = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=2,
            asset2_id=self.demand_asset.name,
            connection_point_2=0,
        )
        secondary_out = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=3,
            asset2_id=self.demand_asset.name,
            connection_point_2=1,
        )
        # Create a Solver Object
        solver = Solver(network=self.network)
        # Set the temperatures and cop for HP
        self.heat_transfer_asset.temperature_out_primary = 20 + 273.15
        self.heat_transfer_asset.temperature_out_secondary = 70 + 273.15
        self.heat_transfer_asset.heat_transfer_coefficient = 1.0 - 1.0 / 3.0
        self.heat_transfer_asset.mass_flow_initialization_primary = -1
        self.heat_transfer_asset.mass_flow_rate_rate_set_point_secondary = +1

        # Set the temperature of the demand
        self.demand_asset.supply_temperature = 40 + 273.15
        self.demand_asset.mass_flow_rate_set_point = 38.76
        self.demand_asset.pre_scribe_mass_flow = True

        # Set the temperature of the production
        self.production_asset.pre_scribe_mass_flow = False
        self.production_asset.supply_temperature = 30 + 273.15

        # -- Set associated node temperature
        self.network.get_node(primary_in).initial_temperature = 30 + 273.15
        self.network.get_node(primary_out).initial_temperature = 20 + 273.15
        self.network.get_node(secondary_in).initial_temperature = 40 + 273.15
        self.network.get_node(secondary_out).initial_temperature = 70 + 273.15

        # Act
        solver.solve()

        # Assert
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=0, use_relative_indexing=False
                )
            ],
            -77.55,
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=2, use_relative_indexing=False
                )
            ],
            38.76,
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=0, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(primary_in).initial_temperature),
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=3, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(secondary_in).initial_temperature),
            2,
        )

    def test_heat_transfer_asset_positive_heat_transfer_coefficient(self) -> None:
        """Test a positive heat transfer coefficient.

        The primary side is defined as [0, 1] and the secondary side is defined as [2, 3].
        Primary (index=0) positive and secondary (index=2) positive flow state.
        """
        # Arrange
        # Connect assets
        primary_in = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=0,
            asset2_id=self.production_asset.name,
            connection_point_2=1,
        )
        primary_out = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=1,
            asset2_id=self.production_asset.name,
            connection_point_2=0,
        )
        secondary_in = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=2,
            asset2_id=self.demand_asset.name,
            connection_point_2=1,
        )
        secondary_out = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=3,
            asset2_id=self.demand_asset.name,
            connection_point_2=0,
        )
        # Create a Solver Object
        solver = Solver(network=self.network)
        # Set the temperatures and cop for HP
        self.heat_transfer_asset.temperature_out_primary = 20 + 273.15
        self.heat_transfer_asset.temperature_out_secondary = 70 + 273.15
        self.heat_transfer_asset.heat_transfer_coefficient = 1.0 - 1.0 / 5.0
        self.heat_transfer_asset.mass_flow_rate_rate_set_point_secondary = -38.76

        # Set the temperature of the demand
        self.demand_asset.supply_temperature = 40 + 273.15
        self.demand_asset.mass_flow_rate_set_point = 38.76
        self.demand_asset.pre_scribe_mass_flow = True

        # Set the temperature of the production
        self.production_asset.pre_scribe_mass_flow = False
        self.production_asset.supply_temperature = 30 + 273.15

        # -- Set associated node temperature
        self.network.get_node(primary_in).initial_temperature = 30 + 273.15
        self.network.get_node(primary_out).initial_temperature = 20 + 273.15
        self.network.get_node(secondary_in).initial_temperature = 40 + 273.15
        self.network.get_node(secondary_out).initial_temperature = 70 + 273.15

        # Act
        solver.solve()
        # Assert
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=0, use_relative_indexing=False
                )
            ],
            -93.07,
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=2, use_relative_indexing=False
                )
            ],
            -38.76,
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=0, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(primary_in).initial_temperature),
            2,
        )

    def test_heat_transfer_asset_heat_transfer_coefficient_of_one(self) -> None:
        """Test a heat transfer coefficient equal to one.

        The primary side is defined as [0, 1] and the secondary side is defined as [2, 3].
        Primary (index=0) positive and secondary (index=2) positive flow state.
        """
        # Arrange
        # Connect assets
        primary_in = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=0,
            asset2_id=self.production_asset.name,
            connection_point_2=1,
        )
        primary_out = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=1,
            asset2_id=self.production_asset.name,
            connection_point_2=0,
        )
        secondary_in = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=2,
            asset2_id=self.demand_asset.name,
            connection_point_2=1,
        )
        secondary_out = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=3,
            asset2_id=self.demand_asset.name,
            connection_point_2=0,
        )
        # Create a Solver Object
        solver = Solver(network=self.network)
        # Set the temperatures and cop for HP
        self.heat_transfer_asset.temperature_out_primary = 40 + 273.15
        self.heat_transfer_asset.temperature_out_secondary = 70 + 273.15
        self.heat_transfer_asset.heat_transfer_coefficient = 1.0  # - 1.0 / 5.0
        self.heat_transfer_asset.mass_flow_rate_rate_set_point_secondary = -38.76

        # Set the temperature of the demand
        self.demand_asset.supply_temperature = 40 + 273.15
        self.demand_asset.mass_flow_rate_set_point = 38.76
        self.demand_asset.pre_scribe_mass_flow = True

        # Set the temperature of the production
        self.production_asset.pre_scribe_mass_flow = False
        self.production_asset.supply_temperature = 70 + 273.15

        # -- Set associated node temperature
        self.network.get_node(primary_in).initial_temperature = 70 + 273.15
        self.network.get_node(primary_out).initial_temperature = 40 + 273.15
        self.network.get_node(secondary_in).initial_temperature = 40 + 273.15
        self.network.get_node(secondary_out).initial_temperature = 70 + 273.15

        # Act
        solver.solve()
        # Assert
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=0, use_relative_indexing=False
                )
            ],
            -38.76,
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=2, use_relative_indexing=False
                )
            ],
            -38.76,
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=0, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(primary_in).initial_temperature),
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=2, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(secondary_in).initial_temperature),
            2,
        )

    def test_heat_transfer_asset_negative_heat_transfer_coefficient(self) -> None:
        """Test a negative heat transfer coefficient.

        The primary side is defined as [0, 1] and the secondary side is defined as [2, 3].
        Primary (index=0) positive and secondary (index=2) positive flow state.
        """
        # Arrange
        # Connect assets
        primary_in = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=0,
            asset2_id=self.production_asset.name,
            connection_point_2=1,
        )
        primary_out = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=1,
            asset2_id=self.production_asset.name,
            connection_point_2=0,
        )
        secondary_in = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=2,
            asset2_id=self.demand_asset.name,
            connection_point_2=1,
        )
        secondary_out = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=3,
            asset2_id=self.demand_asset.name,
            connection_point_2=0,
        )
        # Create a Solver Object
        solver = Solver(network=self.network)
        # Set the temperatures and cop for HP
        self.heat_transfer_asset.temperature_out_primary = 30 + 273.15
        self.heat_transfer_asset.temperature_out_secondary = 40 + 273.15
        self.heat_transfer_asset.heat_transfer_coefficient = -1 * (1.0 - 1.0 / 5.0)
        self.heat_transfer_asset.mass_flow_initialization_primary = -1
        self.heat_transfer_asset.mass_flow_rate_rate_set_point_secondary = -1

        # Set the temperature of the demand
        self.demand_asset.supply_temperature = 70 + 273.15
        self.demand_asset.mass_flow_rate_set_point = 38.76
        self.demand_asset.pre_scribe_mass_flow = True

        # Set the temperature of the production
        self.production_asset.pre_scribe_mass_flow = False
        self.production_asset.supply_temperature = 20 + 273.15

        # -- Set associated node temperature
        self.network.get_node(primary_in).initial_temperature = 20 + 273.15
        self.network.get_node(primary_out).initial_temperature = 30 + 273.15
        self.network.get_node(secondary_in).initial_temperature = 70 + 273.15
        self.network.get_node(secondary_out).initial_temperature = 40 + 273.15

        # Act
        solver.solve()

        # Assert
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=0, use_relative_indexing=False
                )
            ],
            -93.07,
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=2, use_relative_indexing=False
                )
            ],
            -38.76,
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=0, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(primary_in).initial_temperature),
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=1, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(primary_out).initial_temperature),
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=2, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(secondary_in).initial_temperature),
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=3, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(secondary_out).initial_temperature),
            2,
        )

    def test_heat_transfer_asset_zero_flow(self) -> None:
        """Test zero flow across the heat transfer asset.

        The primary side is defined as [0, 1] and the secondary side is defined as [2, 3].
        Primary (index=0) positive and secondary (index=2) positive flow state.
        """
        # Arrange
        # Connect assets
        primary_in = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=0,
            asset2_id=self.production_asset.name,
            connection_point_2=1,
        )
        primary_out = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=1,
            asset2_id=self.production_asset.name,
            connection_point_2=0,
        )
        secondary_in = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=2,
            asset2_id=self.demand_asset.name,
            connection_point_2=1,
        )
        secondary_out = self.network.connect_assets(
            asset1_id=self.heat_transfer_asset.name,
            connection_point_1=3,
            asset2_id=self.demand_asset.name,
            connection_point_2=0,
        )
        # Create a Solver Object
        solver = Solver(network=self.network)

        # Set the temperatures and cop for HP
        self.heat_transfer_asset.temperature_out_primary = 20 + 273.15
        self.heat_transfer_asset.temperature_out_secondary = 70 + 273.15
        self.heat_transfer_asset.heat_transfer_coefficient = 1.0 - 1.0 / 5.0
        self.heat_transfer_asset.mass_flow_initialization_primary = 0.0
        self.heat_transfer_asset.mass_flow_rate_rate_set_point_secondary = 0.0

        # Set the temperature of the demand
        self.demand_asset.supply_temperature = 40 + 273.15
        self.demand_asset.mass_flow_rate_set_point = 0.0
        self.demand_asset.pre_scribe_mass_flow = True

        # Set the temperature of the production
        self.production_asset.pre_scribe_mass_flow = False
        self.production_asset.supply_temperature = 30 + 273.15

        # -- Set associated node temperature
        self.network.get_node(primary_in).initial_temperature = 30 + 273.15
        self.network.get_node(primary_out).initial_temperature = 20 + 273.15
        self.network.get_node(secondary_in).initial_temperature = 40 + 273.15
        self.network.get_node(secondary_out).initial_temperature = 70 + 273.15

        # Act
        solver.solve()

        # Assert
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=0, use_relative_indexing=False
                )
            ],
            0.0,
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=2, use_relative_indexing=False
                )
            ],
            0.0,
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=0, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(primary_in).initial_temperature),
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=1, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(primary_out).initial_temperature),
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=2, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(secondary_in).initial_temperature),
            2,
        )
        self.assertAlmostEqual(
            self.heat_transfer_asset.prev_sol[
                self.heat_transfer_asset.get_index_matrix(
                    property_name="internal_energy", connection_point=3, use_relative_indexing=False
                )
            ],
            fluid_props.get_ie(self.network.get_node(secondary_out).initial_temperature),
            2,
        )
