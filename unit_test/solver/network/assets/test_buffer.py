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

"""Test Thermocline Buffer entities."""
import unittest
from unittest.mock import patch
from uuid import uuid4

import numpy as np
import numpy.testing as np_testing

from omotes_simulator_core.solver.matrix.index_core_quantity import index_core_quantity
from omotes_simulator_core.solver.network.assets.buffer_asset import HeatBufferAsset
from omotes_simulator_core.solver.network.assets.fall_type import FallType
from omotes_simulator_core.solver.network.assets.node import Node
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


class HeatBufferAssetTest(unittest.TestCase):
    """Testcase for thermocline HeatBufferAsset class."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Create a HeatBufferAsset object
        self.asset = HeatBufferAsset(
            name=str(uuid4()),
            _id=str(uuid4()),
        )

        # Create supply, connection_point:0 and return node, connection_point:1
        self.supply_node = Node(name=str(uuid4()), _id=str(uuid4()))
        self.return_node = Node(name=str(uuid4()), _id=str(uuid4()))

        # Connect the nodes to the asset
        self.asset.connect_node(node=self.supply_node, connection_point=0)
        self.asset.connect_node(node=self.return_node, connection_point=1)

    @patch.object(HeatBufferAsset, "get_thermal_equations")
    @patch.object(HeatBufferAsset, "get_press_to_node_equation")
    @patch.object(HeatBufferAsset, "get_volumetric_continuity_equation")
    @patch.object(HeatBufferAsset, "get_mass_flow_equation")
    def test_get_equations(
        self, mass_flow_eq_patch, volumetric_cont_eq_patch, press_to_node_eq_patch, thermal_eq_patch
    ) -> None:
        """Evaluate the retrieval of equations from the HeatBufferAsset object."""
        # Arrange

        # Act
        equations = self.asset.get_equations()  # act

        # Assert
        self.assertEqual(thermal_eq_patch.call_count, 2)
        self.assertEqual(press_to_node_eq_patch.call_count, 2)
        self.assertEqual(volumetric_cont_eq_patch.call_count, 1)
        self.assertEqual(mass_flow_eq_patch.call_count, 1)
        self.assertEqual(len(equations), 6)

    def test_get_equation_insufficient_nodes(self) -> None:
        """Evaluate the retrieval of equations from the HeatBufferAsset object with insufficient nodes."""
        # Arrange
        self.asset.connected_nodes = {}

        # Act
        with self.assertRaises(ValueError) as cm:
            self.asset.get_equations()

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(str(cm.exception), "The number of connected nodes must be 2!")

    def test_get_equations_invalid_number_of_unknowns(self) -> None:
        """Evaluate the retrieval of equations from the HeatBufferAsset object with more unknowns."""
        # Arrange
        self.asset.number_of_unknowns = 4

        # Act
        with self.assertRaises(ValueError) as cm:
            self.asset.get_equations()

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(str(cm.exception), "The number of unknowns must be 6!")

    def test_get_equations_less_unknowns(self) -> None:
        """Evaluate the retrieval of equations from the HeatBufferAsset object with less unknowns."""
        # Arrange
        self.asset.number_of_unknowns = 2

        # Act
        with self.assertRaises(ValueError) as cm:
            self.asset.get_equations()

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(str(cm.exception), "The number of unknowns must be 6!")

    @patch.object(fluid_props, "get_density")
    def test_get_volumetric_continuity_equation(self, get_density_patch) -> None:
        """Evaluate getting an internal continuity equation for the HeatBufferAsset object.

        Volumetric continuity equation:
        m_in / rho_in + m_out / rho_out = 0
        """
        # Arrange
        get_density_patch.return_value = 10.0
        self.asset.prev_sol = np.array(
            [
                1.0,  # discharge 0
                2.0,  # pressure 0
                10.0,  # internal energy 0
                4.0,  # discharge 1
                5.0,  # pressure 1
                20.0,  # internal energy 1
            ]
        )

        # Act
        equation_object = self.asset.get_volumetric_continuity_equation()

        # Assert
        np_testing.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    self.asset.matrix_index + index_core_quantity.mass_flow_rate,
                    self.asset.matrix_index
                    + index_core_quantity.mass_flow_rate
                    + index_core_quantity.number_core_quantities,
                ]
            ),
        )
        np_testing.assert_array_equal(equation_object.coefficients, np.array([1 / 10.0, -1 / 10.0]))
        self.assertEqual(equation_object.rhs, 0.0)

    def test_get_internal_energy_equation(self) -> None:
        """Evaluate getting an internal energy equation for the HeatBufferAsset object.

        The equation is:
        -m_in * EI_in + m_out * EI_out - Q_supplied = 0
        """
        # Arrange
        self.asset.prev_sol = np.array(
            [
                1.0,  # discharge 0
                2.0,  # pressure 0
                3.0,  # internal energy 0
                4.0,  # discharge 1
                5.0,  # pressure 1
                6.0,  # internal energy 1
            ]
        )

        # Act
        equation_object = self.asset.get_internal_energy_equation()

        # Assert
        np_testing.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    self.asset.matrix_index + index_core_quantity.mass_flow_rate,
                    self.asset.matrix_index + index_core_quantity.internal_energy,
                    self.asset.matrix_index
                    + index_core_quantity.mass_flow_rate
                    + index_core_quantity.number_core_quantities,
                    self.asset.matrix_index
                    + index_core_quantity.internal_energy
                    + index_core_quantity.number_core_quantities,
                ]
            ),
        )
        np_testing.assert_array_equal(
            equation_object.coefficients,
            np.array(
                [
                    self.asset.prev_sol[index_core_quantity.internal_energy],
                    self.asset.prev_sol[index_core_quantity.mass_flow_rate],
                    self.asset.prev_sol[
                        index_core_quantity.internal_energy
                        + index_core_quantity.number_core_quantities
                    ],
                    self.asset.prev_sol[
                        index_core_quantity.mass_flow_rate
                        + index_core_quantity.number_core_quantities
                    ],
                ]
            ),
        )
        self.assertEqual(
            equation_object.rhs,
            self.asset.prev_sol[index_core_quantity.mass_flow_rate]
            * self.asset.prev_sol[index_core_quantity.internal_energy]
            + self.asset.prev_sol[
                index_core_quantity.mass_flow_rate + index_core_quantity.number_core_quantities
            ]
            * self.asset.prev_sol[
                index_core_quantity.internal_energy + index_core_quantity.number_core_quantities
            ]
            + self.asset.heat_flux,
        )

    @patch.object(FallType, "get_prescribe_temp_equation")
    def test_get_thermal_equations_higher_than_massflow_threshold(self, mock_energy_eq) -> None:
        """Evaluate thermal equations higher than threshold massflow.

        The equations are:
        mIE_in - mIE_out = 0
        """
        # Arrange
        connection_point = 0
        self.asset.prev_sol[
            index_core_quantity.mass_flow_rate
            + index_core_quantity.number_core_quantities * connection_point
        ] = 1.0

        # Act
        self.asset.get_thermal_equations(connection_point=connection_point)

        # Assert
        self.assertEqual(mock_energy_eq.call_count, 1)

    @patch.object(FallType, "get_internal_energy_to_node_equation")
    def test_get_thermal_equations_lower_than_massflow_threshold(self, mock_energy_eq) -> None:
        """Evaluate thermal equations lower than threshold massflow.

        The equations are:
        IE_connection_point = IE_node
        """
        # Arrange
        connection_point = 0
        self.asset.prev_sol[
            index_core_quantity.mass_flow_rate
            + index_core_quantity.number_core_quantities * connection_point
        ] = (self.asset.massflow_zero_limit * 0.1)

        # Act
        self.asset.get_thermal_equations(connection_point=connection_point)

        # Assert
        self.assertEqual(mock_energy_eq.call_count, 1)

    @patch.object(FallType, "get_press_to_node_equation")
    def test_get_press_to_node_equation(self, mock_press_to_node_eq) -> None:
        """Evaluate getting pressure to node equations for the HeatBufferAsset object.

        The equations are:
        - Pressure at the boundary - Pressure at the node = 0
        """
        # Arrange
        connection_point = 0

        # Act
        self.asset.get_press_to_node_equation(connection_point=connection_point)

        # Assert
        self.assertEqual(mock_press_to_node_eq.call_count, 1)
