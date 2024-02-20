"""Module containing the Fall type class."""
import uuid
import numpy as np
from simulator_core.solver.network.assets.Baseasset import BaseAsset
from simulator_core.solver.matrix.equation_object import EquationObject
from simulator_core.solver.matrix.core_enum import IndexEnum, NUMBER_CORE_QUANTITIES


class FallType(BaseAsset):
    """A class to represent a fall type asset in a network.

    This class inherits from the BaseAsset class and implements the methods to generate the
    equations for the fall type asset.

    Attributes
    ----------
    connected_nodes : list[int]
        A list of integers that store the node indices that are connected to the asset.
    number_of_connection_point : int
        The number of connection points for the asset.

    Methods
    -------
    get_equations() -> list[EquationObject]
        Returns a list of EquationObjects that represent the equations for the asset.
    add_equations()
        Adds the equations for the asset to the equation system.
    add_internal_cont_equation() -> EquationObject
        Returns an EquationObject that represents the internal continuity equation for the asset.
    add_internal_pressure_loss_equation() -> EquationObject
        Returns an EquationObject that represents the internal pressure loss equation for the asset.
    add_internal_energy_equation() -> EquationObject
        Returns an EquationObject that represents the internal energy equation for the asset.
    update_pressure_loss_equation() -> EquationObject
        Returns an updated EquationObject that represents the internal pressure loss equation
        for the asset.
    """

    def __init__(self, name: uuid.UUID,
                 number_of_unknowns: int = 6,
                 number_con_points: int = 2,
                 supply_temperature: float = 293.15,
                 heat_supplied: float = 0.0,
                 loss_coefficient: float = 1.0):
        """
        Initializes the FallType object with the given parameters.

        Parameters
        ----------
        name : uuid.UUID
            The unique identifier of the asset.
        number_of_unknowns : int, optional
            The number of unknown variables for the asset. The default is 6, which corresponds
            to the mass flow rate, pressure, and temperature at each connection point.
        number_con_points : int, optional
            The number of connection points for the asset. The default is 2, which corresponds to
            the inlet and outlet.
        """
        super().__init__(name, number_of_unknowns, number_con_points,
                         supply_temperature=supply_temperature)
        self.number_of_connection_point = number_con_points
        self.heat_supplied = heat_supplied
        self.loss_coefficient = loss_coefficient

    def get_equations(self) -> list[EquationObject]:
        """Returns a list of EquationObjects that represent the equations for the asset.

         The equations are:

        - Pressure balance at each connection point
        - Thermal balance at each connection point
        - Internal continuity equation
        - Internal pressure loss equation
        :return: list[EquationObject]
            A list of EquationObjects that contain the indices, coefficients, and right-hand side
            values of the equations.
        """
        equations = [self.add_press_to_node_equation(0),
                     self.add_press_to_node_equation(1),
                     self.add_thermal_equations(0),
                     self.add_thermal_equations(1),
                     self.add_internal_cont_equation(),
                     self.add_internal_pressure_loss_equation()
                     ]
        return equations

    def add_thermal_equations(self, connection_point: int) -> EquationObject:
        """Adds a thermal equation for a connection point of the asset.

        :param connection_point: The index of the connection point to add the equation for.
        :type connection_point: int
        :return: An equation object representing the thermal equation.
        :rtype: EquationObject
        """
        if self.prev_sol[0 + connection_point * 3] > 0:
            return self.add_internal_energy_equation()
        else:
            return self.add_temp_to_node_equation(connection_point)

    def add_internal_cont_equation(self) -> EquationObject:
        """Returns an EquationObject that represents the internal continuity equation for the asset.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side value
            of the equation.
        """
        equation_object = EquationObject()
        equation_object.indices = np.array([self.matrix_index + IndexEnum.discharge,
                                            self.matrix_index + IndexEnum.discharge
                                            + NUMBER_CORE_QUANTITIES])
        equation_object.coefficients = np.array([1.0, 1.0])
        equation_object.rhs = 0.0
        return equation_object

    def add_internal_energy_equation(self) -> EquationObject:
        """Returns an EquationObject that represents the internal energy equation for the asset.

         The equation is:

        - Mass flow rate at inlet * Specific internal energy at inlet
        + Mass flow rate at outlet * Specific internal energy at outlet - Heat supplied = 0

        :return:EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side value of
            the equation.
        """
        equation_object = EquationObject()
        equation_object.indices = np.array([self.matrix_index + IndexEnum.discharge,
                                            self.matrix_index + IndexEnum.internal_energy,
                                            self.matrix_index + IndexEnum.discharge
                                            + NUMBER_CORE_QUANTITIES,
                                            self.matrix_index + IndexEnum.internal_energy
                                            + NUMBER_CORE_QUANTITIES])
        equation_object.coefficients = np.array([self.prev_sol[2],
                                                 self.prev_sol[0],
                                                 self.prev_sol[5],
                                                 self.prev_sol[3]])
        equation_object.rhs = (self.prev_sol[0] * self.prev_sol[2]
                               + self.prev_sol[3] * self.prev_sol[5]
                               + self.heat_supplied)
        return equation_object

    def add_internal_pressure_loss_equation(self) -> EquationObject:
        """Returns an EquationObject that represents the pressure loss equation for the asset.

         The equation is:

        - Pressure at inlet - Pressure at outlet - 2 * Loss coefficient * Mass flow rate *
        abs(Mass flow rate) = 0
        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side value
            of the equation.
        """
        equation_object = EquationObject()
        equation_object.indices = np.array([self.matrix_index + IndexEnum.discharge,
                                            self.matrix_index + IndexEnum.pressure,
                                            self.matrix_index + IndexEnum.pressure
                                            + NUMBER_CORE_QUANTITIES])
        self.update_loss_coefficient()
        if self.prev_sol[0] < 1e-5:
            equation_object.coefficients = np.array([-2.0 * self.loss_coefficient * 1e-5,
                                                     -1.0, 1.0])
            equation_object.rhs = -self.loss_coefficient * self.prev_sol[0] * 1e-5
        else:
            equation_object.coefficients = np.array([-2.0 * self.loss_coefficient
                                                     * abs(self.prev_sol[0]), -1.0, 1.0])
            equation_object.rhs = (-self.loss_coefficient * self.prev_sol[0]
                                   * abs(self.prev_sol[0]))
        return equation_object

    def update_loss_coefficient(self) -> None:
        """Basic function which does not do anything, but can be overwritten in derived classes."""
        pass
