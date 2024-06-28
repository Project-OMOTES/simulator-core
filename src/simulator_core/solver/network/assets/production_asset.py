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
"""Module containing the production asset class."""
import numpy as np

from simulator_core.solver.matrix.equation_object import EquationObject
from simulator_core.solver.network.assets.fall_type import FallType


class ProductionAsset(FallType):
    """
    A class to represent a production asset in a network.

    This class inherits from the FallType class and implements the methods to generate
    the equations for the production asset.

    Attributes
    ----------
    connected_nodes : list[int]
        A list of integers that store the node indices that are connected to the asset.
    number_of_connection_point : int
        The number of connection points for the asset.
    pre_scribe_mass_flow : bool
        A boolean flag that indicates whether the mass flow rate or the pressure is prescribed
        at the connection points.

    Methods
    -------
    get_equations() -> list[EquationObject]
        Returns a list of EquationObjects that represent the equations for the asset.
    add_pre_scribe_equation(connection_point: int) -> EquationObject
        Returns an EquationObject that represents the prescribed mass flow rate or pressure
        equation for the asset at the given connection point.
    """

    mass_flow_rate_set_point: float
    """The mass flow rate set point for the asset."""

    set_pressure: float
    """The pressure set point for the asset."""

    pre_scribe_mass_flow: bool
    """A boolean flag that indicates whether the mass flow rate or the pressure is prescribed
    at the connection points."""

    def __init__(
        self,
        name: str,
        _id: str,
        supply_temperature: float = 293.15,
        heat_supplied: float = 0.0,
        loss_coefficient: float = 1.0,
        pre_scribe_mass_flow: bool = True,
        mass_flow_rate_set_point: float = 10.0,
        set_pressure: float = 10000.0,
    ):
        """
        Initializes the ProductionAsset object with the given parameters.

        Parameters
        ----------
        name : str The name of the asset.
        _id : str The unique identifier of the asset.
        number_of_unknowns : int, optional
            The number of unknown variables for the asset. The default is 6, which corresponds to
            the mass flow rate, pressure, and temperature at each connection point.
        number_con_points : int, optional
            The number of connection points for the asset. The default is 2, which corresponds to
            the inlet and outlet.
        """
        self.pre_scribe_mass_flow = pre_scribe_mass_flow
        self.mass_flow_rate_set_point = mass_flow_rate_set_point
        self.set_pressure = set_pressure

        super().__init__(
            name=name,
            _id=_id,
            supply_temperature=supply_temperature,
            heat_supplied=heat_supplied,
            loss_coefficient=loss_coefficient,
        )

    def get_equations(self) -> list[EquationObject]:
        """Returns a list of EquationObjects that represent the equations for the asset.

        The equations are:
        - Pressure balance at each connection point
        - Thermal balance at each connection point
        - Prescribed mass flow rate or pressure at each connection point
        :return: list[EquationObject]
            A list of EquationObjects that contain the indices, coefficients, and right-hand side
            values of the equations.
        """
        equations = [
            super().add_press_to_node_equation(0),
            super().add_press_to_node_equation(1),
            self.add_thermal_equations(0),
            self.add_thermal_equations(1),
            self.add_pre_scribe_equation(0),
            self.add_pre_scribe_equation(1),
        ]
        return equations

    def add_pre_scribe_equation(self, connection_point: int) -> EquationObject:
        """Returns an EquationObject for a pre describe equation.

        The returned equation object represents the prescribed mass flow rate or pressure
        equation for the asset at the given connection point.

        The equation is:

        - If pre_scribe_mass_flow is True, then Mass flow rate at connection point = Mass flow rate
        property
        - If pre_scribe_mass_flow is False, then Pressure at connection point = Set pressure
        property
        :param int connection_point: The connection point for which to add the equation
        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation.
        """
        # Raise IndexError if the connection point is not available
        if connection_point >= self.number_of_connection_point:
            raise IndexError("The connection point is not available.")

        # Create equation object
        equation_object = EquationObject()
        if self.pre_scribe_mass_flow:
            equation_object.indices = np.array(
                [
                    self.get_index_matrix(property_name="mass_flow_rate",
                                          connection_point=connection_point)
                ]
            )
            equation_object.coefficients = np.array([-1.0 + 2 * connection_point])
            equation_object.rhs = self.mass_flow_rate_set_point
        else:
            equation_object.indices = np.array([
                self.get_index_matrix(property_name="pressure",
                                      connection_point=connection_point)]
            )
            equation_object.coefficients = np.array([1.0])
            if connection_point == 0:
                equation_object.rhs = 0.5 * self.set_pressure
            else:
                equation_object.rhs = self.set_pressure
        return equation_object

    def add_thermal_equations(self, connection_point: int) -> EquationObject:
        """Adds a thermal equation for a connection point of the asset.

        :param connection_point: The index of the connection point to add the equation for.
        :type connection_point: int
        :return: An equation object representing the thermal equation.
        :rtype: EquationObject
        """
        if self.prev_sol[self.get_index_matrix(property_name="mass_flow_rate",
                                               connection_point=connection_point,
                                               matrix=False)] > 0:
            return self.add_prescribe_temp(connection_point)
        else:
            return self.add_temp_to_node_equation(connection_point)
