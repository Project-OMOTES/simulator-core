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

import csv
import unittest
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import numpy as np
import numpy.testing as npt
import scipy as sp

from omotes_simulator_core.solver.matrix.equation_object import EquationObject
from omotes_simulator_core.solver.matrix.matrix import Matrix


class MatrixTest(unittest.TestCase):
    """Test the matrix object."""

    def test_init(self) -> None:
        """Test the init of the matrix object."""
        # arrange

        # act
        matrix = Matrix()  # act

        # assert
        self.assertEqual(matrix.num_unknowns, 0)
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
        npt.assert_array_equal(matrix.sol_new, np.array([1.0] * number_of_unknowns))
        npt.assert_array_equal(matrix.sol_old, np.array([0.0] * number_of_unknowns))
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

    def test_solve_dense_rhs(self) -> None:
        """Pass a floating-point vector to the sparse solver, including a single unknown."""
        for size in (1, 3):
            with self.subTest(size=size):
                matrix = Matrix()
                matrix.add_unknowns(size)
                equations = []
                for i in range(size):
                    equation = EquationObject()
                    equation.indices = np.array([i])
                    equation.coefficients = np.array([2.0])
                    equation.rhs = i - 1
                    equations.append(equation)
                with patch(
                    "omotes_simulator_core.solver.matrix.matrix.sp.sparse.linalg.spsolve",
                    wraps=sp.sparse.linalg.spsolve,
                ) as solve:
                    result = matrix.solve(equations)
                rhs = solve.call_args.args[1]
                self.assertIsInstance(rhs, np.ndarray)
                self.assertEqual(rhs.shape, (size,))
                self.assertEqual(rhs.dtype, np.dtype(float))
                npt.assert_allclose(result, np.arange(-1, size - 1) / 2)

    def test_solve_repeated_rhs(self) -> None:
        """Refresh the RHS and retain the previous solution across solves."""
        matrix = Matrix()
        matrix.add_unknowns(1)
        equation = EquationObject()
        equation.indices = np.array([0])
        equation.coefficients = np.array([2.0])
        equation.rhs = 4.0
        self.assertEqual(matrix.solve([equation]), [2.0])
        equation.rhs = -6.0
        self.assertEqual(matrix.solve([equation]), [-3.0])
        npt.assert_array_equal(matrix.sol_old, [2.0])
        npt.assert_array_equal(matrix.sol_new, [-3.0])

    def test_dump_matrix_rhs_formats(self) -> None:
        """Keep the CSV layout identical for dense and legacy sparse RHS inputs."""
        matrix = Matrix()
        matrix.add_unknowns(3)
        coefficients = sp.sparse.eye(3, format="csc")
        rhs = np.array([0.0, -2.0, 3.0])
        for rhs_array in (rhs, sp.sparse.csc_matrix(rhs[:, None])):
            with self.subTest(rhs_type=type(rhs_array)), TemporaryDirectory() as directory:
                filename = Path(directory) / "dump.csv"
                matrix.dump_matrix(coefficients, rhs_array, str(filename))
                with filename.open(newline="") as handle:
                    rows = list(csv.reader(handle))
                self.assertEqual(rows[0], ["m", "P", "u", "rhs"])
                npt.assert_array_equal(
                    np.array(rows[1:], dtype=float), np.column_stack((np.eye(3), rhs))
                )

    def test_solve_dump(self) -> None:
        """Write valid diagnostics during an explicit dump and a singular solve."""
        for singular in (False, True):
            with self.subTest(singular=singular), TemporaryDirectory() as directory:
                matrix = Matrix()
                matrix.add_unknowns(3)
                equations = []
                for i in range(3):
                    equation = EquationObject()
                    equation.indices = np.array([i])
                    equation.coefficients = np.array([0.0 if singular else 1.0])
                    equation.rhs = float(i)
                    equations.append(equation)
                filename = Path(directory) / "dump.csv"
                dump = partial(matrix.dump_matrix, file_name=str(filename))
                with patch.object(matrix, "dump_matrix", side_effect=dump) as dump_method:
                    if singular:
                        with self.assertWarns(sp.sparse.linalg.MatrixRankWarning):
                            with self.assertRaisesRegex(RuntimeError, "Matrix is singular"):
                                matrix.solve(equations)
                    else:
                        self.assertEqual(matrix.solve(equations, dump=True), [0.0, 1.0, 2.0])
                    dump_method.assert_called_once()
                with filename.open(newline="") as handle:
                    rows = list(csv.reader(handle))
                self.assertEqual(rows[0], ["m", "P", "u", "rhs"])
                expected_matrix = np.zeros((3, 3)) if singular else np.eye(3)
                npt.assert_array_equal(
                    np.array(rows[1:], dtype=float),
                    np.column_stack((expected_matrix, np.arange(3))),
                )

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
            equation_object.indices = np.array([position, position + 1])
            equation_object.coefficients = np.array([1.0, 1.0])
            equations.append(equation_object)
        position = matrix.add_unknowns(1)
        equation_object = EquationObject()
        equation_object.rhs = 5.0
        equation_object.indices = np.array([position])
        equation_object.coefficients = np.array([1.0])
        equations.append(equation_object)

        # act
        results = matrix.solve(equations)  # act

        # assert
        self.assertEqual(results, [5.0] * (size + 1))

    def test_solve_singular(self) -> None:
        """Test the solving of the matrix object."""
        # arrange
        matrix = Matrix()
        index = matrix.add_unknowns(2)
        equation1 = EquationObject()
        equation1.indices = np.array([index, index + 1])
        equation1.coefficients = np.array([0.0, 0.0])
        equation1.rhs = 0.0
        equation2 = EquationObject()
        equation2.indices = np.array([index, index + 1])
        equation2.coefficients = np.array([0.0, 1.0])
        equation2.rhs = 10.0

        # act
        with self.assertRaises(RuntimeError) as cm:
            matrix.solve([equation1, equation2])

        # assert
        self.assertIsInstance(cm.exception, RuntimeError)
        self.assertEqual(str(cm.exception), "Matrix is singular, matrix is dumped to file.")

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
        matrix.sol_new = np.array([1.0])
        matrix.sol_old = matrix.sol_new

        # act
        result = matrix.is_converged()

        # assert
        self.assertEqual(result, True)

    def test_is_converged_tolerances(self) -> None:
        """Test is_converged gives the same result as np.allclose."""
        matrix = Matrix()
        matrix.add_unknowns(3)
        for new, old in [
            ([0.0, 0.0, 0.0], [5e-7, 0.0, 0.0]),
            ([0.0, 0.0, 0.0], [2e-6, 0.0, 0.0]),
            ([1000.0, 1.0, 1.0], [1000.0005, 1.0, 1.0]),
            ([1000.0, 1.0, 1.0], [1000.01, 1.0, 1.0]),
        ]:
            matrix.sol_new = np.array(new)
            matrix.sol_old = np.array(old)
            expected = np.allclose(new, old, atol=1e-6, rtol=1e-6)
            self.assertEqual(matrix.is_converged(), expected)

    def test_solve_with_duplicate_entries(self) -> None:
        """Test that duplicate (row, column) entries are summed."""
        matrix = Matrix()
        index = matrix.add_unknowns(2)
        equation1 = EquationObject()
        equation1.indices = np.array([index, index, index + 1])
        equation1.coefficients = np.array([1.0, 1.0, 1.0])
        equation1.rhs = 5.0
        equation2 = EquationObject()
        equation2.indices = np.array([index + 1])
        equation2.coefficients = np.array([2.0])
        equation2.rhs = 2.0

        result = matrix.solve([equation1, equation2])

        npt.assert_allclose(result, [2.0, 1.0])

    def test_solve_pattern_cache_reuse_and_invalidation(self) -> None:
        """Test that the cached pattern is reused and rebuilt when the structure changes."""
        matrix = Matrix()
        index = matrix.add_unknowns(2)

        def make(
            coefficients: list[float], rhs: list[float], diagonal_only: bool = False
        ) -> list[EquationObject]:
            equation1 = EquationObject()
            equation2 = EquationObject()
            equation1.indices = np.array([index, index + 1])
            equation1.coefficients = np.array(coefficients[:2])
            equation1.rhs = rhs[0]
            if diagonal_only:
                equation2.indices = np.array([index + 1])
                equation2.coefficients = np.array(coefficients[3:])
            else:
                equation2.indices = np.array([index, index + 1])
                equation2.coefficients = np.array(coefficients[2:])
            equation2.rhs = rhs[1]
            return [equation1, equation2]

        first = matrix.solve(make([2.0, 0.0, 0.0, 4.0], [2.0, 8.0]))
        cache = matrix._pattern_cache
        second = matrix.solve(make([1.0, 0.0, 0.0, 1.0], [3.0, 4.0]))
        reused = matrix._pattern_cache is cache
        third = matrix.solve(make([1.0, 1.0, 0.0, 2.0], [3.0, 4.0], diagonal_only=True))

        npt.assert_allclose(first, [1.0, 2.0])
        npt.assert_allclose(second, [3.0, 4.0])
        self.assertTrue(reused)
        self.assertIsNot(matrix._pattern_cache, cache)
        npt.assert_allclose(third, [1.0, 2.0])

    def test_get_solution(self) -> None:
        """Test the get solution of the matrix object."""
        # arrange
        matrix = Matrix()
        matrix.add_unknowns(10)
        matrix.sol_new = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])

        # act
        result = matrix.get_solution(index=3, number_of_unknowns=4)

        # assert
        self.assertEqual(result, [4.0, 5.0, 6.0, 7.0])

    def test_get_solution_error_index(self) -> None:
        """Test the get solution to raise an error when index is out of bound."""
        # arrange
        matrix = Matrix()
        matrix.add_unknowns(10)
        matrix.sol_new = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])

        # act
        with self.assertRaises(IndexError) as cm:
            matrix.get_solution(index=11, number_of_unknowns=4)

        # assert
        self.assertIsInstance(cm.exception, IndexError)
        self.assertEqual(
            str(cm.exception), f"Index ({11}) greater than number " f"of unknowns ({10})"
        )

    def test_get_solution_error_number(self) -> None:
        """Test the get solution to raise an error when index is out of bound."""
        # arrange
        matrix = Matrix()
        matrix.add_unknowns(10)
        matrix.sol_new = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])

        # act
        with self.assertRaises(IndexError) as cm:
            matrix.get_solution(index=5, number_of_unknowns=10)

        # assert
        self.assertIsInstance(cm.exception, IndexError)
        self.assertEqual(
            str(cm.exception),
            f"Index ({5}) plus request number of elements "
            f"({10}) greater than "
            f"number of unknowns {10}",
        )

    def test_reset_solution(self) -> None:
        """Test the reset solution of the matrix object."""
        # arrange
        matrix = Matrix()
        matrix.add_unknowns(1)
        matrix.sol_new = np.array([999.0])
        matrix.sol_old = np.array([10.0])

        # act
        matrix.reset_solution()  # act

        # assert
        self.assertEqual(matrix.sol_new, [1.0])
        self.assertEqual(matrix.sol_old, [10.0])
