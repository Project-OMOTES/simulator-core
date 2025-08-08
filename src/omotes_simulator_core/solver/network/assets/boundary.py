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

"""Module containing Based boundary class."""
import numpy as np

from omotes_simulator_core.solver.matrix.equation_object import EquationObject
from omotes_simulator_core.solver.matrix.index_core_quantity import index_core_quantity
from omotes_simulator_core.solver.network.assets.base_asset import BaseAsset


class BaseBoundary(BaseAsset):
    """A base class for boundary conditions.

    This class represents a boundary condition and
    has a number of connection points, a name, and a number of unknowns.

    Attributes
    ----------
        connected_nodes (list): A list of nodes that are connected to this boundary.
        number_of_connection_point (int): The number of connection points for this boundary.
        equations_dict (dict): A dictionary that maps equation ids to equation indices in the
    """

    def __init__(
        self, name: str, _id: str, number_of_unknowns: int = 3, number_con_points: int = 1
    ):
        """Initialize the boundary condition.

        :param int number_con_points:The number of connection points for this boundary.
        :param str name: The name of this boundary.
        :param int number_of_unknowns (optional): The number of unknowns for this boundary.
                                                  Defaults to 3.
        """
        super().__init__(
            name=name,
            _id=_id,
            number_of_unknowns=number_of_unknowns,
            number_connection_points=number_con_points,
        )
        self.initial_pressure = 10000.0

    def get_pressure_equation(self) -> EquationObject:
        """Get a prescribed pressure equation for the boundary.

        This method gets an equation to the matrix that sets the pressure at the boundary
        to a fixed value.
        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation.
        """
        # self.equations_dict["prescribe pressure"] = equation_id
        equation_object = EquationObject()
        equation_object.indices = np.array([self.matrix_index + index_core_quantity.pressure])
        equation_object.coefficients = np.array([1.0])
        equation_object.rhs = self.initial_pressure
        return equation_object

    def get_equations(self) -> list[EquationObject]:
        """Method to get all the equations of the boundary.

        These equations are:
        - Pressure balance at each connection point
        - Thermal balance at each connection point
        - Pre describe pressure equation

        :return:EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation.
        """
        equations = [
            self.get_pressure_equation(),
            self.get_thermal_equations(0),
            self.get_press_to_node_equation(0),
        ]
        return equations
