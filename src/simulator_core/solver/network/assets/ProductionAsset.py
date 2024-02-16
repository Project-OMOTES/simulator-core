"""Module containing the production asset class."""
import uuid
from simulator_core.solver.matrix.equation_object import EquationObject
from simulator_core.solver.network.assets.Fall_type import FallType
from simulator_core.solver.matrix.core_enum import IndexEnum, NUMBER_CORE_QUANTITIES


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

    def __init__(self, name: uuid.UUID,
                 number_of_unknowns: int = 6,
                 number_con_points: int = 2,
                 supply_temperature: float = 293.15,
                 heat_supplied: float = 0.0,
                 loss_coefficient: float = 1.0,
                 pre_scribe_mass_flow: bool = True,
                 mass_flow_rate_set_point: float = 10.0,
                 set_pressure: float = 10000.0):
        """
        Initializes the ProductionAsset object with the given parameters.

        Parameters
        ----------
        name : uuid.UUID The unique identifier of the asset.
        number_of_unknowns : int, optional
            The number of unknown variables for the asset. The default is 6, which corresponds to
            the mass flow rate, pressure, and temperature at each connection point.
        number_con_points : int, optional
            The number of connection points for the asset. The default is 2, which corresponds to
            the inlet and outlet.
        """
        super().__init__(name, number_of_unknowns, number_con_points,
                         supply_temperature=supply_temperature,
                         heat_supplied=heat_supplied,
                         loss_coefficient=loss_coefficient)
        self.number_of_connection_point = number_con_points
        self.pre_scribe_mass_flow = pre_scribe_mass_flow
        self.mass_flow_rate_set_point = mass_flow_rate_set_point
        self.set_pressure = set_pressure

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
        equations = [super().add_press_to_node_equation(0),
                     super().add_press_to_node_equation(1),
                     self.add_thermal_equations(0),
                     self.add_thermal_equations(1),
                     self.add_pre_scribe_equation(0),
                     self.add_pre_scribe_equation(1)]
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
        equation_object = EquationObject()
        if self.pre_scribe_mass_flow:
            equation_object.indices = [self.matrix_index + IndexEnum.discharge
                                       + connection_point * NUMBER_CORE_QUANTITIES]
            equation_object.coefficients = [-1.0 + 2 * connection_point]
            equation_object.rhs = self.mass_flow_rate_set_point
        else:
            equation_object.indices = [self.matrix_index + IndexEnum.pressure
                                       + connection_point * NUMBER_CORE_QUANTITIES]
            equation_object.coefficients = [1.0]
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
        if self.prev_sol[IndexEnum.discharge + connection_point * NUMBER_CORE_QUANTITIES] > 0:
            return self.add_prescribe_temp(connection_point)
        else:
            return self.add_temp_to_node_equation(connection_point)