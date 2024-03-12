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
import numpy as np
import csv
from simulator_core.solver.matrix.equation_object import EquationObject
from simulator_core.solver.matrix.utility import absolute_difference, relative_difference


class Matrix:
    """Class which stores the matrix and can be used to solve it."""

    def __init__(self) -> None:
        """Constructor of matrix class."""
        self.num_unknowns: int = 0
        self.mat: list[list[float]] = []
        self.rhs: list[float] = []
        self.sol_new: list[float] = []
        self.sol_old: list[float] = []
        self.relative_convergence: float = 1e-6
        self.absolute_convergence: float = 1e-6

    def add_unknowns(self, number_unknowns: int) -> int:
        """Method to add unknowns to the matrix.

        Adds unknowns to the matrix and returns the location of the unknowns in the solution.
        :param int number_unknowns: Number of unknowns to add
        :return: int Starting index of the added unknowns.
        """
        if number_unknowns < 1:
            raise ValueError("Number of unknowns should be at least 1.")
        self.num_unknowns += number_unknowns
        self.sol_new += [1.0] * number_unknowns
        self.sol_old += [0.0] * number_unknowns
        return self.num_unknowns - number_unknowns

    def add_equation(self, equation_object: EquationObject) -> None:
        """Method to add an equation to the matrix.

        Add equation to the matrix it returns a unique id to the equation for easy access.
        :param EquationObject equation_object: Object containing all information of the equation
        :return:
        """
        row = len(self.rhs)
        self.rhs.append(0.0)
        self.mat.append([])
        self.mat[row] = equation_object.to_list(self.num_unknowns)
        self.rhs[row] = equation_object.rhs

    def solve(self, equations: list[EquationObject], dumb: bool = False) -> list[float]:
        """Method to solve the system of equation given in the matrix.

        Solves the system of equations and returns the solution. The numpy linalg
        library solve method is used. For this the matrix is converted to np arrays.
        :return: list containing the solution of the system of equations.
        """
        # TODO add checks if enough equations have been supplied.
        # TODO check if matrix is solvable.
        self.rhs = []
        self.mat = []
        for equation in equations:
            self.add_equation(equation)
        if dumb:
            self.dump_matrix()
        self.sol_old = self.sol_new
        a = np.array(self.mat)
        b = np.array(self.rhs)
        self.sol_new = np.linalg.solve(a, b).tolist()
        return self.sol_new

    def is_converged(self) -> bool:
        """Returns true when the solution has converged and false when not.

        This method uses both the absolute difference and the relative difference to determine if
        the solution has converged. If one of them is converged true is returned.
        :return: Bool whether the solution has converged based on the given convergence criteria.
        """
        if self.num_unknowns == 0:
            raise ValueError("No unknowns have been added to the matrix.")
        rel_dif = max(
            [relative_difference(old, new) for old, new in zip(self.sol_old, self.sol_new)])
        abs_dif = max(
            [absolute_difference(old, new) for old, new in zip(self.sol_old, self.sol_new)])
        return rel_dif < self.relative_convergence or abs_dif < self.absolute_convergence

    def get_solution(self, index: int, number_of_unknowns: int) -> list[float]:
        """Method to get the solution of an asset.

        Returns the solution starting at the given index and for the number of
        unknowns supplied at the input.

        :param int index:Start position for which to supply the solution
        :param int number_of_unknowns: Number of elements for which the solution needs to
        be provided
        :return: list with teh solution
        """
        #  TODO add checks if the index and number of unknowns are within the range of the solution.
        return self.sol_new[index:index + number_of_unknowns]

    def dump_matrix(self, file_name: str = 'dump.csv') -> None:
        """Method to dump the matrix to a csv file.

        :param str file_name: File name to dump the matrix in default=dump.csv
        :return:
        """
        with open(file_name, 'w', newline='') as f:
            write = csv.writer(f)
            for row, rhs in zip(self.mat, self.rhs):
                write.writerow(row + [rhs])

    def reset_solution(self) -> None:
        """Method to reset the solution to 1, so the new iteration can start."""
        self.sol_new = [1.0] * len(self.sol_new)
