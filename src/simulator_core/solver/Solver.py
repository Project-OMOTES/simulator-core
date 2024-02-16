from simulator_core.solver.matrix.matrix import Matrix
from simulator_core.solver.network.Network import Network
from simulator_core.solver.matrix.equation_object import EquationObject


class Solver:
    def __init__(self, network: Network):
        self.matrix = Matrix()
        self.network = network
        self.set_unknowns_matrix()

    def set_unknowns_matrix(self):
        for asset in self.network.assets:
            self.network.get_asset(asset).set_matrix_index(self.matrix.add_unknowns(
                self.network.get_asset(asset).number_of_unknowns))
        for node in self.network.nodes:
            self.network.get_node(node).set_matrix_index(self.matrix.add_unknowns(
                self.network.get_node(node).number_of_unknowns))

    def get_equations(self) -> list[EquationObject]:
        equations = []
        for asset in self.network.assets:
            equations = equations + self.network.assets[asset].get_equations()
        for node in self.network.nodes:
            equations = equations + self.network.nodes[node].get_equations()
        return equations

    def solve(self):
        iteration = 0
        while not (self.matrix.is_converged()):
            iteration += 1
            self.matrix.dumb_matrix()
            equations = self.get_equations()
            self.matrix.solve(equations, dumb=False)
            self.results_to_assets()
            if iteration > 100:
                print("No converged solution reached")
                break

    def get_results(self):
        pass

    def results_to_assets(self):
        self.network.set_result_asset(self.matrix.sol_new)
        self.network.set_result_node(self.matrix.sol_new)
