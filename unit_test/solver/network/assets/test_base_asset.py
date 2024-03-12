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
from simulator_core.solver.network.assets.base_asset import BaseAsset
from simulator_core.solver.network.assets.node import Node
from simulator_core.solver.utils.fluid_properties import fluid_props


class BaseAssetTest(unittest.TestCase):
    """Testcase for BaseAsset class."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Create a BaseAsset object
        self.asset = BaseAsset(
            name=uuid4(),
        )
        # Create supply, connection_point:0 and return node, connection_point:1
        self.supply_node = Node(name=uuid4())
        self.return_node = Node(name=uuid4())

    def test_base_asset_connect_node(self) -> None:
        """Test the connect_node method."""
        # Arrange

        # Act
        self.asset.connect_node(node=self.supply_node, connection_point=0)
        self.asset.connect_node(node=self.return_node, connection_point=1)

        # Assert
        assert self.asset.connected_nodes[0] == self.supply_node
        assert self.asset.connected_nodes[1] == self.return_node

    def test_base_asset_connect_node_already_connected(self) -> None:
        """Test the connect_node method with already connected node."""
        # Arrange
        connection_point_id = 0
        self.asset.connect_node(node=self.supply_node, connection_point=connection_point_id)

        # Act
        with self.assertRaises(ValueError) as cm:
            self.asset.connect_node(node=self.supply_node, connection_point=connection_point_id)

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            str(cm.exception),
            (
                f" connection point {connection_point_id}  of asset {self.asset.name} "
                f" already connected to a node"
            ),
        )

    def test_base_asset_check_connection_point_valid(self) -> None:
        """Test the check_connection_point_valid method."""
        # Arrange
        connection_point_id = 0

        # Act
        result = self.asset.check_connection_point_valid(connection_point=connection_point_id)

        # Assert
        assert result is True

    def test_base_asset_check_connection_point_not_valid(self) -> None:
        """Test the check_connection_point_valid method."""
        # Arrange
        connection_point_id = 2

        # Act
        with self.assertRaises(IndexError) as cm:
            self.asset.check_connection_point_valid(connection_point=connection_point_id)

        # Assert
        self.assertIsInstance(cm.exception, IndexError)
        self.assertEqual(
            str(cm.exception),
            (
                f"Asset {self.asset.name} only has {self.asset.number_of_connection_point - 1}. "
                f"{connection_point_id} is too high"
            ),
        )

    def test_base_is_connected(self) -> None:
        """Test the is_connected method."""
        # Arrange
        self.asset.connect_node(node=self.supply_node, connection_point=0)

        # Act
        result = self.asset.is_connected(connection_point=0)

        # Assert
        assert result is True

    def test_base_is_not_connected(self) -> None:
        """Test the is_connected method."""
        # Arrange

        # Act
        result = self.asset.is_connected(connection_point=0)

        # Assert
        assert result is False

    def test_base_get_connected_node(self) -> None:
        """Test the get_connected_node method."""
        # Arrange
        self.asset.connect_node(node=self.supply_node, connection_point=0)

        # Act
        result = self.asset.get_connected_node(connection_point=0)

        # Assert
        assert result is self.supply_node

    def test_base_is_all_connected(self) -> None:
        """Test the is_all_connected method."""
        # Arrange
        self.asset.connect_node(node=self.supply_node, connection_point=0)
        self.asset.connect_node(node=self.return_node, connection_point=1)

        # Act
        result = self.asset.is_all_connected()

        # Assert
        assert result is True

    def test_base_is_not_all_connected(self) -> None:
        """Test the is_all_connected method."""
        # Arrange
        self.asset.connect_node(node=self.supply_node, connection_point=0)

        # Act
        result = self.asset.is_all_connected()

        # Assert
        assert result is False

    def test_base_add_thermal_equations_with_discharge(self) -> None:
        """Test the add_thermal_equations method.

        The discharge at the connection point of the prev_sol is greater than 0.
        """
        # Arrange
        connection_point_id = 0
        self.asset.connect_node(node=self.supply_node, connection_point=connection_point_id)
        self.asset.prev_sol[IndexEnum.discharge + connection_point_id * NUMBER_CORE_QUANTITIES] = (
            1.0
        )

        # Act
        equation_object = self.asset.add_thermal_equations(connection_point=connection_point_id)

        # Assert
        assert equation_object.rhs == fluid_props.get_ie(self.asset.supply_temperature)
        assert all(equation_object.coefficients == [1.0])
        assert all(
            equation_object.indices
            == [IndexEnum.internal_energy + connection_point_id * NUMBER_CORE_QUANTITIES]
        )

    def test_base_add_thermal_equations_no_discharge(self) -> None:
        """Test the add_thermal_equations method.

        The discharge at the connection point of the prev_sol is 0.
        """
        # Arrange
        connection_point_id = 0
        self.asset.connect_node(node=self.supply_node, connection_point=connection_point_id)

        # Act
        equation_object = self.asset.add_thermal_equations(connection_point=connection_point_id)

        # Assert
        assert equation_object.rhs == 0.0
        assert all(equation_object.coefficients == [1.0, -1.0])
        assert all(
            equation_object.indices == [IndexEnum.internal_energy, IndexEnum.internal_energy]
        )

    def test_base_add_thermal_equations_no_discharge_not_connected(self) -> None:
        """Test the add_thermal_equations method.

        The discharge at the connection point of the prev_sol is 0.
        """
        # Arrange
        connection_point_id = 0

        # Act
        with self.assertRaises(ValueError) as cm:
            self.asset.add_thermal_equations(connection_point=connection_point_id)

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            str(cm.exception),
            (
                f"Connection point {connection_point_id} of asset {self.asset.name} "
                f"is not connected to a node."
            ),
        )

    def test_base_add_press_to_node_equation(self) -> None:
        """Test the add_press_to_node_equations method."""
        # Arrange
        connection_point_id = 0
        self.asset.connect_node(node=self.supply_node, connection_point=connection_point_id)

        # Act
        equation_object = self.asset.add_press_to_node_equation(
            connection_point=connection_point_id
        )

        # Assert
        assert equation_object.rhs == 0.0
        assert all(equation_object.coefficients == [1.0, -1.0])
        assert all(
            equation_object.indices
            == [
                IndexEnum.pressure + connection_point_id * NUMBER_CORE_QUANTITIES,
                self.asset.connected_nodes[connection_point_id].matrix_index + IndexEnum.pressure,
            ]
        )

    def test_base_add_press_to_node_equation_not_connected(self) -> None:
        """Test the add_press_to_node_equations method."""
        # Arrange
        connection_point_id = 0

        # Act
        with self.assertRaises(ValueError) as cm:
            self.asset.add_press_to_node_equation(connection_point=connection_point_id)

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            str(cm.exception),
            (
                f"Connection point {connection_point_id} of asset {self.asset.name} "
                f"is not connected to a node."
            ),
        )

    def test_base_get_pressure(self) -> None:
        """Test the get_pressure method."""
        # Arrange
        connection_point_id = 0
        self.asset.prev_sol[IndexEnum.pressure + connection_point_id * NUMBER_CORE_QUANTITIES] = (
            10000.0
        )

        # Act
        result = self.asset.get_pressure(connection_point=connection_point_id)

        # Assert
        assert result == 10000.0

    def test_base_get_mass_flow_rate(self) -> None:
        """Test the get_mass_flow_rate method."""
        # Arrange
        connection_point_id = 0
        self.asset.prev_sol[IndexEnum.discharge + connection_point_id * NUMBER_CORE_QUANTITIES] = (
            1.0
        )

        # Act
        result = self.asset.get_mass_flow_rate(connection_point=connection_point_id)

        # Assert
        assert result == 1.0

    def test_base_get_temperature(self) -> None:
        """Test the get_temperature method."""
        # Arrange
        connection_point_id = 0
        temperature = 300.0
        self.asset.prev_sol[
            IndexEnum.internal_energy + connection_point_id * NUMBER_CORE_QUANTITIES
        ] = fluid_props.get_ie(temperature)

        # Act
        result = self.asset.get_temperature(connection_point=connection_point_id)

        # Assert
        assert result == temperature
