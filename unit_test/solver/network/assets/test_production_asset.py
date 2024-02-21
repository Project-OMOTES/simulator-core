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

from simulator_core.solver.matrix.core_enum import NUMBER_CORE_QUANTITIES, IndexEnum
from simulator_core.solver.network.assets.node import Node
from simulator_core.solver.network.assets.production_asset import ProductionAsset
from simulator_core.solver.utils.fluid_properties import fluid_props


class ProductionAssetTest(unittest.TestCase):
    """Testcase for ProductionAsset class."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Create a ProductionAsset object
        self.asset = ProductionAsset(
            name=uuid4(),
        )
        # Create supply, connection_point:0 and return node, connection_point:1
        self.supply_node = Node(name=uuid4())
        self.return_node = Node(name=uuid4())
        # Connect the nodes to the asset
        self.asset.connect_node(node=self.supply_node, connection_point=0)
        self.asset.connect_node(node=self.return_node, connection_point=1)

    def test_production_asset_get_equations(self) -> None:
        """Evaluate the get_equations method."""
        # Arrange
        # Act
        equations = self.asset.get_equations()
        # Assert
        assert len(equations) == self.asset.number_of_unknowns

    def test_pre_scribe_mass_flow(self) -> None:
        """Test the pre_scribe_mass_flow attribute."""
        # Arrange
        self.asset.pre_scribe_mass_flow = True
        self.asset.mass_flow_rate_set_point = 20.0  # kg/s
        connection_point_id = 1

        # Act
        equation_object = self.asset.add_pre_scribe_equation(connection_point=connection_point_id)

        # Assert
        assert self.asset.pre_scribe_mass_flow is True
        assert self.asset.mass_flow_rate_set_point == 20.0
        assert equation_object.rhs == 20.0
        assert all(equation_object.coefficients == [1.0])

    def test_pre_scribe_pressure(self) -> None:
        """Test the pre_scribe_mass_flow attribute.

        The pressure is prescribed at the connection point.
        """
        # Arrange
        self.asset.pre_scribe_mass_flow = False
        self.asset.set_pressure = 10000.0  # Pa
        connection_point_id = 1

        # Act
        equation_object = self.asset.add_pre_scribe_equation(connection_point=connection_point_id)

        # Assert
        assert self.asset.pre_scribe_mass_flow is False
        assert self.asset.set_pressure == 10000.0
        assert equation_object.rhs == 10000.0
        assert all(equation_object.coefficients == [1.0])

    def test_pre_scribe_non_existing_connection_point(self) -> None:
        """Test the pre_scribe_mass_flow attribute.

        Check error handling when the connection point does not exist.
        """
        # Arrange
        connection_point_id = 2

        # Act
        with self.assertRaises(IndexError) as cm:
            self.asset.add_pre_scribe_equation(connection_point=connection_point_id)

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
        equation_object = self.asset.add_thermal_equations(connection_point=connection_point_id)

        # Assert
        assert all(
            equation_object.indices == [IndexEnum.internal_energy, IndexEnum.internal_energy]
        )
        assert all(equation_object.coefficients == [1.0, -1.0])
        assert equation_object.rhs == 0.0

    def test_thermal_equation_with_discharge(self) -> None:
        """Test the thermal equation for a connection point of the asset.

        Check handling of non-zero mass flow rate (IE1 != IE2).
        """
        # Arrange
        connection_point_id = 1
        self.asset.prev_sol[IndexEnum.discharge + connection_point_id * NUMBER_CORE_QUANTITIES] = (
            1.0
        )

        # Act
        equation_object = self.asset.add_thermal_equations(connection_point=connection_point_id)

        # Assert
        assert all(
            equation_object.indices
            == [IndexEnum.internal_energy + connection_point_id * NUMBER_CORE_QUANTITIES]
        )
        assert all(equation_object.coefficients == [1.0])
        assert equation_object.rhs == fluid_props.get_ie(self.asset.supply_temperature)
