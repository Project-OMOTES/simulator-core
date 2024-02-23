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

"""Test matrix object."""

import unittest

import numpy as np

from simulator_core.solver.matrix.matrix import Matrix
from simulator_core.solver.matrix.equation_object import EquationObject


class MatrixTest(unittest.TestCase):
    """Test the matrix object."""

    def test_init(self) -> None:
        """Test the init of the matrix object."""
        # arrange

        # act
        matrix = Matrix()  # act

        # assert
        self.assertEqual(matrix.num_unknowns, 0)
        self.assertEqual(len(matrix.mat), 0)
        self.assertEqual(len(matrix.rhs), 0)
        self.assertEqual(len(matrix.sol_new), 0)
        self.assertEqual(len(matrix.sol_old), 0)
        self.assertEqual(matrix.relative_convergence, 1e-6)
        self.assertEqual(matrix.absolute_convergence, 1e-6)

    def test_add_unknowns(self) -> None:
        """Test the add unknowns of the matrix object."""
        # arrange
        matrix = Matrix()
        number_of_unknowns = 2

        # act
        index = matrix.add_unknowns(number_unknowns=number_of_unknowns)  # act

        # assert
        self.assertEqual(matrix.num_unknowns, number_of_unknowns)
        self.assertEqual(matrix.sol_new, [1.0] * number_of_unknowns)
        self.assertEqual(matrix.sol_old, [0.0] * number_of_unknowns)
        self.assertEqual(index, 0)

    def test_add_unknowns_error(self) -> None:
        """Test the add unknowns of the matrix object."""
        # arrange
        matrix = Matrix()

        # act
        with self.assertRaises(ValueError) as cm:
            matrix.add_unknowns(number_unknowns=0)

        # assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            str(cm.exception),
            "Number of unknowns should be at least 1.",
        )

    def test_add_additional_unknowns(self) -> None:
        """Test the add unknowns of the matrix object."""
        # arrange
        matrix = Matrix()
        number_of_unknowns = 2
        matrix.add_unknowns(number_unknowns=number_of_unknowns)

        # act
        index = matrix.add_unknowns(number_unknowns=number_of_unknowns)  # act

        # assert
        self.assertEqual(index, number_of_unknowns)

    def test_add_equation(self) -> None:
        """Test the add equation of the matrix object."""
        # arrange
        matrix = Matrix()
        index = matrix.add_unknowns(2)
        equation = EquationObject()
        equation.indices = np.array([index, index + 1])
        equation.coefficients = np.array([1.0, 1.0])
        equation.rhs = 10.0

        # act
        matrix.add_equation(equation_object=equation)  # act

        # assert
        self.assertEqual(len(matrix.mat), 1)
        self.assertEqual(len(matrix.rhs), 1)
        self.assertEqual(matrix.mat[0], [1.0, 1.0])
        self.assertEqual(matrix.rhs[0], 10.0)

    def test_solve(self) -> None:
        """Test the solving of the matrix object."""
        # arrange
        matrix = Matrix()
        index = matrix.add_unknowns(2)
        equation1 = EquationObject()
        equation1.indices = np.array([index, index + 1])
        equation1.coefficients = np.array([1.0, 1.0])
        equation1.rhs = 0.0
        equation2 = EquationObject()
        equation2.indices = np.array([index, index + 1])
        equation2.coefficients = np.array([0.0, 1.0])
        equation2.rhs = 10.0

        # act
        result = matrix.solve([equation1, equation2])

        # assert
        self.assertEqual(result, [-10.0, 10.0])

    def test_solve_large(self) -> None:
        """Test the solving of the matrix object."""
        # arrange
        matrix = Matrix()
        value = 10.0
        equations = []
        size = 100
        for _ in range(size):
            position = matrix.add_unknowns(1)
            equation_object = EquationObject()
            equation_object.rhs = value
            equation_object.indices = [position, position + 1]
            equation_object.coefficients = [1.0, 1.0]
            equations.append(equation_object)
        position = matrix.add_unknowns(1)
        equation_object = EquationObject()
        equation_object.rhs = 5.0
        equation_object.indices = [position]
        equation_object.coefficients = [1.0]
        equations.append(equation_object)

        # act
        results = matrix.solve(equations)  # act

        # assert
        self.assertEqual(results, [5.0] * (size + 1))

    def test_is_converged_false(self) -> None:
        """Test the is converged of the matrix object."""
        # arrange
        matrix = Matrix()
        matrix.add_unknowns(2)

        # act
        result = matrix.is_converged()

        # assert
        self.assertEqual(result, False)

    def test_convergence_raise_error(self) -> None:
        """Test the convergence of the matrix object."""
        # arrange
        matrix = Matrix()

        # act
        with self.assertRaises(ValueError) as cm:
            matrix.is_converged()

        # assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            str(cm.exception),
            "No unknowns have been added to the matrix.",
        )

    def test_is_converged_true(self) -> None:
        """Test the is converged of the matrix object."""
        # arrange
        matrix = Matrix()
        matrix.add_unknowns(1)
        matrix.sol_new = [1.0]
        matrix.sol_old = matrix.sol_new

        # act
        result = matrix.is_converged()

        # assert
        self.assertEqual(result, True)

    def test_get_solution(self) -> None:
        """Test the get solution of the matrix object."""
        # arrange
        matrix = Matrix()
        matrix.add_unknowns(10)
        matrix.sol_new = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

        # act
        result = matrix.get_solution(index=3, number_of_unknowns=4)

        # assert
        self.assertEqual(result, [4.0, 5.0, 6.0, 7.0])

    def test_reset_solution(self) -> None:
        """Test the reset solution of the matrix object."""
        # arrange
        matrix = Matrix()
        matrix.add_unknowns(1)
        matrix.sol_new = [999.0]
        matrix.sol_old = [10.0]

        # act
        matrix.reset_solution()  # act

        # assert
        self.assertEqual(matrix.sol_new, [1.0])
        self.assertEqual(matrix.sol_old, [10.0])
