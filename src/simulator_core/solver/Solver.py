"""Module for solving the network class."""
from simulator_core.solver.matrix.matrix import Matrix
from simulator_core.solver.network.Network import Network
from simulator_core.solver.matrix.equation_object import EquationObject


class Solver:
    """Class to solve the network."""

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
            self.network.get_asset(asset).set_matrix_index(self.matrix.add_unknowns(
                self.network.get_asset(asset).number_of_unknowns))
        for node in self.network.nodes:
            self.network.get_node(node).set_matrix_index(self.matrix.add_unknowns(
                self.network.get_node(node).number_of_unknowns))

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
        while not (self.matrix.is_converged()):
            iteration += 1
            equations = self.get_equations()
            self.matrix.solve(equations, dumb=False)
            self.results_to_assets()
            if iteration > 100:
                print("No converged solution reached")
                break

    def get_results(self) -> None:
        """Method to get the results of the network."""
        pass

    def results_to_assets(self) -> None:
        """Method to transfer the results to the assets from the matrix."""
        self.network.set_result_asset(self.matrix.sol_new)
        self.network.set_result_node(self.matrix.sol_new)
