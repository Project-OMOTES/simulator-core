"""Module containing abstract BaseItem class."""
import uuid
from abc import ABC, abstractmethod
from simulator_core.solver.matrix.equation_object import EquationObject


class BaseItem(ABC):
    """A base class for items in a network."""

    def __init__(self, number_of_unknowns: int, name: uuid.UUID):
        """Initializes the BaseItem object with the given parameters.

        :param int number_of_unknowns: The number of unknown variables for the item.
        :param uuid.UUID name: The unique identifier of the item.
        """
        self.name = name
        self.number_of_unknowns = number_of_unknowns
        self.matrix_index = 0
        self.prev_sol: list[float] = [0.0] * self.number_of_unknowns

    def set_matrix_index(self, index: int) -> None:
        """Sets the matrix index of the item.

        :param int index: The index of the item in the matrix.
        """
        self.matrix_index = index

    @abstractmethod
    def get_equations(self) -> list[EquationObject]:
        """Returns the equations for the item.

        :return: The equations for the item.
        :rtype: list[EquationObject]
        """
        pass
