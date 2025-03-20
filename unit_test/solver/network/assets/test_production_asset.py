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

"""Test Junction entities."""
import unittest
from uuid import uuid4

import numpy.testing as npt

from omotes_simulator_core.solver.matrix.index_core_quantity import index_core_quantity
from omotes_simulator_core.solver.network.assets.node import Node
from omotes_simulator_core.solver.network.assets.production_asset import HeatBoundary
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


class HeatBoundaryTest(unittest.TestCase):
    """Testcase for HeatBoundary class."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Create a HeatBoundary object
        self.asset = HeatBoundary(
            name=str(uuid4()),
            _id=str(uuid4()),
        )
        # Create supply, connection_point:0 and return node, connection_point:1
        self.supply_node = Node(name=str(uuid4()), _id=str(uuid4()))
        self.return_node = Node(name=str(uuid4()), _id=str(uuid4()))
        # Connect the nodes to the asset
        self.asset.connect_node(node=self.supply_node, connection_point=0)
        self.asset.connect_node(node=self.return_node, connection_point=1)

    def test_production_asset_get_equations(self) -> None:
        """Evaluate the get_equations method."""
        # Arrange
        # Act
        equations = self.asset.get_equations()
        # Assert
        self.assertEqual(len(equations), self.asset.number_of_unknowns)

    def test_pre_scribe_mass_flow(self) -> None:
        """Test the pre_scribe_mass_flow attribute."""
        # Arrange
        self.asset.pre_scribe_mass_flow = True
        self.asset.mass_flow_rate_set_point = 20.0  # kg/s
        connection_point_id = 1

        # Act
        equation_object = self.asset.get_pre_scribe_mass_flow_or_pressure_equations(
            connection_point=connection_point_id
        )

        # Assert
        self.assertTrue(self.asset.pre_scribe_mass_flow)
        self.assertEqual(self.asset.mass_flow_rate_set_point, 20.0)
        self.assertEqual(equation_object.rhs, 20.0)
        self.assertTrue(all(equation_object.coefficients == [1.0]))

    def test_pre_scribe_pressure(self) -> None:
        """Test the pre_scribe_mass_flow attribute.

        The pressure is prescribed at the connection point.
        """
        # Arrange
        self.asset.pre_scribe_mass_flow = False
        self.asset.set_pressure = 10000.0  # Pa
        connection_point_id = 1

        # Act
        equation_object = self.asset.get_pre_scribe_mass_flow_or_pressure_equations(
            connection_point=connection_point_id
        )

        # Assert
        self.assertFalse(self.asset.pre_scribe_mass_flow)
        self.assertEqual(self.asset.set_pressure, 10000.0)
        self.assertEqual(equation_object.rhs, 10000.0)
        self.assertTrue(all(equation_object.coefficients == [1.0]))

    def test_pre_scribe_non_existing_connection_point(self) -> None:
        """Test the pre_scribe_mass_flow attribute.

        Check error handling when the connection point does not exist.
        """
        # Arrange
        connection_point_id = 2

        # Act
        with self.assertRaises(IndexError) as cm:
            self.asset.get_pre_scribe_mass_flow_or_pressure_equations(
                connection_point=connection_point_id
            )

        # Assert
        self.assertIsInstance(cm.exception, IndexError)
        self.assertEqual(cm.exception.args[0], "The connection point is not available.")

    def test_thermal_equation_no_discharge(self) -> None:
        """Test the thermal equation for a connection point of the asset.

        Check handling of zero mass flow rate (IE1 == IE2).
        """
        # Arrange
        connection_point_id = 0

        # Act
        equation_object = self.asset.get_thermal_equations(connection_point=connection_point_id)

        # Assert
        npt.assert_array_equal(
            equation_object.indices,
            [index_core_quantity.internal_energy, index_core_quantity.internal_energy],
        )
        npt.assert_array_equal(equation_object.coefficients, [1.0, -1.0])
        self.assertEqual(equation_object.rhs, 0.0)

    def test_thermal_equation_with_discharge(self) -> None:
        """Test the thermal equation for a connection point of the asset.

        Check handling of non-zero mass flow rate (IE1 != IE2).
        """
        # Arrange
        connection_point_id = 1
        self.asset.prev_sol[
            index_core_quantity.mass_flow_rate
            + connection_point_id * index_core_quantity.number_core_quantities
        ] = 1.0

        # Act
        equation_object = self.asset.get_thermal_equations(connection_point=connection_point_id)

        # Assert
        npt.assert_array_equal(
            equation_object.indices,
            [
                index_core_quantity.internal_energy
                + connection_point_id * index_core_quantity.number_core_quantities
            ],
        )
        npt.assert_array_equal(equation_object.coefficients, [1.0])
        self.assertEqual(equation_object.rhs, fluid_props.get_ie(self.asset.out_temperature))
