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

import unittest
from unittest.mock import patch
from uuid import uuid4

from omotes_simulator_core.solver.network.assets.heat_transfer_asset import HeatTransferAsset
from omotes_simulator_core.solver.network.assets.node import Node
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


class HeatTransferTest(unittest.TestCase):
    """Testcase for Boundary class."""

    def setUp(self) -> None:
        self.asset = HeatTransferAsset(
            name=str(uuid4()),
            _id=str(uuid4()),
        )
        # Create supply, connection_point:0 and return node, connection_point:1
        self.prim_supply_node = Node(name=str(uuid4()), _id=str(uuid4()))
        self.prim_return_node = Node(name=str(uuid4()), _id=str(uuid4()))
        self.sec_supply_node = Node(name=str(uuid4()), _id=str(uuid4()))
        self.sec_return_node = Node(name=str(uuid4()), _id=str(uuid4()))
        # Connect the nodes to the asset
        self.asset.connect_node(node=self.prim_supply_node, connection_point=0)
        self.asset.connect_node(node=self.prim_return_node, connection_point=1)
        self.asset.connect_node(node=self.sec_supply_node, connection_point=2)
        self.asset.connect_node(node=self.sec_return_node, connection_point=3)

    @patch.object(HeatTransferAsset, "get_internal_energy_to_node_equation")
    @patch.object(HeatTransferAsset, "prescribe_temperature_at_connection_point")
    @patch.object(HeatTransferAsset, "prescribe_mass_flow_at_connection_point")
    @patch.object(HeatTransferAsset, "prescribe_pressure_at_connection_point")
    @patch.object(HeatTransferAsset, "get_press_to_node_equation")
    @patch.object(HeatTransferAsset, "add_continuity_equation")
    @patch.object(HeatTransferAsset, "get_mass_flow_from_prev_solution")
    def test_get_equations_initial_conditions_prescribe_pressure_secondary(
        self,
        mock_get_mass_flow_from_prev_solution,
        mock_add_continuity_equation,
        mock_get_press_to_node_equation,
        mock_prescribe_pressure_at_connection_point,
        mock_prescribe_mass_flow_at_connection_point,
        mock_prescribe_temperature_at_connection_point,
        mock_get_internal_energy_to_node_equation,
    ):
        """Test get_equations with default parameters.

        Test assumes:
        - connection point order [0, 1, 2, 3] corresponds to [primary_in, primary_out, secondary_in,
        secondary_out].
        - massflow at primary_in flows into the asset (m_0 < m_threshold).
        - massflow at secondary_in flow into the asset (m_2 < m_threshold).
        - pressure at secondary side is prescribed (pre_scribe_mass_flow_secondary = False).
        """
        # Arrange

        # Act
        equations = self.asset.get_equations()  # act

        # Assert
        self.assertEqual(len(equations), 12)
        self.assertEqual(mock_add_continuity_equation.call_count, 1)
        self.assertEqual(mock_get_press_to_node_equation.call_count, 4)
        self.assertEqual(mock_prescribe_pressure_at_connection_point.call_count, 2)
        self.assertEqual(mock_prescribe_mass_flow_at_connection_point.call_count, 1)
        self.assertEqual(mock_prescribe_temperature_at_connection_point.call_count, 0)
        self.assertEqual(mock_get_internal_energy_to_node_equation.call_count, 4)
        self.assertEqual(mock_get_mass_flow_from_prev_solution.call_count, 0)
        self.assertEqual(
            (
                mock_add_continuity_equation.call_count
                + mock_get_press_to_node_equation.call_count
                + mock_prescribe_pressure_at_connection_point.call_count
                + mock_prescribe_mass_flow_at_connection_point.call_count
                + mock_prescribe_temperature_at_connection_point.call_count
                + mock_get_internal_energy_to_node_equation.call_count
            ),
            12,
        )

    @patch.object(HeatTransferAsset, "get_internal_energy_to_node_equation")
    @patch.object(HeatTransferAsset, "prescribe_temperature_at_connection_point")
    @patch.object(HeatTransferAsset, "prescribe_mass_flow_at_connection_point")
    @patch.object(HeatTransferAsset, "prescribe_pressure_at_connection_point")
    @patch.object(HeatTransferAsset, "get_press_to_node_equation")
    @patch.object(HeatTransferAsset, "add_continuity_equation")
    @patch.object(HeatTransferAsset, "get_mass_flow_from_prev_solution")
    def test_get_equations_initial_conditions_prescribe_mass_flow_secondary(
        self,
        mock_get_mass_flow_from_prev_solution,
        mock_add_continuity_equation,
        mock_get_press_to_node_equation,
        mock_prescribe_pressure_at_connection_point,
        mock_prescribe_mass_flow_at_connection_point,
        mock_prescribe_temperature_at_connection_point,
        mock_get_internal_energy_to_node_equation,
    ):
        """Test get_equations with default parameters.

        Test assumes:
        - connection point order [0, 1, 2, 3] corresponds to [primary_in, primary_out, secondary_in,
        secondary_out].
        - massflow at primary_in flows into the asset (m_0 < m_threshold).
        - massflow at secondary_in flow into the asset (m_2 < m_threshold).
        - massflow at secondary side is prescribed (pre_scribe_mass_flow_secondary = True).
        """
        # Arrange
        self.asset.pre_scribe_mass_flow_secondary = True

        # Act
        equations = self.asset.get_equations()  # act

        # Assert
        self.assertEqual(len(equations), 12)
        self.assertEqual(mock_add_continuity_equation.call_count, 1)
        self.assertEqual(mock_get_press_to_node_equation.call_count, 4)
        self.assertEqual(mock_prescribe_pressure_at_connection_point.call_count, 0)
        self.assertEqual(mock_prescribe_mass_flow_at_connection_point.call_count, 3)
        self.assertEqual(mock_prescribe_temperature_at_connection_point.call_count, 0)
        self.assertEqual(mock_get_internal_energy_to_node_equation.call_count, 4)
        self.assertEqual(mock_get_mass_flow_from_prev_solution.call_count, 0)
        self.assertEqual(
            (
                mock_add_continuity_equation.call_count
                + mock_get_press_to_node_equation.call_count
                + mock_prescribe_pressure_at_connection_point.call_count
                + mock_prescribe_mass_flow_at_connection_point.call_count
                + mock_prescribe_temperature_at_connection_point.call_count
                + mock_get_internal_energy_to_node_equation.call_count
            ),
            12,
        )

    @patch.object(HeatTransferAsset, "get_internal_energy_to_node_equation")
    @patch.object(HeatTransferAsset, "prescribe_temperature_at_connection_point")
    @patch.object(HeatTransferAsset, "prescribe_mass_flow_at_connection_point")
    @patch.object(HeatTransferAsset, "prescribe_pressure_at_connection_point")
    @patch.object(HeatTransferAsset, "get_press_to_node_equation")
    @patch.object(HeatTransferAsset, "add_continuity_equation")
    @patch.object(HeatTransferAsset, "get_mass_flow_from_prev_solution")
    def test_get_equations_zero_flow_prescribe_pressure_secondary(
        self,
        mock_get_mass_flow_from_prev_solution,
        mock_add_continuity_equation,
        mock_get_press_to_node_equation,
        mock_prescribe_pressure_at_connection_point,
        mock_prescribe_mass_flow_at_connection_point,
        mock_prescribe_temperature_at_connection_point,
        mock_get_internal_energy_to_node_equation,
    ):
        """Test get_equations from previous solution with zero flow.

        Test assumes:
        - connection point order [0, 1, 2, 3] corresponds to [primary_in, primary_out, secondary_in,
        secondary_out].
        - massflow at primary_in flows into the asset (m_0 < m_threshold).
        - massflow at secondary_in flow into the asset (m_2 < m_threshold).
        - pressure at secondary side is prescribed (pre_scribe_mass_flow_secondary = False).
        """
        # Arrange
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="mass_flow_rate", connection_point=0, use_relative_indexing=False
            )
        ] = 0.0
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="mass_flow_rate", connection_point=2, use_relative_indexing=False
            )
        ] = 0.0
        # -- Set temperatures to override zero value check
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=0, use_relative_indexing=False
            )
        ] = fluid_props.get_ie(273.15 + 30)
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=1, use_relative_indexing=False
            )
        ] = fluid_props.get_ie(273.15 + 20)
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=2, use_relative_indexing=False
            )
        ] = fluid_props.get_ie(273.15 + 40)
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=3, use_relative_indexing=False
            )
        ] = fluid_props.get_ie(273.15 + 70)

        # Act
        equations = self.asset.get_equations()  # act

        # Assert
        self.assertEqual(len(equations), 12)
        self.assertEqual(mock_add_continuity_equation.call_count, 1)
        self.assertEqual(mock_get_press_to_node_equation.call_count, 4)
        self.assertEqual(mock_prescribe_pressure_at_connection_point.call_count, 2)
        self.assertEqual(mock_prescribe_mass_flow_at_connection_point.call_count, 1)
        self.assertEqual(mock_prescribe_temperature_at_connection_point.call_count, 2)
        self.assertEqual(mock_get_internal_energy_to_node_equation.call_count, 2)
        self.assertEqual(mock_get_mass_flow_from_prev_solution.call_count, 1)
        self.assertEqual(
            (
                mock_add_continuity_equation.call_count
                + mock_get_press_to_node_equation.call_count
                + mock_prescribe_pressure_at_connection_point.call_count
                + mock_prescribe_mass_flow_at_connection_point.call_count
                + mock_prescribe_temperature_at_connection_point.call_count
                + mock_get_internal_energy_to_node_equation.call_count
            ),
            12,
        )

    @patch.object(HeatTransferAsset, "get_internal_energy_to_node_equation")
    @patch.object(HeatTransferAsset, "prescribe_temperature_at_connection_point")
    @patch.object(HeatTransferAsset, "prescribe_mass_flow_at_connection_point")
    @patch.object(HeatTransferAsset, "prescribe_pressure_at_connection_point")
    @patch.object(HeatTransferAsset, "get_press_to_node_equation")
    @patch.object(HeatTransferAsset, "add_continuity_equation")
    @patch.object(HeatTransferAsset, "get_mass_flow_from_prev_solution")
    def test_get_equations_flow_prescribe_mass_flow_secondary(
        self,
        mock_get_mass_flow_from_prev_solution,
        mock_add_continuity_equation,
        mock_get_press_to_node_equation,
        mock_prescribe_pressure_at_connection_point,
        mock_prescribe_mass_flow_at_connection_point,
        mock_prescribe_temperature_at_connection_point,
        mock_get_internal_energy_to_node_equation,
    ):
        """Test get_equations from previous solution with zero flow.

        Test assumes:
        - connection point order [0, 1, 2, 3] corresponds to [primary_in, primary_out, secondary_in,
        secondary_out].
        - massflow at primary_in flows into the asset (m_0 < m_threshold).
        - massflow at secondary_in flow into the asset (m_2 < m_threshold).
        - pressure at secondary side is prescribed (pre_scribe_mass_flow_secondary = True).
        """
        # Arrange
        self.asset.pre_scribe_mass_flow_secondary = True
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="mass_flow_rate", connection_point=0, use_relative_indexing=False
            )
        ] = 0.0
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="mass_flow_rate", connection_point=2, use_relative_indexing=False
            )
        ] = 0.0
        # -- Set temperatures to override zero value check
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=0, use_relative_indexing=False
            )
        ] = fluid_props.get_ie(273.15 + 30)
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=1, use_relative_indexing=False
            )
        ] = fluid_props.get_ie(273.15 + 20)
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=2, use_relative_indexing=False
            )
        ] = fluid_props.get_ie(273.15 + 40)
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=3, use_relative_indexing=False
            )
        ] = fluid_props.get_ie(273.15 + 70)

        # Act
        equations = self.asset.get_equations()  # act

        # Assert
        self.assertEqual(len(equations), 12)
        self.assertEqual(mock_add_continuity_equation.call_count, 1)
        self.assertEqual(mock_get_press_to_node_equation.call_count, 4)
        self.assertEqual(mock_prescribe_pressure_at_connection_point.call_count, 0)
        self.assertEqual(mock_prescribe_mass_flow_at_connection_point.call_count, 3)
        self.assertEqual(mock_prescribe_temperature_at_connection_point.call_count, 2)
        self.assertEqual(mock_get_internal_energy_to_node_equation.call_count, 2)
        self.assertEqual(mock_get_mass_flow_from_prev_solution.call_count, 1)
        self.assertEqual(
            (
                mock_add_continuity_equation.call_count
                + mock_get_press_to_node_equation.call_count
                + mock_prescribe_pressure_at_connection_point.call_count
                + mock_prescribe_mass_flow_at_connection_point.call_count
                + mock_prescribe_temperature_at_connection_point.call_count
                + mock_get_internal_energy_to_node_equation.call_count
            ),
            12,
        )

    @patch.object(HeatTransferAsset, "get_internal_energy_to_node_equation")
    @patch.object(HeatTransferAsset, "prescribe_temperature_at_connection_point")
    @patch.object(HeatTransferAsset, "prescribe_mass_flow_at_connection_point")
    @patch.object(HeatTransferAsset, "prescribe_pressure_at_connection_point")
    @patch.object(HeatTransferAsset, "get_press_to_node_equation")
    @patch.object(HeatTransferAsset, "add_continuity_equation")
    @patch.object(HeatTransferAsset, "get_mass_flow_from_prev_solution")
    def test_get_equations_with_flow_prescribe_pressure_secondary(
        self,
        mock_get_mass_flow_from_prev_solution,
        mock_add_continuity_equation,
        mock_get_press_to_node_equation,
        mock_prescribe_pressure_at_connection_point,
        mock_prescribe_mass_flow_at_connection_point,
        mock_prescribe_temperature_at_connection_point,
        mock_get_internal_energy_to_node_equation,
    ):
        """Test get_equations from previous solution nonzero flow.

        Test assumes:
        - connection point order [0, 1, 2, 3] corresponds to [primary_in, primary_out, secondary_in,
        secondary_out].
        - massflow at primary_in flows into the asset (m_0 < m_threshold).
        - massflow at secondary_in flow into the asset (m_2 < m_threshold).
        - pressure at secondary side is prescribed (pre_scribe_mass_flow_secondary = False).
        """
        # Arrange
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="mass_flow_rate", connection_point=0, use_relative_indexing=False
            )
        ] = -77.55
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="mass_flow_rate", connection_point=2, use_relative_indexing=False
            )
        ] = -38.76
        # -- Set temperatures to override zero value check
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=0, use_relative_indexing=False
            )
        ] = fluid_props.get_ie(273.15 + 30)
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=1, use_relative_indexing=False
            )
        ] = fluid_props.get_ie(273.15 + 20)
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=2, use_relative_indexing=False
            )
        ] = fluid_props.get_ie(273.15 + 40)
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=3, use_relative_indexing=False
            )
        ] = fluid_props.get_ie(273.15 + 70)

        # Act
        equations = self.asset.get_equations()  # act

        # Assert
        self.assertEqual(len(equations), 12)
        self.assertEqual(mock_add_continuity_equation.call_count, 1)
        self.assertEqual(mock_get_press_to_node_equation.call_count, 4)
        self.assertEqual(mock_prescribe_pressure_at_connection_point.call_count, 2)
        self.assertEqual(mock_prescribe_mass_flow_at_connection_point.call_count, 1)
        self.assertEqual(mock_prescribe_temperature_at_connection_point.call_count, 2)
        self.assertEqual(mock_get_internal_energy_to_node_equation.call_count, 2)
        self.assertEqual(mock_get_mass_flow_from_prev_solution.call_count, 1)
        self.assertEqual(
            (
                mock_add_continuity_equation.call_count
                + mock_get_press_to_node_equation.call_count
                + mock_prescribe_pressure_at_connection_point.call_count
                + mock_prescribe_mass_flow_at_connection_point.call_count
                + mock_prescribe_temperature_at_connection_point.call_count
                + mock_get_internal_energy_to_node_equation.call_count
            ),
            12,
        )

    def test_get_heat_power_primary(self):
        """Test get_heat_power_primary method."""
        # Arrange
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=0, use_relative_indexing=False
            )
        ] = 5.0
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=1, use_relative_indexing=False
            )
        ] = 10.0
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="mass_flow_rate", connection_point=0, use_relative_indexing=False
            )
        ] = 1.0

        # Act
        heat_power = self.asset.get_heat_power_primary()

        # Assert
        self.assertEqual(heat_power, 5)

    def test_get_heat_power_secondary(self):
        """Test get_heat_power_secondary method."""
        # Arrange
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=2, use_relative_indexing=False
            )
        ] = 15.0
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=3, use_relative_indexing=False
            )
        ] = 20.0
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="mass_flow_rate", connection_point=2, use_relative_indexing=False
            )
        ] = 1.0

        # Act
        heat_power = self.asset.get_heat_power_secondary()

        # Assert
        self.assertEqual(heat_power, 5)

    def test_get_electric_power_consumption(self):
        """Test get_electric_power_consumption method."""
        # Arrange
        self.asset.heat_transfer_coefficient = 5.0
        # --- Primary side
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=0, use_relative_indexing=False
            )
        ] = 5.0
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=1, use_relative_indexing=False
            )
        ] = 10.0
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="mass_flow_rate", connection_point=0, use_relative_indexing=False
            )
        ] = 2.0

        # --- Secondary side
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=2, use_relative_indexing=False
            )
        ] = 15.0
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="internal_energy", connection_point=3, use_relative_indexing=False
            )
        ] = 20.0
        self.asset.prev_sol[
            self.asset.get_index_matrix(
                property_name="mass_flow_rate", connection_point=2, use_relative_indexing=False
            )
        ] = 1.0

        # Act
        electric_power = self.asset.get_electric_power_consumption()

        # Assert
        self.assertEqual(electric_power, 1.0)
