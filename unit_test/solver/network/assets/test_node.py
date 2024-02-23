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

"""Test Node asset of the solver class."""
import unittest
from unittest.mock import patch
from uuid import uuid4

import numpy as np
import numpy.testing as np_test

from simulator_core.solver.matrix.core_enum import NUMBER_CORE_QUANTITIES, IndexEnum
from simulator_core.solver.network.assets.node import Node
from simulator_core.solver.network.assets.production_asset import ProductionAsset
from simulator_core.solver.utils.fluid_properties import fluid_props


class NodeTest(unittest.TestCase):
    """Testcase for Node class."""

    def test_init(self) -> None:
        """Test the __init__ method of the Node class."""
        # arrange
        asset_name = uuid4()
        number_of_unknowns = 2
        height = 10.0
        initial_temperature = 20.0
        set_pressure = 100000.0

        # act
        asset = Node(
            name=asset_name,
            number_of_unknowns=number_of_unknowns,
            height=height,
            initial_temperature=initial_temperature,
            set_pressure=set_pressure,
        )  # act

        # assert
        self.assertEqual(asset.name, asset_name)
        self.assertEqual(asset.number_of_unknowns, number_of_unknowns)
        self.assertEqual(asset.height, height)
        self.assertEqual(asset.initial_temperature, initial_temperature)
        self.assertEqual(asset.set_pressure, set_pressure)
        self.assertEqual(asset.connected_assets, [])

    def test_connect_asset(self) -> None:
        """Test the connect_asset method of the Node class."""
        # arrange
        asset_name = uuid4()
        main_asset = Node(name=asset_name)
        connected_asset = ProductionAsset(name=uuid4())
        connection_id = 0

        # act
        main_asset.connect_asset(asset=connected_asset, con_point=connection_id)  # act

        # assert
        self.assertEqual(main_asset.connected_assets, [(connected_asset, connection_id)])

    def test_connect_asset_with_invalid_connection_id(self) -> None:
        """Test the connect_asset method of the Node class with invalid connection_id."""
        # arrange
        asset_name = uuid4()
        main_asset = Node(name=asset_name)
        connected_asset = ProductionAsset(name=uuid4())
        connection_id = 2

        # act
        with self.assertRaises(ValueError) as cm:
            main_asset.connect_asset(asset=connected_asset, con_point=connection_id)

        # assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            cm.exception.args[0],
            f"Connection point {connection_id} does not exist on asset {connected_asset.name}.",
        )

    def test_get_equations(self) -> None:
        """Test the get_equations method of the Node class."""
        # arrange
        asset_name = uuid4()
        asset = Node(name=asset_name)

        # act
        equations = asset.get_equations()

        # assert

    def test_add_node_cont_equation(self) -> None:
        """Test the add_node_cont_equation method of the Node class."""
        # arrange
        asset_name = uuid4()
        asset = Node(name=asset_name)

        # act
        equation_object = asset.add_node_cont_equation()

        # assert
        self.assertEqual(equation_object.indices, [asset.matrix_index + IndexEnum.discharge])
        self.assertEqual(equation_object.coefficients, [1.0])
        self.assertEqual(equation_object.rhs, 0.0)

    def test_add_node_cont_equation_with_additional_asset(self) -> None:
        """Test the add_node_cont_equation method of the Node class with additional asset."""
        # arrange
        asset_name = uuid4()
        asset = Node(name=asset_name)
        connected_asset = ProductionAsset(name=uuid4())
        connection_point = 0
        asset.connect_asset(asset=connected_asset, con_point=connection_point)

        # act
        equation_object = asset.add_node_cont_equation()  # act

        # assert
        np_test.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    asset.matrix_index + IndexEnum.discharge,
                    connected_asset.matrix_index + IndexEnum.discharge,
                ]
            ),
        )
        np_test.assert_array_equal(equation_object.coefficients, np.array([1.0, 1.0]))
        self.assertEqual(equation_object.rhs, 0.0)

    def test_add_discharge_equation(self) -> None:
        """Test the add_discharge_equation method of the Node class."""
        # arrange
        asset_name = uuid4()
        asset = Node(name=asset_name)

        # act
        equation_object = asset.add_discharge_equation()

        # assert
        np_test.assert_array_equal(
            equation_object.indices, np.array([asset.matrix_index + IndexEnum.discharge])
        )
        np_test.assert_array_equal(equation_object.coefficients, np.array([1.0]))
        self.assertEqual(equation_object.rhs, 0.0)

    def test_add_pressure_set_equation(self) -> None:
        """Test the add_pressure_set_equation method of the Node class."""
        # arrange
        asset_name = uuid4()
        asset = Node(name=asset_name, set_pressure=5.0)

        # act
        equation_object = asset.add_pressure_set_equation()

        # assert
        np_test.assert_array_equal(
            equation_object.indices, np.array([asset.matrix_index + IndexEnum.pressure])
        )
        np_test.assert_array_equal(equation_object.coefficients, np.array([1.0]))
        self.assertEqual(equation_object.rhs, asset.set_pressure)

    def test_set_temperature_equation(self) -> None:
        """Test the set_temperature_equation method of the Node class."""
        # arrange
        asset_name = uuid4()
        asset = Node(name=asset_name, initial_temperature=275.0)

        # act
        equation_object = asset.set_temperature_equation()

        # assert
        np_test.assert_array_equal(
            equation_object.indices, np.array([asset.matrix_index + IndexEnum.internal_energy])
        )
        np_test.assert_array_equal(equation_object.coefficients, np.array([1.0]))
        self.assertEqual(equation_object.rhs, fluid_props.get_ie(asset.initial_temperature))

    def test_is_connected_true(self) -> None:
        """Test the is_connected method of the Node class."""
        # arrange
        asset_name = uuid4()
        asset = Node(name=asset_name)
        connected_asset = ProductionAsset(name=uuid4())
        connection_point = 0

        # act
        asset.connect_asset(asset=connected_asset, con_point=connection_point)

        # assert
        self.assertTrue(asset.is_connected())

    def test_is_connected_false(self) -> None:
        """Test the is_connected method of the Node class."""
        # arrange
        asset_name = uuid4()
        asset = Node(name=asset_name)

        # act

        # assert
        self.assertFalse(asset.is_connected())


class NodeTestEnergyEquation(unittest.TestCase):
    """Testcase for Node class energy equation."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Asset properties
        self.initial_temperature = 275.0
        self.internal_energy = fluid_props.get_ie(self.initial_temperature)
        self.discharge = 1.0
        # Create base asset
        self.asset = Node(name=uuid4(), initial_temperature=self.initial_temperature)
        # Create connected asset
        self.connected_asset = ProductionAsset(name=uuid4())
        self.connected_asset.set_matrix_index(NUMBER_CORE_QUANTITIES)
        self.connection_point = 0
        # Create connected asset on other connection point
        self.connected_asset_2 = ProductionAsset(name=uuid4())
        self.connected_asset_2.set_matrix_index(NUMBER_CORE_QUANTITIES * 2)
        self.connection_point_2 = 1

    def test_add_energy_equation(self) -> None:
        """Test the add_energy_equation method of the Node class."""
        # arrange
        self.asset.prev_sol[IndexEnum.discharge] = self.discharge
        self.asset.prev_sol[IndexEnum.internal_energy] = self.internal_energy

        # act
        equation_object = self.asset.add_energy_equation()

        # assert
        np_test.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    self.asset.matrix_index + IndexEnum.discharge,
                    self.asset.matrix_index + IndexEnum.internal_energy,
                ]
            ),
        )
        np_test.assert_array_equal(
            equation_object.coefficients, np.array([self.discharge, self.internal_energy])
        )
        self.assertEqual(equation_object.rhs, self.internal_energy * self.discharge)

    def test_add_energy_equation_with_additional_asset(self) -> None:
        """Test the add_energy_equation method of the Node class with additional asset."""
        # arrange
        self.asset.connect_asset(asset=self.connected_asset, con_point=self.connection_point)
        self.asset.prev_sol[IndexEnum.discharge] = self.discharge
        self.asset.prev_sol[IndexEnum.internal_energy] = self.internal_energy
        self.connected_asset.prev_sol[IndexEnum.discharge] = -self.discharge
        self.connected_asset.prev_sol[IndexEnum.internal_energy] = self.internal_energy

        # act
        equation_object = self.asset.add_energy_equation()

        # assert
        np_test.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    self.asset.matrix_index + IndexEnum.discharge,
                    self.asset.matrix_index + IndexEnum.internal_energy,
                    self.connected_asset.matrix_index
                    + IndexEnum.discharge
                    + NUMBER_CORE_QUANTITIES * self.connection_point,
                    self.connected_asset.matrix_index
                    + IndexEnum.internal_energy
                    + NUMBER_CORE_QUANTITIES * self.connection_point,
                ]
            ),
        )
        np_test.assert_array_equal(
            equation_object.coefficients,
            np.array([self.discharge, self.internal_energy, -self.discharge, self.internal_energy]),
        )
        self.assertEqual(
            equation_object.rhs,
            np.prod(self.asset.prev_sol) + np.prod(self.connected_asset.prev_sol),
        )

    @patch.object(Node, "add_energy_equation")
    def test_add_energy_equations_with_positive_negative_flow(self, mock_method) -> None:
        """Test the add_energy_equations method of the Node class."""
        # arrange
        # - Outflow
        self.connected_asset.prev_sol[
            IndexEnum.discharge + self.connection_point * NUMBER_CORE_QUANTITIES
        ] = +self.discharge
        self.asset.connect_asset(asset=self.connected_asset, con_point=self.connection_point)
        # - Inflow
        self.connected_asset_2.prev_sol[
            IndexEnum.discharge + self.connection_point_2 * NUMBER_CORE_QUANTITIES
        ] = -self.discharge
        self.asset.connect_asset(asset=self.connected_asset_2, con_point=self.connection_point_2)

        # act
        self.asset.add_energy_equations()

        # assert
        mock_method.assert_called_once()

    @patch.object(Node, "set_temperature_equation")
    def test_add_energy_equations_with_all_positive_flow(self, mock_method) -> None:
        """Test the add_energy_equations method of the Node class."""
        # arrange
        # - Outflow
        self.connected_asset.prev_sol[
            IndexEnum.discharge + self.connection_point * NUMBER_CORE_QUANTITIES
        ] = +self.discharge
        self.asset.connect_asset(asset=self.connected_asset, con_point=self.connection_point)
        # - Inflow
        self.connected_asset_2.prev_sol[
            IndexEnum.discharge + self.connection_point_2 * NUMBER_CORE_QUANTITIES
        ] = +self.discharge
        self.asset.connect_asset(asset=self.connected_asset_2, con_point=self.connection_point_2)

        # act
        self.asset.add_energy_equations()

        # assert
        mock_method.assert_called_once()

    @patch.object(Node, "set_temperature_equation")
    def test_add_energy_equations_with_all_negative_flow(self, mock_method) -> None:
        """Test the add_energy_equations method of the Node class."""
        # arrange
        # - Outflow
        self.connected_asset.prev_sol[
            IndexEnum.discharge + self.connection_point * NUMBER_CORE_QUANTITIES
        ] = -self.discharge
        self.asset.connect_asset(asset=self.connected_asset, con_point=self.connection_point)
        # - Inflow
        self.connected_asset_2.prev_sol[
            IndexEnum.discharge + self.connection_point_2 * NUMBER_CORE_QUANTITIES
        ] = -self.discharge
        self.asset.connect_asset(asset=self.connected_asset_2, con_point=self.connection_point_2)

        # act
        self.asset.add_energy_equations()

        # assert
        mock_method.assert_called_once()

    @patch.object(Node, "set_temperature_equation")
    def test_add_energy_equations_with_no_flow(self, mock_method) -> None:
        """Test the add_energy_equations method of the Node class."""
        # arrange
        # - Outflow
        self.connected_asset.prev_sol[
            IndexEnum.discharge + self.connection_point * NUMBER_CORE_QUANTITIES
        ] = 0.0
        self.asset.connect_asset(asset=self.connected_asset, con_point=self.connection_point)
        # - Inflow
        self.connected_asset_2.prev_sol[
            IndexEnum.discharge + self.connection_point_2 * NUMBER_CORE_QUANTITIES
        ] = 0.0
        self.asset.connect_asset(asset=self.connected_asset_2, con_point=self.connection_point_2)

        # act
        self.asset.add_energy_equations()

        # assert
        mock_method.assert_called_once()
