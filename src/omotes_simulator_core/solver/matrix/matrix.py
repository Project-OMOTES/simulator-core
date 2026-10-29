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
"""Module containing a matrix class to store the matrix and solve it using numpy."""

import csv
from typing import Any

import numpy as np
import numpy.typing as npt
import scipy as sp

from omotes_simulator_core.solver.matrix.equation_object import EquationObject
from omotes_simulator_core.solver.matrix.index_core_quantity import NUMBER_OF_CORE_QUANTITIES


class Matrix:
    """Class which stores the matrix and can be used to solve it."""

    num_unknowns: int = 0
    sol_new: npt.NDArray = np.array([], dtype=float)
    sol_old: npt.NDArray = np.array([], dtype=float)
    relative_convergence: float = 1e-6
    absolute_convergence: float = 1e-6

    def __init__(self) -> None:
        """Constructor of matrix class."""
        self._pattern_cache: dict[str, Any] | None = None

    def add_unknowns(self, number_unknowns: int) -> int:
        """Method to add unknowns to the matrix.

        Adds unknowns to the matrix and returns the location of the unknowns in the solution.
        :param int number_unknowns: Number of unknowns to add
        :return: int Starting index of the added unknowns.
        """
        if number_unknowns < 1:
            raise ValueError("Number of unknowns should be at least 1.")
        self.num_unknowns += number_unknowns
        self.sol_new = np.concatenate([self.sol_new, np.ones(number_unknowns)])
        self.sol_old = np.concatenate([self.sol_old, np.zeros(number_unknowns)])

        return self.num_unknowns - number_unknowns

    def solve(self, equations: list[EquationObject], dump: bool = False) -> list[float]:
        """Method to solve the system of equation given in the matrix using sparse matrix solver.

        A sparse matrix solver is used, for this the coefficients, indices in the matrix are
        converted to numpy arrays. These arrays are then used to create a csc_matrix which can
        be solved by the sparse matrix solver of scipy.
        :param dump: if true it will dump the matrix to a csv file
        :param equations: list with the equations to solve.
        :return: list containing the solution of the system of equations.
        """
        self.verify_equations(equations)
        self.sol_old = self.sol_new
        coefficient_array = np.concatenate([equation.coefficients for equation in equations])
        column_index_array = np.concatenate([equation.indices for equation in equations])
        lengths = np.fromiter((len(equation) for equation in equations), dtype=np.int64)
        matrix = self._build_csc_matrix(coefficient_array, column_index_array, lengths)
        rhs = np.array([equation.rhs for equation in equations], dtype=float)
        if dump:
            self.dump_matrix(matrix=matrix, rhs_array=rhs)
        self.sol_new = sp.sparse.linalg.spsolve(matrix, rhs)
        if np.isnan(self.sol_new).any():
            self.dump_matrix(matrix=matrix, rhs_array=rhs)
            raise RuntimeError("Matrix is singular, matrix is dumped to file.")
        result: list[float] = self.sol_new.tolist()
        return result

    def _build_csc_matrix(
        self,
        coefficients: npt.NDArray,
        columns: npt.NDArray,
        lengths: npt.NDArray,
    ) -> sp.sparse.csc_matrix:
        """Build the csc matrix, reusing the sparsity pattern when the structure is unchanged.

        The sorting permutation, row indices and column pointers only depend on the column
        indices and the number of coefficients per equation. These are cached and validated on
        every call, so only the coefficients are re-ordered (and duplicates summed) per call.
        :param coefficients: coefficients of all equations, concatenated.
        :param columns: column indices of all equations, concatenated.
        :param lengths: number of coefficients per equation.
        :return: csc matrix of the system of equations.
        """
        cache = self._pattern_cache
        if (
            cache is None
            or cache["num_unknowns"] != self.num_unknowns
            or not np.array_equal(cache["lengths"], lengths)
            or not np.array_equal(cache["columns"], columns)
        ):
            rows = np.repeat(np.arange(len(lengths), dtype=np.int32), lengths)
            permutation = np.lexsort((rows, columns))
            sorted_rows = rows[permutation]
            sorted_columns = columns[permutation]
            is_new_entry = np.ones(len(sorted_rows), dtype=bool)
            is_new_entry[1:] = (sorted_rows[1:] != sorted_rows[:-1]) | (
                sorted_columns[1:] != sorted_columns[:-1]
            )
            starts = np.flatnonzero(is_new_entry)
            has_duplicates = len(starts) != len(sorted_rows)
            indptr = np.zeros(self.num_unknowns + 1, dtype=np.int32)
            np.cumsum(
                np.bincount(sorted_columns[starts], minlength=self.num_unknowns),
                out=indptr[1:],
            )
            cache = {
                "num_unknowns": self.num_unknowns,
                "lengths": lengths.copy(),
                "columns": columns.copy(),
                "permutation": permutation,
                "starts": starts if has_duplicates else None,
                "indices": sorted_rows[starts].astype(np.int32),
                "indptr": indptr,
            }
            self._pattern_cache = cache
        data = coefficients[cache["permutation"]]
        if cache["starts"] is not None:
            data = np.add.reduceat(data, cache["starts"])
        return sp.sparse.csc_matrix(
            (data, cache["indices"], cache["indptr"]),
            shape=(self.num_unknowns, self.num_unknowns),
        )

    def verify_equations(self, equations: list[EquationObject]) -> None:
        """Method to verify if the system of equations can be solved.

        This method checks if the number of equations supplied is equal to the number of unknowns.
        :param equations: list with the equations to verify.
        :return: None
        """
        if len(equations) > self.num_unknowns:
            raise ValueError(
                f"Too many equations supplied. Got {len(equations)} equations, "
                f"but number of unknowns is {self.num_unknowns}"
            )
        if len(equations) < self.num_unknowns:
            raise ValueError(
                f"Not enough equation supplied. Got {len(equations)} equations, "
                f"but number of unknowns is {self.num_unknowns}"
            )

    def is_converged(self) -> bool:
        """Returns true when the solution has converged and false when not.

        This method uses the np.allclose method to calculate if the solution is converged
        :return: Bool whether the solution has converged based on the given convergence criteria.
        """
        if self.num_unknowns == 0:
            raise ValueError("No unknowns have been added to the matrix.")
        return bool(
            np.all(
                np.abs(self.sol_new - self.sol_old)
                <= self.absolute_convergence + self.relative_convergence * np.abs(self.sol_old)
            )
        )

    def get_solution(self, index: int, number_of_unknowns: int) -> list[float]:
        """Method to get the solution of an asset.

        Returns the solution starting at the given index and for the number of
        unknowns supplied at the input.

        :param int index:Start position for which to supply the solution
        :param int number_of_unknowns: Number of elements for which the solution needs to
        be provided
        :return: list with teh solution
        """
        if index > self.num_unknowns:
            raise IndexError(
                f"Index ({index}) greater than number " f"of unknowns ({self.num_unknowns})"
            )
        if (index + number_of_unknowns) > self.num_unknowns:
            raise IndexError(
                f"Index ({index}) plus request number of elements "
                f"({number_of_unknowns}) greater than "
                f"number of unknowns {self.num_unknowns}"
            )
        result: list[float] = self.sol_new[index : index + number_of_unknowns].tolist()
        return result

    def dump_matrix(
        self,
        matrix: sp.sparse.csc_matrix,
        rhs_array: npt.NDArray | sp.sparse.csc_matrix,
        file_name: str = "dump.csv",
    ) -> None:
        """Method to dump the matrix to a csv file.

        :param matrix: Matrix to be printed to the file
        :param rhs_array: Dense vector or sparse column containing the right hand side
        :param file_name: File name to dump the matrix in default=dump.csv
        :return:
        """
        rhs_values = rhs_array if isinstance(rhs_array, np.ndarray) else rhs_array.toarray().ravel()
        with open(file_name, "w", newline="") as f:
            write = csv.writer(f)
            write.writerow(
                ["m", "P", "u"] * int(self.num_unknowns / NUMBER_OF_CORE_QUANTITIES) + ["rhs"]
            )
            for row, rhs in zip(matrix.todense(), rhs_values):
                write.writerow(row.tolist()[0] + [rhs])

    def reset_solution(self) -> None:
        """Method to reset the solution to 1, so the new iteration can start."""
        self.sol_new = np.ones(self.num_unknowns)
