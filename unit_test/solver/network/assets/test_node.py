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

from omotes_simulator_core.solver.matrix.index_core_quantity import index_core_quantity
from omotes_simulator_core.solver.network.assets.node import Node
from omotes_simulator_core.solver.network.assets.production_asset import HeatBoundary
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


class NodeTest(unittest.TestCase):
    """Testcase for Node class."""

    def setUp(self):
        """Set up the test case."""
        self.node_name = str(uuid4())
        self.node = Node(name=self.node_name, _id=self.node_name)

    def test_init(self) -> None:
        """Test the __init__ method of the Node class."""
        # arrange
        number_of_unknowns = 2
        height = 10.0
        initial_temperature = 20.0
        set_pressure = 100000.0

        # act
        node = Node(
            name=self.node_name,
            _id=self.node_name,
            number_of_unknowns=number_of_unknowns,
            height=height,
            initial_temperature=initial_temperature,
            set_pressure=set_pressure,
        )  # act

        # assert
        self.assertEqual(node.name, self.node_name)
        self.assertEqual(node.number_of_unknowns, number_of_unknowns)
        self.assertEqual(node.height, height)
        self.assertEqual(node.initial_temperature, initial_temperature)
        self.assertEqual(node.set_pressure, set_pressure)
        self.assertEqual(node.connected_assets, [])

    def test_connect_asset(self) -> None:
        """Test the connect_asset method of the Node class."""
        # arrange
        connected_asset = HeatBoundary(name=str(uuid4()), _id=str(uuid4()))
        connection_id = 0

        # act
        self.node.connect_asset(asset=connected_asset, connection_point=connection_id)  # act

        # assert
        self.assertEqual(self.node.connected_assets, [(connected_asset, connection_id)])

    def test_connect_asset_with_invalid_connection_id(self) -> None:
        """Test the connect_asset method of the Node class with invalid connection_id."""
        # arrange
        connected_asset = HeatBoundary(name=str(uuid4()), _id=str(uuid4()))
        connection_id = 2

        # act
        with self.assertRaises(ValueError) as cm:
            self.node.connect_asset(asset=connected_asset, connection_point=connection_id)

        # assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            cm.exception.args[0],
            f"Connection point {connection_id} does not exist on asset {connected_asset.name}.",
        )

    def test_get_equations_not_connected(self) -> None:
        """Test the get_equations method of the Node class."""
        # arrange

        # act
        with self.assertRaises(ValueError) as cm:
            self.node.get_equations()

        # assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            cm.exception.args[0], f"Node {self.node.name} " f"is not connected to any asset."
        )

    @patch.object(Node, "get_node_cont_equation")
    @patch.object(Node, "get_discharge_equation")
    @patch.object(Node, "get_energy_equations")
    @patch.object(Node, "set_temperature_equation")
    def test_get_equations_connected(
        self, temperature_patch, energy_patch, discharge_patch, continuity_patch
    ) -> None:
        """Test the get_equations method of the Node class when connected."""
        # arrange
        connected_asset = HeatBoundary(name=str(uuid4()), _id=str(uuid4()))
        connection_point = 0
        self.node.connect_asset(asset=connected_asset, connection_point=connection_point)

        # act
        equations = self.node.get_equations()  # act

        # assert
        continuity_patch.assert_called_once()
        discharge_patch.assert_called_once()
        energy_patch.assert_called_once()
        self.assertEqual(temperature_patch.call_count, 0)
        self.assertEqual(len(equations), 3)

    def test_get_node_cont_equation(self) -> None:
        """Test the get_node_cont_equation method of the Node class."""
        # arrange

        # act
        equation_object = self.node.get_node_cont_equation()

        # assert
        self.assertEqual(
            equation_object.indices, [self.node.matrix_index + index_core_quantity.mass_flow_rate]
        )
        self.assertEqual(equation_object.coefficients, [1.0])
        self.assertEqual(equation_object.rhs, 0.0)

    def test_get_node_cont_equation_with_additional_asset(self) -> None:
        """Test the get_node_cont_equation method of the Node class with additional asset."""
        # arrange
        connected_asset = HeatBoundary(name=str(uuid4()), _id=str(uuid4()))
        connection_point = 0
        self.node.connect_asset(asset=connected_asset, connection_point=connection_point)

        # act
        equation_object = self.node.get_node_cont_equation()  # act

        # assert
        np_test.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    self.node.matrix_index + index_core_quantity.mass_flow_rate,
                    connected_asset.matrix_index + index_core_quantity.mass_flow_rate,
                ]
            ),
        )
        np_test.assert_array_equal(equation_object.coefficients, np.array([1.0, 1.0]))
        self.assertEqual(equation_object.rhs, 0.0)

    def test_get_discharge_equation(self) -> None:
        """Test the get_discharge_equation method of the Node class."""
        # arrange

        # act
        equation_object = self.node.get_discharge_equation()

        # assert
        np_test.assert_array_equal(
            equation_object.indices,
            np.array([self.node.matrix_index + index_core_quantity.mass_flow_rate]),
        )
        np_test.assert_array_equal(equation_object.coefficients, np.array([1.0]))
        self.assertEqual(equation_object.rhs, 0.0)

    def test_get_pressure_set_equation(self) -> None:
        """Test the get_pressure_set_equation method of the Node class."""
        # arrange
        node_name = str(uuid4())
        node = Node(name=node_name, _id=node_name, set_pressure=5.0)

        # act
        equation_object = node.get_pressure_set_equation()

        # assert
        np_test.assert_array_equal(
            equation_object.indices, np.array([node.matrix_index + index_core_quantity.pressure])
        )
        np_test.assert_array_equal(equation_object.coefficients, np.array([1.0]))
        self.assertEqual(equation_object.rhs, node.set_pressure)

    def test_set_temperature_equation(self) -> None:
        """Test the set_temperature_equation method of the Node class."""
        # arrange
        node_name = str(uuid4())
        node = Node(name=node_name, _id=node_name, initial_temperature=275.0)

        # act
        equation_object = node.set_temperature_equation()

        # assert
        np_test.assert_array_equal(
            equation_object.indices,
            np.array([node.matrix_index + index_core_quantity.internal_energy]),
        )
        np_test.assert_array_equal(equation_object.coefficients, np.array([1.0]))
        self.assertEqual(equation_object.rhs, fluid_props.get_ie(node.initial_temperature))

    def test_is_connected_true(self) -> None:
        """Test the is_connected method of the Node class."""
        # arrange
        connected_asset = HeatBoundary(name=str(uuid4()), _id=str(uuid4()))
        connection_point = 0

        # act
        self.node.connect_asset(asset=connected_asset, connection_point=connection_point)

        # assert
        self.assertTrue(self.node.is_connected())

    def test_is_connected_false(self) -> None:
        """Test the is_connected method of the Node class."""
        # arrange

        # act

        # assert
        self.assertFalse(self.node.is_connected())


class NodeTestEnergyEquation(unittest.TestCase):
    """Testcase for Node class energy equation."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Asset properties
        self.initial_temperature = 275.0
        self.internal_energy = fluid_props.get_ie(self.initial_temperature)
        self.discharge = 1.0
        # Create base asset
        self.node = Node(
            name=str(uuid4()), _id=str(uuid4()), initial_temperature=self.initial_temperature
        )
        # Create connected asset
        self.connected_asset = HeatBoundary(name=str(uuid4()), _id=str(uuid4()))
        self.connected_asset.set_matrix_index(index_core_quantity.number_core_quantities)
        self.connection_point = 0
        # Create connected asset on other connection point
        self.connected_asset_2 = HeatBoundary(name=str(uuid4()), _id=str(uuid4()))
        self.connected_asset_2.set_matrix_index(index_core_quantity.number_core_quantities * 2)
        self.connection_point_2 = 1

    def test_get_energy_equation(self) -> None:
        """Test the get_energy_equation method of the Node class."""
        # arrange
        self.node.prev_sol[index_core_quantity.mass_flow_rate] = self.discharge
        self.node.prev_sol[index_core_quantity.internal_energy] = self.internal_energy

        # act
        equation_object = self.node.get_energy_equation()

        # assert
        np_test.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    self.node.matrix_index + index_core_quantity.mass_flow_rate,
                    self.node.matrix_index + index_core_quantity.internal_energy,
                ]
            ),
        )
        np_test.assert_array_equal(
            equation_object.coefficients, np.array([self.internal_energy, self.discharge])
        )
        self.assertEqual(equation_object.rhs, self.internal_energy * self.discharge)

    def test_get_energy_equation_with_additional_asset(self) -> None:
        """Test the get_energy_equation method of the Node class with additional node."""
        # arrange
        self.node.connect_asset(asset=self.connected_asset, connection_point=self.connection_point)
        self.node.prev_sol[index_core_quantity.mass_flow_rate] = self.discharge
        self.node.prev_sol[index_core_quantity.internal_energy] = self.internal_energy
        self.connected_asset.prev_sol[index_core_quantity.mass_flow_rate] = -self.discharge
        self.connected_asset.prev_sol[index_core_quantity.internal_energy] = self.internal_energy

        # act
        equation_object = self.node.get_energy_equation()

        # assert
        np_test.assert_array_equal(
            equation_object.indices,
            np.array(
                [
                    self.node.matrix_index + index_core_quantity.mass_flow_rate,
                    self.node.matrix_index + index_core_quantity.internal_energy,
                    self.connected_asset.matrix_index
                    + index_core_quantity.mass_flow_rate
                    + index_core_quantity.number_core_quantities * self.connection_point,
                    self.connected_asset.matrix_index
                    + index_core_quantity.internal_energy
                    + index_core_quantity.number_core_quantities * self.connection_point,
                ]
            ),
        )
        np_test.assert_array_equal(
            equation_object.coefficients,
            np.array(
                [
                    self.internal_energy,
                    self.discharge,
                    self.internal_energy,
                    -self.discharge,
                ]
            ),
        )
        self.assertEqual(
            equation_object.rhs,
            np.prod(self.node.prev_sol) + np.prod(self.connected_asset.prev_sol),
        )

    def test_initialize_energy_equation_is_called_once(self) -> None:
        """Test that the energy equation object is created only once and then reused."""
        # arrange
        self.node.connect_asset(asset=self.connected_asset, connection_point=self.connection_point)

        # act
        first_equation_object = self.node.get_energy_equation()
        with patch.object(Node, "initialize_energy_equation") as mock_initialize:
            second_equation_object = self.node.get_energy_equation()

        # assert
        mock_initialize.assert_not_called()
        self.assertIs(first_equation_object, second_equation_object)
        self.assertIs(first_equation_object, self.node.energy_equation_object)

    def test_get_energy_equation_updates_coefficients_and_rhs(self) -> None:
        """Test that a second call updates the coefficients and rhs with the new solution."""
        # arrange
        self.node.connect_asset(asset=self.connected_asset, connection_point=self.connection_point)
        self.node.prev_sol[index_core_quantity.mass_flow_rate] = self.discharge
        self.node.prev_sol[index_core_quantity.internal_energy] = self.internal_energy
        self.connected_asset.prev_sol[index_core_quantity.mass_flow_rate] = -self.discharge
        self.connected_asset.prev_sol[index_core_quantity.internal_energy] = self.internal_energy
        self.node.get_energy_equation()
        # Update the previous solution after the equation object has been initialized.
        self.node.prev_sol[index_core_quantity.mass_flow_rate] = 2.0 * self.discharge
        self.connected_asset.prev_sol[index_core_quantity.mass_flow_rate] = -2.0 * self.discharge

        # act
        equation_object = self.node.get_energy_equation()

        # assert
        np_test.assert_array_equal(
            equation_object.coefficients,
            np.array(
                [
                    self.internal_energy,
                    2.0 * self.discharge,
                    self.internal_energy,
                    -2.0 * self.discharge,
                ]
            ),
        )
        self.assertEqual(
            equation_object.rhs,
            np.prod(self.node.prev_sol) + np.prod(self.connected_asset.prev_sol),
        )

    def test_connect_asset_invalidates_energy_equation(self) -> None:
        """Test that connecting an asset invalidates the stored energy equation object."""
        # arrange
        self.node.connect_asset(asset=self.connected_asset, connection_point=self.connection_point)
        self.node.get_energy_equation()

        # act
        self.node.connect_asset(
            asset=self.connected_asset_2, connection_point=self.connection_point_2
        )

        # assert
        self.assertIsNone(self.node.energy_equation_object)
        self.assertEqual(len(self.node.get_energy_equation().indices), 6)

    def test_set_matrix_index_invalidates_energy_equation(self) -> None:
        """Test that setting the matrix index invalidates the stored energy equation object."""
        # arrange
        self.node.connect_asset(asset=self.connected_asset, connection_point=self.connection_point)
        self.node.get_energy_equation()
        new_matrix_index = index_core_quantity.number_core_quantities * 3

        # act
        self.node.set_matrix_index(new_matrix_index)

        # assert
        self.assertIsNone(self.node.energy_equation_object)
        self.assertEqual(
            self.node.get_energy_equation().indices[0],
            new_matrix_index + index_core_quantity.mass_flow_rate,
        )

    def test_initialize_energy_equation_with_invalid_index(self) -> None:
        """Test that an index outside the previous solution of an asset raises an error."""
        # arrange
        self.node.connect_asset(asset=self.connected_asset, connection_point=self.connection_point)
        self.connected_asset.prev_sol = np.zeros(1)

        # act
        with self.assertRaises(IndexError) as cm:
            self.node.initialize_energy_equation()

        # assert
        self.assertIn(self.connected_asset.name, cm.exception.args[0])

    def test_constant_equations_are_cached(self) -> None:
        """Test that the constant node equations are created once and then reused."""
        # arrange
        self.node.connect_asset(asset=self.connected_asset, connection_point=self.connection_point)

        # act
        first = [self.node.get_node_cont_equation(), self.node.get_discharge_equation()]
        second = [self.node.get_node_cont_equation(), self.node.get_discharge_equation()]

        # assert
        for first_equation, second_equation in zip(first, second):
            self.assertIs(first_equation, second_equation)

    def test_set_temperature_equation_updates_rhs(self) -> None:
        """Test that the temperature equation is reused with an updated rhs."""
        # arrange
        self.node.connect_asset(asset=self.connected_asset, connection_point=self.connection_point)
        first_equation = self.node.set_temperature_equation()
        self.node.initial_temperature = 350.0

        # act
        second_equation = self.node.set_temperature_equation()

        # assert
        self.assertIs(first_equation, second_equation)
        self.assertEqual(second_equation.rhs, fluid_props.get_ie(350.0))

    def test_connect_asset_invalidates_node_cont_equation(self) -> None:
        """Test that connecting an asset invalidates the continuity equation."""
        # arrange
        self.node.connect_asset(asset=self.connected_asset, connection_point=self.connection_point)
        first_equation = self.node.get_node_cont_equation()

        # act
        self.node.connect_asset(
            asset=self.connected_asset_2, connection_point=self.connection_point_2
        )
        second_equation = self.node.get_node_cont_equation()

        # assert
        self.assertIsNot(first_equation, second_equation)
        self.assertEqual(len(second_equation.indices), 3)
        np_test.assert_array_equal(second_equation.coefficients, np.ones(3))

    @patch.object(Node, "get_energy_equation")
    @patch.object(Node, "set_temperature_equation")
    def test_get_energy_equations_with_positive_negative_flow(
        self, mock_set_temperature, mock_set_energy
    ) -> None:
        """Test the get_energy_equations method of the Node class."""
        # arrange
        # - Outflow
        self.connected_asset.prev_sol[
            index_core_quantity.mass_flow_rate
            + self.connection_point * index_core_quantity.number_core_quantities
        ] = +self.discharge
        self.node.connect_asset(asset=self.connected_asset, connection_point=self.connection_point)
        # - Inflow
        self.connected_asset_2.prev_sol[
            index_core_quantity.mass_flow_rate
            + self.connection_point_2 * index_core_quantity.number_core_quantities
        ] = -self.discharge
        self.node.connect_asset(
            asset=self.connected_asset_2, connection_point=self.connection_point_2
        )

        # act
        self.node.get_energy_equations()

        # assert
        self.assertEqual(mock_set_temperature.call_count, 0)
        self.assertEqual(mock_set_energy.call_count, 1)

    @patch.object(Node, "get_energy_equation")
    @patch.object(Node, "set_temperature_equation")
    def test_get_energy_equations_with_all_positive_flow(
        self, mock_set_temperature, mock_set_energy
    ) -> None:
        """Test the get_energy_equations method of the Node class.

        For same sign flow only temperature can be set.
        """
        # arrange
        # - Outflow
        self.connected_asset.prev_sol[
            index_core_quantity.mass_flow_rate
            + self.connection_point * index_core_quantity.number_core_quantities
        ] = +self.discharge
        self.node.connect_asset(asset=self.connected_asset, connection_point=self.connection_point)
        # - Inflow
        self.connected_asset_2.prev_sol[
            index_core_quantity.mass_flow_rate
            + self.connection_point_2 * index_core_quantity.number_core_quantities
        ] = +self.discharge
        self.node.connect_asset(
            asset=self.connected_asset_2, connection_point=self.connection_point_2
        )

        # act
        self.node.get_energy_equations()

        # assert
        self.assertEqual(mock_set_temperature.call_count, 1)
        self.assertEqual(mock_set_energy.call_count, 0)

    @patch.object(Node, "get_energy_equation")
    @patch.object(Node, "set_temperature_equation")
    def test_get_energy_equations_with_all_negative_flow(
        self, mock_set_temperature, mock_set_energy
    ) -> None:
        """Test the get_energy_equations method of the Node class."""
        # arrange
        # - Outflow
        self.connected_asset.prev_sol[
            index_core_quantity.mass_flow_rate
            + self.connection_point * index_core_quantity.number_core_quantities
        ] = -self.discharge
        self.node.connect_asset(asset=self.connected_asset, connection_point=self.connection_point)
        # - Inflow
        self.connected_asset_2.prev_sol[
            index_core_quantity.mass_flow_rate
            + self.connection_point_2 * index_core_quantity.number_core_quantities
        ] = -self.discharge
        self.node.connect_asset(
            asset=self.connected_asset_2, connection_point=self.connection_point_2
        )

        # act
        self.node.get_energy_equations()

        # assert
        self.assertEqual(mock_set_temperature.call_count, 1)
        self.assertEqual(mock_set_energy.call_count, 0)

    @patch.object(Node, "get_energy_equation")
    @patch.object(Node, "set_temperature_equation")
    def test_get_energy_equations_with_no_flow(self, mock_set_temperature, mock_set_energy) -> None:
        """Test the get_energy_equations method of the Node class."""
        # arrange
        # - Outflow
        self.connected_asset.prev_sol[
            index_core_quantity.mass_flow_rate
            + self.connection_point * index_core_quantity.number_core_quantities
        ] = 0.0
        self.node.connect_asset(asset=self.connected_asset, connection_point=self.connection_point)
        # - Inflow
        self.connected_asset_2.prev_sol[
            index_core_quantity.mass_flow_rate
            + self.connection_point_2 * index_core_quantity.number_core_quantities
        ] = 0.0
        self.node.connect_asset(
            asset=self.connected_asset_2, connection_point=self.connection_point_2
        )

        # act
        self.node.get_energy_equations()

        # assert
        self.assertEqual(mock_set_temperature.call_count, 1)
        self.assertEqual(mock_set_energy.call_count, 0)

    @patch.object(Node, "get_energy_equation")
    @patch.object(Node, "set_temperature_equation")
    def test_get_energy_equations_after_connecting_asset(
        self, mock_set_temperature, mock_set_energy
    ) -> None:
        """Test that the cached mass flow lookup is invalidated when an asset is connected."""
        # arrange
        # - Outflow, at this point the node only sees a single positive flow.
        self.connected_asset.prev_sol[
            index_core_quantity.mass_flow_rate
            + self.connection_point * index_core_quantity.number_core_quantities
        ] = +self.discharge
        self.node.connect_asset(asset=self.connected_asset, connection_point=self.connection_point)
        self.node.get_energy_equations()
        # - Inflow on a second asset, connected after the first call.
        self.connected_asset_2.prev_sol[
            index_core_quantity.mass_flow_rate
            + self.connection_point_2 * index_core_quantity.number_core_quantities
        ] = -self.discharge
        self.node.connect_asset(
            asset=self.connected_asset_2, connection_point=self.connection_point_2
        )

        # act
        self.node.get_energy_equations()

        # assert
        self.assertEqual(mock_set_temperature.call_count, 1)
        self.assertEqual(mock_set_energy.call_count, 1)
