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

from omotes_simulator_core.solver.matrix.index_core_quantity import (
    NUMBER_OF_CORE_QUANTITIES,
    CoreQuantity,
)
from omotes_simulator_core.solver.network.assets.fall_type import FallType
from omotes_simulator_core.solver.network.assets.node import Node


class FallTypeTest(unittest.TestCase):
    """Testcase for Boundary class."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Create a BaseBoundary object
        self.asset = FallType(
            name=str(uuid4()),
            _id=str(uuid4()),
        )
        # Create supply, connection_point:0 and return node, connection_point:1
        self.supply_node = Node(name=str(uuid4()), _id=str(uuid4()))
        self.return_node = Node(name=str(uuid4()), _id=str(uuid4()))
        # Connect the nodes to the asset
        self.asset.connect_node(node=self.supply_node, connection_point=0)
        self.asset.connect_node(node=self.return_node, connection_point=1)

    @patch.object(FallType, "get_thermal_equations")
    @patch.object(FallType, "get_press_to_node_equation")
    @patch.object(FallType, "get_internal_cont_equation")
    @patch.object(FallType, "get_internal_pressure_loss_equation")
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
        self.asset.connected_nodes = {}

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

    def test_get_internal_cont_equation(self) -> None:
        """Evaluate getting an internal continuity equation for the boundary object.

        Conservation of mass equation:
        m_in = m_out
        """
        # Arrange

        # Act
        equation_object = self.asset.get_internal_cont_equation()

        # Assert
        np_testing.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    self.asset.matrix_index + CoreQuantity.MASS_FLOW_RATE,
                    self.asset.matrix_index
                    + CoreQuantity.MASS_FLOW_RATE
                    + NUMBER_OF_CORE_QUANTITIES,
                ]
            ),
        )
        np_testing.assert_array_equal(equation_object.coefficients, np.array([1.0, 1.0]))
        self.assertEqual(equation_object.rhs, 0.0)

    def test_get_internal_energy_equation(self) -> None:
        """Evaluate getting an internal energy equation for the boundary object.

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
                    self.asset.matrix_index + CoreQuantity.MASS_FLOW_RATE,
                    self.asset.matrix_index + CoreQuantity.INTERNAL_ENERGY,
                    self.asset.matrix_index
                    + CoreQuantity.MASS_FLOW_RATE
                    + NUMBER_OF_CORE_QUANTITIES,
                    self.asset.matrix_index
                    + CoreQuantity.INTERNAL_ENERGY
                    + NUMBER_OF_CORE_QUANTITIES,
                ]
            ),
        )
        np_testing.assert_array_equal(
            equation_object.coefficients,
            np.array(
                [
                    self.asset.prev_sol[CoreQuantity.INTERNAL_ENERGY],
                    self.asset.prev_sol[CoreQuantity.MASS_FLOW_RATE],
                    self.asset.prev_sol[CoreQuantity.INTERNAL_ENERGY + NUMBER_OF_CORE_QUANTITIES],
                    self.asset.prev_sol[CoreQuantity.MASS_FLOW_RATE + NUMBER_OF_CORE_QUANTITIES],
                ]
            ),
        )
        self.assertEqual(
            equation_object.rhs,
            self.asset.prev_sol[CoreQuantity.MASS_FLOW_RATE]
            * self.asset.prev_sol[CoreQuantity.INTERNAL_ENERGY]
            + self.asset.prev_sol[CoreQuantity.MASS_FLOW_RATE + NUMBER_OF_CORE_QUANTITIES]
            * self.asset.prev_sol[CoreQuantity.INTERNAL_ENERGY + NUMBER_OF_CORE_QUANTITIES]
            + self.asset.heat_flux,
        )

    def test_get_internal_pressure_loss_equation(self) -> None:
        """Evaluate getting an internal pressure loss equation for the boundary object.

        The equation is:
        - Pressure at inlet - Pressure at outlet - 2 * Loss coefficient * Mass flow rate *
        abs(Mass flow rate) = 0
        """
        # Arrange
        self.asset.prev_sol = np.array(
            [
                1.0,  # mass_flow_rate 0
                2.0,  # pressure 0
                3.0,  # internal energy 0
                4.0,  # mass_flow_rate 1
                5.0,  # pressure 1
                6.0,  # internal energy 1
            ]
        )
        self.asset.update_loss_coefficient()

        # Act
        equation_object = self.asset.get_internal_pressure_loss_equation()

        # Assert
        np_testing.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    self.asset.matrix_index + CoreQuantity.MASS_FLOW_RATE,
                    self.asset.matrix_index + CoreQuantity.PRESSURE,
                    self.asset.matrix_index + CoreQuantity.PRESSURE + NUMBER_OF_CORE_QUANTITIES,
                ]
            ),
        )
        np_testing.assert_array_equal(
            equation_object.coefficients,
            np.array(
                [
                    -2.0
                    * self.asset.loss_coefficient
                    * abs(self.asset.prev_sol[CoreQuantity.MASS_FLOW_RATE]),
                    -1.0,
                    1.0,
                ]
            ),
        )
        self.assertEqual(
            equation_object.rhs,
            -self.asset.loss_coefficient
            * self.asset.prev_sol[CoreQuantity.MASS_FLOW_RATE]
            * abs(self.asset.prev_sol[CoreQuantity.MASS_FLOW_RATE]),
        )

    def test_internal_energy_equation_refreshes_solution_and_heat(self) -> None:
        self.asset.set_matrix_index(18)
        for flow_0, energy_0, flow_1, energy_1, heat in (
            (2.0, 100.0, -2.0, 90.0, 5.0),
            (-3.0, 80.0, 3.0, 110.0, -7.0),
            (0.0, 70.0, 0.0, 120.0, 0.0),
        ):
            with self.subTest(flow_0=flow_0):
                self.asset.prev_sol = np.array(
                    [flow_0, 10000.0, energy_0, flow_1, 20000.0, energy_1]
                )
                with patch.object(self.asset, "update_heat_supplied") as update_heat:
                    update_heat.side_effect = lambda heat=heat: setattr(
                        self.asset, "heat_flux", heat
                    )
                    equation = self.asset.get_internal_energy_equation()
                update_heat.assert_called_once_with()
                np_testing.assert_array_equal(equation.indices, [18, 20, 21, 23])
                np_testing.assert_array_equal(
                    equation.coefficients, [energy_0, flow_0, energy_1, flow_1]
                )
                self.assertEqual(equation.rhs, flow_0 * energy_0 + flow_1 * energy_1 + heat)

    def test_internal_energy_equation_preserves_index_override(self) -> None:
        class ReorderedFallType(FallType):
            def get_index_matrix(
                self,
                core_quantity: CoreQuantity,
                connection_point: int,
                use_relative_indexing: bool,
            ) -> int:
                offsets = {
                    CoreQuantity.INTERNAL_ENERGY: 0,
                    CoreQuantity.PRESSURE: 1,
                    CoreQuantity.MASS_FLOW_RATE: 2,
                }
                return (
                    offsets[core_quantity]
                    + 3 * connection_point
                    + (0 if use_relative_indexing else self.matrix_index)
                )

        asset = ReorderedFallType("reordered", "reordered")
        asset.set_matrix_index(12)
        asset.prev_sol = np.array([100.0, 10000.0, 2.0, 80.0, 20000.0, -2.0])
        equation = asset.get_internal_energy_equation()
        np_testing.assert_array_equal(equation.indices, [14, 12, 17, 15])
        np_testing.assert_array_equal(equation.coefficients, [100.0, 2.0, 80.0, -2.0])
        self.assertEqual(equation.rhs, 40.0)

    def test_get_internal_pressure_loss_equation_linearized_discharge(self) -> None:
        """Evaluate getting an internal pressure loss equation for the boundary object.

        The equation is:
        - Pressure at inlet - Pressure at outlet - 2 * Loss coefficient * Mass flow rate *
        abs(Mass flow rate) = 0
        """
        # Arrange
        self.asset.prev_sol = np.array([0.0, 2.0, 3.0, 0.0, 5.0, 6.0])
        self.asset.update_loss_coefficient()

        # Act
        equation_object = self.asset.get_internal_pressure_loss_equation()

        # Assert
        np_testing.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    self.asset.matrix_index + CoreQuantity.MASS_FLOW_RATE,
                    self.asset.matrix_index + CoreQuantity.PRESSURE,
                    self.asset.matrix_index + CoreQuantity.PRESSURE + NUMBER_OF_CORE_QUANTITIES,
                ]
            ),
        )
        np_testing.assert_array_equal(
            equation_object.coefficients,
            np.array([-2.0 * self.asset.loss_coefficient * 1e-5, -1.0, 1.0]),
        )
        self.assertEqual(
            equation_object.rhs,
            -self.asset.loss_coefficient * 1e-5 * self.asset.prev_sol[CoreQuantity.MASS_FLOW_RATE],
        )

    @patch.object(FallType, "get_internal_energy_equation")
    def test_get_thermal_equations_higher_than_massflow_threshold(self, mock_energy_eq) -> None:
        """Evaluate thermal equations higher than threshold massflow.

        The equations are:
        mIE_in - mIE_out = 0
        """
        # Arrange
        connection_point = 0
        self.asset.prev_sol[
            CoreQuantity.MASS_FLOW_RATE + NUMBER_OF_CORE_QUANTITIES * connection_point
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
            CoreQuantity.MASS_FLOW_RATE + NUMBER_OF_CORE_QUANTITIES * connection_point
        ] = (self.asset.massflow_zero_limit * 0.1)

        # Act
        self.asset.get_thermal_equations(connection_point=connection_point)

        # Assert
        self.assertEqual(mock_energy_eq.call_count, 1)

    @patch.object(FallType, "get_press_to_node_equation")
    def test_get_press_to_node_equation(self, mock_press_to_node_eq) -> None:
        """Evaluate getting pressure to node equations for the boundary object.

        The equations are:
        - Pressure at the boundary - Pressure at the node = 0
        """
        # Arrange
        connection_point = 0

        # Act
        self.asset.get_press_to_node_equation(connection_point=connection_point)

        # Assert
        self.assertEqual(mock_press_to_node_eq.call_count, 1)
