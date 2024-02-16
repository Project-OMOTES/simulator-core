"""Module containing a matrix class to store the matrix and solve it using numpy."""
import uuid
import numpy as np
import scipy
import csv
from simulator_core.solver.matrix.equation_object import EquationObject
from simulator_core.solver.matrix.utility import absolute_difference, relative_difference


class Matrix:
    """Class which stores the matrix and can be used to solve it."""

    def __init__(self):
        """Constructor of matrix class."""
        self.num_unknowns = 0
        self.mat = []
        self.rhs = []
        self.sol_new = []
        self.sol_old = []
        self.equation_handle_dict = {}
        self.relative_convergence = 1e-6
        self.absolute_convergence = 1e-6

    def add_unknowns(self, number_unknowns: int) -> int:
        """Method to add unknowns to the matrix.

        Adds unknowns to the matrix and returns the location of the unknowns in the solution.
        :param int number_unknowns: Number of unknowns to add
        :return: int Starting index of the added unknowns.
        """
        self.num_unknowns += number_unknowns
        self.sol_new += [1.0] * number_unknowns
        self.sol_old += [0.0] * number_unknowns
        return self.num_unknowns - number_unknowns

    def add_equation(self, equation_object: EquationObject):
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

    def remove_equation(self, handle: uuid.UUID):
        """Method to remove an equation from the matrix.

        Removes the equation with the given handle from the matrix.
        :param handle: Handle of the equation to be removed from the matrix.
        :return:
        """
        row = self.equation_handle_dict[handle]
        self.rhs.pop(row)
        self.mat.pop(row)
        self.equation_handle_dict.pop(handle)
        # since you remove an equation all indices most by shifted by 1.
        for equation in self.equation_handle_dict:
            if self.equation_handle_dict[equation] > row:
                self.equation_handle_dict[equation] -= 1

    def set_equation(self, handle: uuid.UUID, equation_object: EquationObject):
        """Method to set the coefficient of an equation in the matrix.

        Sets the coefficients of an equation with the given handle.
        :param uuid.UUID handle: handle of the equation.
        :param equation_object: object containing all information of the equation
        :return: None
        """
        row = self.equation_handle_dict[handle]
        self.mat[row] = equation_object.to_list(self.num_unknowns)
        self.rhs[row] = equation_object.rhs

    def solve(self, equations: list[EquationObject], dumb: bool = False) -> list:
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
            self.dumb_matrix()
        self.sol_old = self.sol_new
        a = np.array(self.mat)
        b = np.array(self.rhs)
        self.sol_new = np.linalg.solve(a, b)
        return self.sol_new.tolist()

    def solve2(self, equations: list[EquationObject], dumb: bool = False) -> list:
        """Method to solve the system of equation given in the matrix.

        Solves the system of equations and returns the solution. The numpy linalg
        library solve method is used. For this the matrix is converted to np arrays.
        :return: list containing the solution of the system of equations.
        """
        # TODO add checks if enough equations have been supplied.
        # TODO check if matrix is solvable.
        self.rhs = np.array([equation.rhs for equation in equations], float)
        row = np.array([], int)
        col = np.array([], int)
        data = np.array([], float)
        row_index = 0
        for equation in equations:
            row = np.append(row, [row_index] * len(equation.indices))
            row_index += 1
            col = np.append(col, equation.indices)
            data = np.append(data, equation.coefficients)
        A = scipy.sparse.csc_matrix((data, (row, col)),
                                shape=(self.num_unknowns, self.num_unknowns))
        self.sol_new = scipy.sparse.linalg.spsolve(A, self.rhs)
        return self.sol_new.tolist()

    def is_converged(self) -> bool:
        """Returns true when the solution has converged and false when not.

        This method uses both the absolute difference and the relative difference to determine if
        the solution has converged. If one of them is converged true is returned.
        :return: Bool whether the solution has converged based on the given convergence criteria.
        """
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
        return self.sol_new[index:index + number_of_unknowns]

    def dumb_matrix(self, file_name: str = 'dumb.csv'):
        """Method to dumb the matrix to a csv file.

        :param str file_name: File name to dumb the matrix in default=dumb.csv
        :return:
        """
        with open(file_name, 'w', newline='') as f:
            write = csv.writer(f)
            write.writerows(self.mat)

    def reset_solution(self):
        self.sol_new = [1] * len(self.sol_new)
