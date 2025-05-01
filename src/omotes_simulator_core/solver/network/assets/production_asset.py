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
"""Implementation of the HeatBoundary class."""
import numpy as np

from omotes_simulator_core.solver.matrix.equation_object import EquationObject
from omotes_simulator_core.solver.network.assets.fall_type import FallType


class HeatBoundary(FallType):
    """
    A class to represent a heat boundary in a network.

    This class inherits from the FallType class and implements the methods to generate
    the equations for the heat boundary.

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
    get_pre_scribe_mass_flow_or_pressure_equations(connection_point: int) -> EquationObject
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
        heat_flux: float = 0.0,
        loss_coefficient: float = 1.0,
        pre_scribe_mass_flow: bool = True,
        mass_flow_rate_set_point: float = 10.0,
        set_pressure: float = 10000.0,
    ):
        """
        Initializes the HeatBoundary object with the given parameters.

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
            heat_flux=heat_flux,
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
            super().get_press_to_node_equation(0),
            super().get_press_to_node_equation(1),
            self.get_thermal_equations(0),
            self.get_thermal_equations(1),
            self.get_pre_scribe_mass_flow_or_pressure_equations(0),
            self.get_pre_scribe_mass_flow_or_pressure_equations(1),
        ]
        return equations

    def get_pre_scribe_mass_flow_or_pressure_equations(
        self, connection_point: int
    ) -> EquationObject:
        """Returns an EquationObject for a pre describe equation.

        The returned equation object represents the prescribed mass flow rate or pressure
        equation for the asset at the given connection point.

        The equation is:

        - If pre_scribe_mass_flow is True, then Mass flow rate at connection point = Mass flow rate
        property
        - If pre_scribe_mass_flow is False, then Pressure at connection point = Set pressure
        property
        :param int connection_point: The connection point for which to get the equation
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
                    self.get_index_matrix(
                        property_name="mass_flow_rate",
                        connection_point=connection_point,
                        use_relative_indexing=False,
                    )
                ]
            )
            equation_object.coefficients = np.array([-1.0 + 2 * connection_point])
            equation_object.rhs = self.mass_flow_rate_set_point
        else:
            equation_object.indices = np.array(
                [
                    self.get_index_matrix(
                        property_name="pressure",
                        connection_point=connection_point,
                        use_relative_indexing=False,
                    )
                ]
            )
            equation_object.coefficients = np.array([1.0])
            if connection_point == 0:
                equation_object.rhs = 0.5 * self.set_pressure
            else:
                equation_object.rhs = self.set_pressure
        return equation_object

    def get_thermal_equations(self, connection_point: int) -> EquationObject:
        """Gets a thermal equation for a connection point of the asset.

        :param connection_point: The index of the connection point to get the equation for.
        :type connection_point: int
        :return: An equation object representing the thermal equation.
        :rtype: EquationObject
        """
        if (
            self.prev_sol[
                self.get_index_matrix(
                    property_name="mass_flow_rate",
                    connection_point=connection_point,
                    use_relative_indexing=True,
                )
            ]
            > self.massflow_zero_limit
        ):
            return self.get_prescribe_temp_equation(connection_point)
        else:
            return self.get_internal_energy_to_node_equation(connection_point)
