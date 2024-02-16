"""Module containing the node class."""
import uuid
from simulator_core.solver.network.assets.BaseItem import BaseItem
from simulator_core.solver.network.assets.Baseasset import BaseAsset
from simulator_core.solver.matrix.equation_object import EquationObject
from simulator_core.solver.matrix.core_enum import IndexEnum, NUMBER_CORE_QUANTITIES


class Node(BaseItem):
    """
    A class to represent a node in a network.

    This class inherits from the BaseItem class and implements the methods to generate the
    equations for the node.

    Attributes
    ----------
    connected_assets : list[list[BaseAsset, int]]
        A list of lists that store the asset objects and the connection point indices that
        are connected to the node.

    Methods
    -------
    connect_asset(asset: BaseAsset, con_point: int)
        Connects an asset object to the node at the given connection point index.
    get_equations() -> list[EquationObject]
        Returns a list of EquationObjects that represent the equations for the node.
    add_energy_equations() -> EquationObject
        Returns an EquationObject that represents the energy balance equation for the node.
    add_node_cont_equation() -> EquationObject
        Returns an EquationObject that represents the mass flow rate continuity equation for
        the node.
    add_discharge_equation() -> EquationObject
        Returns an EquationObject that represents the discharge equation for the node.
    add_pressure_set_equation() -> EquationObject
        Returns an EquationObject that represents the pressure set equation for the node.
    set_temperature_equation() -> EquationObject
        Returns an EquationObject that represents the temperature set equation for the node.
    add_energy_equation() -> EquationObject
        Returns an EquationObject that represents the energy equation for the node.
    is_connected() -> bool
        Returns True if the node is connected to any asset, False otherwise.
    """

    def __init__(self, name: uuid.UUID, number_of_unknowns: int = 3, height: float = 0.0,
                 initial_temperature: float = 373.15, set_pressure: float = 10000.0):
        """Initializes the Node object with the given parameters.

        :param uuid.UUID name: The unique identifier of the node.
        :param int, optional number_of_unknowns: The number of unknown variables for the node.
        The default is 3.
        """
        super().__init__(number_of_unknowns, name)
        self.connected_assets = []
        self.height = height
        self.initial_temperature = initial_temperature
        self.set_pressure = set_pressure

    def connect_asset(self, asset: BaseAsset, con_point: int):
        """Connects an asset object at the given connection point to the node .

        :param BaseAsset asset: The asset object that is connected to the node.
        :param int con_point: The connection point for the asset which is connected to this node.
        :return:
        """
        self.connected_assets.append([asset, con_point])

    def get_equations(self) -> list[EquationObject]:
        """Returns a list of EquationObjects that represent the equations for the node.

        The equations are:

        - Mass flow rate continuity equation
        - Energy balance equation
        - Discharge equation
        :return: list[EquationObject]
            A list of EquationObjects that contain the indices, coefficients, and right-hand side
            values of the equations.
        """
        equations = [self.add_node_cont_equation(),
                     self.add_energy_equations(),
                     self.add_discharge_equation()]
        return equations

    def add_energy_equations(self) -> EquationObject:
        """Returns an EquationObject that represents the energy balance equation for the node.

        When the mass flow rate of all connected components is smaller or equal 0.
        Then the node will pre-scribe its temperature otherwise it will give
        an equation where the sum of mass flow rat times specific internal energy is zero.


        :return: EquationObject An EquationObject that contains the indices, coefficients,
            and right-hand side value of the equation.
        """
        flows = [asset[0].prev_sol[IndexEnum.discharge
                                   + asset[1] * NUMBER_CORE_QUANTITIES]
                 <= 0 for asset in self.connected_assets]
        if all(flows):
            return self.set_temperature_equation()
        else:
            return self.add_energy_equation()

    def add_node_cont_equation(self) -> EquationObject:
        """Returns an EquationObject that represents the mass continuity equation for the node.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side value
            of the equation.
        """
        equation_object = EquationObject()
        equation_object.indices = [self.matrix_index + IndexEnum.discharge]
        equation_object.coefficients = [1.0]
        equation_object.rhs = 0.0
        for asset in self.connected_assets:
            equation_object.indices.append(asset[0].matrix_index + IndexEnum.discharge
                                           + asset[1] * NUMBER_CORE_QUANTITIES)
            equation_object.coefficients.append(1.0)
        return equation_object

    def add_discharge_equation(self) -> EquationObject:
        """Returns an EquationObject that represents the discharge is zero equation for the node.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation.
        """
        equation_object = EquationObject()
        equation_object.indices = [self.matrix_index + IndexEnum.discharge]
        equation_object.coefficients = [1.0]
        equation_object.rhs = 0.0
        return equation_object

    def add_pressure_set_equation(self) -> EquationObject:
        """Returns an EquationObject that sets the pressure of the node to a pre-defined value.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation.
        """
        equation_object = EquationObject()
        equation_object.indices = [self.matrix_index + IndexEnum.pressure]
        equation_object.coefficients = [1.0]
        equation_object.rhs = self.set_pressure
        return equation_object

    def set_temperature_equation(self) -> EquationObject:
        """Returns an EquationObject that sets the temperature of the node to a pre-defined value.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation.
        """
        equation_object = EquationObject()
        equation_object.indices = [self.matrix_index + IndexEnum.internal_energy]
        equation_object.coefficients = [1.0]
        equation_object.rhs = self.fluid_properties.get_ie(self.initial_temperature)
        return equation_object

    def add_energy_equation(self) -> EquationObject:
        """Returns an EquationObject that represents the energy equation for the node.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation
        """
        equation_object = EquationObject()
        equation_object.indices = [self.matrix_index + IndexEnum.discharge,
                                   self.matrix_index + IndexEnum.internal_energy]
        equation_object.coefficients = [self.prev_sol[2], self.prev_sol[0]]
        equation_object.rhs = self.prev_sol[0] * self.prev_sol[2]
        for asset in self.connected_assets:
            equation_object.indices.append(asset[0].matrix_index
                                           + IndexEnum.discharge
                                           + asset[1] * NUMBER_CORE_QUANTITIES)
            equation_object.indices.append(asset[0].matrix_index + IndexEnum.internal_energy
                                           + asset[1] * NUMBER_CORE_QUANTITIES)
            prev_sol = asset[0].prev_sol
            equation_object.coefficients.append(prev_sol[asset[1] * 3 + 2])
            equation_object.coefficients.append(prev_sol[asset[1] * 3])
            equation_object.rhs += prev_sol[asset[1] * 3] * prev_sol[asset[1] * 3 + 2]
        return equation_object

    def is_connected(self) -> bool:
        """Returns True if the node is connected to any asset, False otherwise.

        :return: bool
            A boolean value that indicates whether the node is connected or not.
        """
        return len(self.connected_assets) > 0
