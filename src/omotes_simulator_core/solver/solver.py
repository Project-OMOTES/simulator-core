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
"""Module for solving the network class."""
import logging

from omotes_simulator_core.solver.matrix.equation_object import EquationObject
from omotes_simulator_core.solver.matrix.matrix import Matrix
from omotes_simulator_core.solver.network.network import Network

logger = logging.getLogger(__name__)


class Solver:
    """Class to solve the network."""

    _iteration_limit: int = 100
    """The maximum number of iterations for the solver."""

    def __init__(self, network: Network):
        """Constructor of the solver class.

        Initializes the class properties and sets the unknowns of the matrix.

        :param Network network: The network to be solved.
        """
        self.matrix = Matrix()
        self.network = network
        self.set_unknowns_matrix()

    def set_unknowns_matrix(self) -> None:
        """Sets the unknowns of the matrix."""
        for asset in self.network.assets:
            self.network.get_asset(asset).set_matrix_index(
                self.matrix.add_unknowns(self.network.get_asset(asset).number_of_unknowns)
            )
        for node in self.network.nodes:
            self.network.get_node(node).set_matrix_index(
                self.matrix.add_unknowns(self.network.get_node(node).number_of_unknowns)
            )

    def get_equations(self) -> list[EquationObject]:
        """Method to get the equations of the network.

        :return: list[EquationObject] equations: List of equations of the network.
        """
        equations: list[EquationObject] = []
        for asset in self.network.assets:
            equations = equations + self.network.assets[asset].get_equations()
        for node in self.network.nodes:
            equations = equations + self.network.nodes[node].get_equations()
        return equations

    def solve(self) -> None:
        """Method to solve the network."""
        iteration = 0
        self.matrix.reset_solution()
        for asset in self.network.assets:
            self.network.get_asset(asset).reset_prev_sol()
        for node in self.network.nodes:
            self.network.get_node(node).reset_prev_sol()
        while not self.matrix.is_converged():
            iteration += 1
            equations = self.get_equations()
            self.matrix.solve(equations, dump=False)
            self.results_to_assets()
            if iteration > self._iteration_limit:
                logger.warning("No converged solution reached")
                break
        logger.debug("Solver finished after %d iterations", iteration)

    def get_results(self) -> None:
        """Method to get the results of the network."""

    def results_to_assets(self) -> None:
        """Method to transfer the results to the assets from the matrix."""
        self.network.set_result_asset(self.matrix.sol_new)
        self.network.set_result_node(self.matrix.sol_new)
