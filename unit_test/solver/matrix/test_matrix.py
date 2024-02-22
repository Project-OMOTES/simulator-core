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

    def test_init(self):
        """Test the init of the matrix object."""
        # arrange

        # act
        matrix = Matrix()

        # assert
        self.assertEqual(matrix.num_unknowns, 0)
        self.assertEqual(len(matrix.mat), 0)
        self.assertEqual(len(matrix.rhs), 0)
        self.assertEqual(len(matrix.sol_new), 0)
        self.assertEqual(len(matrix.sol_old), 0)
        self.assertEqual(matrix.relative_convergence, 1e-6)
        self.assertEqual(matrix.absolute_convergence, 1e-6)

    def test_add_unknowns(self):
        """Test the add unknowns of the matrix object."""
        # arrange
        matrix = Matrix()

        # act
        index = matrix.add_unknowns(2)

        # assert
        self.assertEqual(matrix.num_unknowns, 2)
        self.assertEqual(len(matrix.sol_new), 2)
        self.assertEqual(len(matrix.sol_old), 2)
        self.assertEqual(index, 0)

    def test_add_additional_unknowns(self):
        """Test the add unknowns of the matrix object."""
        # arrange
        matrix = Matrix()
        matrix.add_unknowns(2)

        # act
        index = matrix.add_unknowns(2)

        # assert
        self.assertEqual(matrix.num_unknowns, 4)
        self.assertEqual(len(matrix.sol_new), 4)
        self.assertEqual(len(matrix.sol_old), 4)
        self.assertEqual(index, 2)

    def test_add_equation(self):
        """Test the add equation of the matrix object."""
        # arrange
        matrix = Matrix()
        index = matrix.add_unknowns(2)
        equation = EquationObject()
        equation.indices = np.array([index, index + 1])
        equation.coefficients = np.array([1.0, 1.0])
        equation.rhs = 10.0

        # act
        matrix.add_equation(equation_object=equation)

        # assert
        self.assertEqual(len(matrix.mat), 1)
        self.assertEqual(len(matrix.rhs), 1)
        self.assertEqual(matrix.mat[0], [1.0, 1.0])
        self.assertEqual(matrix.rhs[0], 10.0)

    def test_solve(self):
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

    def test_solve_large(self):
        """Test the solving of the matrix object."""

        # arrange
        matrix = Matrix()
        value = 10.0
        equations = []
        size = 1000
        for i in range(size):
            position = matrix.add_unknowns(1)
            equation_object = EquationObject()
            equation_object.indices = [0]
            equation_object.rhs = value
            equation_object.indices = [position]
            equation_object.coefficients = [1.0]
            equations.append(equation_object)

        # act
        results = matrix.solve(equations)

        # assert
        self.assertEqual(results, [value] * size)

    def test_is_converged(self):
        """Test the is converged of the matrix object."""
        # arrange
        matrix = Matrix()
        matrix.add_unknowns(2)

        # act
        result = matrix.is_converged()

        # assert
        self.assertEqual(result, False)

    def test_convergence_raise_error(self):
        """Test the convergence of the matrix object."""
        # arrange
        matrix = Matrix()

        # act
        matrix.relative_convergence = -1

        # assert
        with self.assertRaises(ValueError):
            matrix.is_converged()

    def test_is_converged2(self):
        """Test the is converged of the matrix object."""
        # arrange
        matrix = Matrix()
        matrix.add_unknowns(1)
        equation = EquationObject()
        equation.indices = [0]
        equation.coefficients = [1.0]
        equation.rhs = 10.0
        matrix.solve([equation])
        matrix.solve([equation])

        # act
        result = matrix.is_converged()

        # assert
        self.assertEqual(result, True)

    def test_get_solution(self):
        """Test the get solution of the matrix object."""
        # arrange
        matrix = Matrix()
        matrix.add_unknowns(10)

        # act
        result = matrix.get_solution(0, 2)

        # assert
        self.assertEqual(result, [1.0, 1.0])

    def test_reset_solution(self):
        """Test the reset solution of the matrix object."""
        # arrange
        matrix = Matrix()
        matrix.add_unknowns(1)
        equation = EquationObject()
        equation.indices = [0]
        equation.coefficients = [1.0]
        equation.rhs = 10.0
        matrix.solve([equation])
        matrix.solve([equation])

        # act
        matrix.reset_solution()

        # assert
        self.assertEqual(matrix.sol_new, [1.0])
        self.assertEqual(matrix.sol_old, [10.0])
