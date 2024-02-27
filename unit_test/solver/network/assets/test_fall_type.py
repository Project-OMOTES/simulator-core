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

"""Test FallType entities."""
import unittest
from unittest.mock import patch
from uuid import uuid4

import numpy as np
import numpy.testing as np_testing

from simulator_core.solver.matrix.core_enum import NUMBER_CORE_QUANTITIES, IndexEnum
from simulator_core.solver.network.assets.fall_type import FallType
from simulator_core.solver.network.assets.node import Node


class FallTypeTest(unittest.TestCase):
    """Testcase for Boundary class."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Create a BaseBoundary object
        self.asset = FallType(
            name=uuid4(),
        )
        # Create supply, connection_point:0 and return node, connection_point:1
        self.supply_node = Node(name=uuid4())
        self.return_node = Node(name=uuid4())
        # Connect the nodes to the asset
        self.asset.connect_node(node=self.supply_node, connection_point=0)
        self.asset.connect_node(node=self.return_node, connection_point=1)

    @patch.object(FallType, "add_thermal_equations")
    @patch.object(FallType, "add_press_to_node_equation")
    @patch.object(FallType, "add_internal_cont_equation")
    @patch.object(FallType, "add_internal_pressure_loss_equation")
    def test_get_equations(
        self, press_loss_eq_patch, internal_cont_eq_patch, press_to_node_patch, thermal_patch
    ) -> None:
        """Evaluate the retrieval of equations from the boundary object."""
        # Arrange

        # Act
        equations = self.asset.get_equations()  # act

        # Assert
        self.assertEqual(thermal_patch.call_count, 2)
        self.assertEqual(press_to_node_patch.call_count, 2)
        self.assertEqual(internal_cont_eq_patch.call_count, 1)
        self.assertEqual(press_loss_eq_patch.call_count, 1)
        self.assertEqual(len(equations), 6)

    def test_get_equation_insufficient_nodes(self) -> None:
        """Evaluate the retrieval of equations from the boundary object with insufficient nodes."""
        # Arrange
        self.asset.connected_nodes = []

        # Act
        with self.assertRaises(ValueError) as cm:
            self.asset.get_equations()

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(str(cm.exception), "The number of connected nodes must be 2!")

    def test_get_equations_invalid_number_of_unknowns(self) -> None:
        """Evaluate the retrieval of equations from the boundary object with more unknowns."""
        # Arrange
        self.asset.number_of_unknowns = 4

        # Act
        with self.assertRaises(ValueError) as cm:
            self.asset.get_equations()

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(str(cm.exception), "The number of unknowns must be 6!")

    def test_get_equations_less_unknowns(self) -> None:
        """Evaluate the retrieval of equations from the boundary object with less unknowns."""
        # Arrange
        self.asset.number_of_unknowns = 2

        # Act
        with self.assertRaises(ValueError) as cm:
            self.asset.get_equations()

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(str(cm.exception), "The number of unknowns must be 6!")

    def test_add_internal_cont_equation(self) -> None:
        """Evaluate the addition of an internal continuity equation to the boundary object.

        Conservation of mass equation:
        m_in = m_out
        """
        # Arrange

        # Act
        equation_object = self.asset.add_internal_cont_equation()

        # Assert
        np_testing.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    self.asset.matrix_index + IndexEnum.discharge,
                    self.asset.matrix_index + IndexEnum.discharge + NUMBER_CORE_QUANTITIES,
                ]
            ),
        )
        np_testing.assert_array_equal(equation_object.coefficients, np.array([1.0, 1.0]))
        self.assertEqual(equation_object.rhs, 0.0)

    def test_add_internal_energy_equation(self) -> None:
        """Evaluate the addition of an internal energy equation to the boundary object.

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
        equation_object = self.asset.add_internal_energy_equation()

        # Assert
        np_testing.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    self.asset.matrix_index + IndexEnum.discharge,
                    self.asset.matrix_index + IndexEnum.internal_energy,
                    self.asset.matrix_index + IndexEnum.discharge + NUMBER_CORE_QUANTITIES,
                    self.asset.matrix_index + IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES,
                ]
            ),
        )
        np_testing.assert_array_equal(
            equation_object.coefficients,
            np.array(
                [
                    self.asset.prev_sol[IndexEnum.internal_energy],
                    self.asset.prev_sol[IndexEnum.discharge],
                    self.asset.prev_sol[IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES],
                    self.asset.prev_sol[IndexEnum.discharge + NUMBER_CORE_QUANTITIES],
                ]
            ),
        )
        self.assertEqual(
            equation_object.rhs,
            self.asset.prev_sol[IndexEnum.discharge]
            * self.asset.prev_sol[IndexEnum.internal_energy]
            + self.asset.prev_sol[IndexEnum.discharge + NUMBER_CORE_QUANTITIES]
            * self.asset.prev_sol[IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES]
            + self.asset.heat_supplied,
        )

    def test_add_internal_pressure_loss_equation(self) -> None:
        """Evaluate the addition of an internal pressure loss equation to the boundary object.

        The equation is:
        - Pressure at inlet - Pressure at outlet - 2 * Loss coefficient * Mass flow rate *
        abs(Mass flow rate) = 0
        """
        # Arrange
        self.asset.prev_sol = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        self.asset.update_loss_coefficient()

        # Act
        equation_object = self.asset.add_internal_pressure_loss_equation()

        # Assert
        np_testing.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    self.asset.matrix_index + IndexEnum.discharge,
                    self.asset.matrix_index + IndexEnum.pressure,
                    self.asset.matrix_index + IndexEnum.pressure + NUMBER_CORE_QUANTITIES,
                ]
            ),
        )
        np_testing.assert_array_equal(
            equation_object.coefficients,
            np.array(
                [
                    -2.0
                    * self.asset.loss_coefficient
                    * abs(self.asset.prev_sol[IndexEnum.discharge]),
                    -1.0,
                    1.0,
                ]
            ),
        )
        self.assertEqual(
            equation_object.rhs,
            -self.asset.loss_coefficient
            * self.asset.prev_sol[IndexEnum.discharge]
            * abs(self.asset.prev_sol[IndexEnum.discharge]),
        )

    def test_add_internal_pressure_loss_equation_linearized_discharge(self) -> None:
        """Evaluate the addition of an internal pressure loss equation to the boundary object.

        The equation is:
        - Pressure at inlet - Pressure at outlet - 2 * Loss coefficient * Mass flow rate *
        abs(Mass flow rate) = 0
        """
        # Arrange
        self.asset.prev_sol = np.array([0.0, 2.0, 3.0, 0.0, 5.0, 6.0])
        self.asset.update_loss_coefficient()

        # Act
        equation_object = self.asset.add_internal_pressure_loss_equation()

        # Assert
        np_testing.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    self.asset.matrix_index + IndexEnum.discharge,
                    self.asset.matrix_index + IndexEnum.pressure,
                    self.asset.matrix_index + IndexEnum.pressure + NUMBER_CORE_QUANTITIES,
                ]
            ),
        )
        np_testing.assert_array_equal(
            equation_object.coefficients,
            np.array([-2.0 * self.asset.loss_coefficient * 1e-5, -1.0, 1.0]),
        )
        self.assertEqual(
            equation_object.rhs,
            -self.asset.loss_coefficient * 1e-5 * self.asset.prev_sol[IndexEnum.discharge],
        )

    @patch.object(FallType, "add_internal_energy_equation")
    def test_add_thermal_equations(self, mock_energy_eq) -> None:
        """Evaluate the addition of thermal equations to the boundary object.

        The equations are:
        mIE_in - mIE_out = 0
        """
        # Arrange
        connection_point = 0
        self.asset.prev_sol[IndexEnum.discharge + NUMBER_CORE_QUANTITIES * connection_point] = 1.0

        # Act
        self.asset.add_thermal_equations(connection_point=connection_point)

        # Assert
        self.assertEqual(mock_energy_eq.call_count, 1)

    @patch.object(FallType, "add_press_to_node_equation")
    def test_add_press_to_node_equation(self, mock_press_to_node_eq) -> None:
        """Evaluate the addition of pressure to node equations to the boundary object.

        The equations are:
        - Pressure at the boundary - Pressure at the node = 0
        """
        # Arrange
        connection_point = 0

        # Act
        self.asset.add_press_to_node_equation(connection_point=connection_point)

        # Assert
        self.assertEqual(mock_press_to_node_eq.call_count, 1)
