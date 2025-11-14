#  Copyright (c) 2025. Deltares & TNO
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
"""Implementation of the HeatBuffer class."""
import numpy as np

from omotes_simulator_core.solver.matrix.equation_object import EquationObject
from omotes_simulator_core.solver.network.assets.fall_type import FallType
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


class HeatBufferAsset(FallType):
    """
    A class to represent an ideal heat buffer in a network.

    This class inherits from the FallType class and implements the methods to generate
    the equations for an ideal heat buffer.

    Attributes
    ----------
    connected_nodes : list[int]
        A list of integers that store the node indices that are connected to the asset.
    number_of_connection_point : int
        The number of connection points for the asset.
    """

    inlet_massflow: float
    """The inlet (connection point 0) mass flow rate for the asset (based on volumetric flow)."""

    outlet_temperature: float
    """The outlet temperature for the asset, set by the controller."""

    inlet_temperature: float
    """The inlet temperature for the asset, set by the controller."""

    def __init__(
        self,
        name: str,
        _id: str,
        outlet_temperature: float = 293.15,
        inlet_temperature: float = 293.15,
        inlet_massflow: float = 10.0,
    ):
        """
        Initializes the HeatBuffer object with the given parameters.

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
        self.inlet_massflow = inlet_massflow

        # Set inlet and outlet temperatures
        self.inlet_temperature = inlet_temperature
        self.outlet_temperature = outlet_temperature

        # Initialize the FallType parent class
        super().__init__(
            name=name,
            _id=_id,
            supply_temperature=outlet_temperature,
        )

    def get_equations(self) -> list[EquationObject]:
        """Returns a list of EquationObjects that represent the equations for the asset.

        The equations are:
        - Pressure balance at each connection point
        - Thermal balance at each connection point
        - Internal continuity equation for mass flow

        :return: list[EquationObject]
            A list of EquationObjects that contain the indices, coefficients, and right-hand side
            values of the equations.
        """
        # Check if there are two nodes connected to the asset
        if len(self.connected_nodes) != 2:
            raise ValueError("The number of connected nodes must be 2!")
        # Check if the number of unknowns is 6
        if self.number_of_unknowns != 6:
            raise ValueError("The number of unknowns must be 6!")

        equations = [
            self.get_press_to_node_equation(0),  # Pressure balance at inlet (conn. pt -> node)
            self.get_press_to_node_equation(1),  # Pressure balance at outlet (conn. pt -> node)
            self.get_volumetric_continuity_equation(),  # Volumetric continuity equation
            self.get_mass_flow_equation(0),  # Prescribed mass flow at inlet
            self.get_thermal_equations(0),  # Thermal equation at inlet
            self.get_thermal_equations(1),  # Thermal equation at outlet
        ]
        return equations

    def get_volumetric_continuity_equation(self) -> EquationObject:
        """Returns an EquationObject to set the volumetric continuity equation.

        The returned equation object represents the volumetric continuity equation
        for the asset.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation.
        """
        # Get density at connection point 0 and 1
        rho_0 = fluid_props.get_density(self.inlet_temperature)
        rho_1 = fluid_props.get_density(self.outlet_temperature)

        # Create equation object
        equation_object = EquationObject()

        equation_object.indices = np.array(
            [
                self.get_index_matrix(
                    property_name="mass_flow_rate",
                    connection_point=0,
                    use_relative_indexing=False,
                ),
                self.get_index_matrix(
                    property_name="mass_flow_rate",
                    connection_point=1,
                    use_relative_indexing=False,
                ),
            ]
        )
        equation_object.coefficients = np.array([rho_1, -1 * rho_0])
        equation_object.rhs = 0.0

        return equation_object

    def get_mass_flow_equation(self, connection_point: int) -> EquationObject:
        """Returns an EquationObject to set the mass flow equation.

        The returned equation object represents the prescribed mass flow rate equation
        for the asset at the given connection point.

        m_dot(connection_point) = mass_flow_rate_set_point

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
        equation_object.rhs = self.inlet_massflow

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
