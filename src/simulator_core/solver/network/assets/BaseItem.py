import uuid
from abc import ABC, abstractmethod
from simulator_core.solver.matrix.equation_object import EquationObject
from simulator_core.solver.utils.fluid_properties import FluidProperties


class BaseItem(ABC):
    def __init__(self, number_of_unknowns: int, name: uuid.UUID):
        self.name = name
        self.number_of_unknowns = number_of_unknowns
        self.fluid_properties = FluidProperties()
        self.matrix_index = 0
        self.prev_sol = [0] * self.number_of_unknowns

    def set_matrix_index(self, index: int):
        self.matrix_index = index

    @abstractmethod
    def get_equations(self) -> list[EquationObject]:
        pass
