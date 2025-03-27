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

"""Module containing the node class."""
import numpy as np

from omotes_simulator_core.solver.matrix.equation_object import EquationObject
from omotes_simulator_core.solver.network.assets.base_item import BaseItem
from omotes_simulator_core.solver.network.assets.base_node_item import BaseNodeItem
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


class Node(BaseNodeItem):
    """
    A class to represent a node in a network.

    This class inherits from the BaseItem class and implements the methods to generate the
    equations for the node.

    Attributes
    ----------
    connected_assets : list[list[BaseItem, int]]
        A list of lists that store the asset objects and the connection point indices that
        are connected to the node.

    Methods
    -------
    connect_asset(asset: BaseItem, connection_point: int)
        Connects an asset object to the node at the given connection point index.
    get_equations() -> list[EquationObject]
        Returns a list of EquationObjects that represent the equations for the node.
    get_energy_equations() -> EquationObject
        Returns an EquationObject that represents the energy balance equation for the node.
    get_node_cont_equation() -> EquationObject
        Returns an EquationObject that represents the mass flow rate continuity equation for
        the node.
    get_discharge_equation() -> EquationObject
        Returns an EquationObject that represents the discharge equation for the node.
    get_pressure_set_equation() -> EquationObject
        Returns an EquationObject that represents the pressure set equation for the node.
    set_temperature_equation() -> EquationObject
        Returns an EquationObject that represents the temperature set equation for the node.
    get_energy_equation() -> EquationObject
        Returns an EquationObject that represents the energy equation for the node.
    is_connected() -> bool
        Returns True if the node is connected to any asset, False otherwise.
    """

    def __init__(
        self,
        name: str,
        _id: str,
        number_of_unknowns: int = 3,
        height: float = 0.0,
        initial_temperature: float = 273.15,
        set_pressure: float = 10000.0,
    ):
        """Initializes the Node object with the given parameters.

        :param uuid.UUID name: The unique identifier of the node.
        :param int, optional number_of_unknowns: The number of unknown variables for the node.
        The default is 3.
        """
        super().__init__(name=name, _id=_id, number_of_unknowns=number_of_unknowns)
        self.connected_assets: list[tuple[BaseItem, int]] = []
        self.height = height
        self.initial_temperature = initial_temperature
        self.set_pressure = set_pressure

    def connect_asset(self, asset: BaseItem, connection_point: int) -> None:
        """Connects an asset object at the given connection point to the node .

        :param BaseAsset asset: The asset object that is connected to the node.
        :param int connection_point: The connection point for the asset which is connected to this
            node.
        :return:
        """
        if connection_point > (asset.number_of_connection_point - 1):
            raise ValueError(
                f"Connection point {connection_point} does not exist on asset {asset.name}."
            )
        # Check if the asset is already connected to the node at the given connection point
        if set((asset, connection_point)) in set(self.connected_assets):
            raise ValueError(
                f"Asset {asset.name} is already connected to node {self.name} at connection"
                + f" point {connection_point}."
            )
        else:
            # Connect the asset to the node
            self.connected_assets.append((asset, connection_point))

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
        # Check connection
        if not self.is_connected():
            raise ValueError(f"Node {self.name} is not connected to any asset.")
        # Construct equation object
        equations = [
            self.get_node_cont_equation(),
            self.get_energy_equations(),
            self.get_discharge_equation(),
        ]
        return equations

    def get_energy_equations(self) -> EquationObject:
        """Returns an EquationObject that represents the energy balance equation for the node.

        When the mass flow rate of all connected components is smaller or equal 0.
        Then the node will pre-scribe its temperature otherwise it will give
        an equation where the sum of mass flow rat times specific internal energy is zero.


        :return: EquationObject An EquationObject that contains the indices, coefficients,
            and right-hand side value of the equation.
        """
        flows = np.array(
            [
                asset.prev_sol[
                    asset.get_index_matrix(
                        "mass_flow_rate", asset_connection_point, use_relative_indexing=True
                    )
                ]
                for asset, asset_connection_point in self.connected_assets
            ]
        )

        if (
            all(np.sign(flows) == 1)
            or all(np.sign(flows) == -1)
            or all(abs(flows) <= self.massflow_zero_limit)
        ):
            return self.set_temperature_equation()
        else:
            return self.get_energy_equation()

    def get_node_cont_equation(self) -> EquationObject:
        """Returns an EquationObject that represents the mass continuity equation for the node.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side value
            of the equation.
        """
        equation_object = EquationObject()
        equation_object.indices = np.array(
            [self.get_index_matrix(property_name="mass_flow_rate", use_relative_indexing=False)]
        )
        equation_object.coefficients = np.array([1.0])
        equation_object.rhs = 0.0
        for asset, asset_connection_point in self.connected_assets:
            equation_object.indices = np.append(
                equation_object.indices,
                [
                    asset.get_index_matrix(
                        property_name="mass_flow_rate",
                        connection_point=asset_connection_point,
                        use_relative_indexing=False,
                    )
                ],
            )
            equation_object.coefficients = np.append(equation_object.coefficients, [1.0])
        return equation_object

    def get_discharge_equation(self) -> EquationObject:
        """Returns an EquationObject that represents the discharge is zero equation for the node.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation.
        """
        equation_object = EquationObject()
        equation_object.indices = np.array(
            [self.get_index_matrix(property_name="mass_flow_rate", use_relative_indexing=False)]
        )
        equation_object.coefficients = np.array([1.0])
        equation_object.rhs = 0.0
        return equation_object

    def get_pressure_set_equation(self) -> EquationObject:
        """Returns an EquationObject that sets the pressure of the node to a pre-defined value.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation.
        """
        equation_object = EquationObject()
        equation_object.indices = np.array(
            [self.get_index_matrix(property_name="pressure", use_relative_indexing=False)]
        )
        equation_object.coefficients = np.array([1.0])
        equation_object.rhs = self.set_pressure
        return equation_object

    def set_temperature_equation(self) -> EquationObject:
        """Returns an EquationObject that sets the temperature of the node to a pre-defined value.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation.
        """
        equation_object = EquationObject()
        equation_object.indices = np.array(
            [self.get_index_matrix(property_name="internal_energy", use_relative_indexing=False)]
        )
        equation_object.coefficients = np.array([1.0])
        equation_object.rhs = fluid_props.get_ie(self.initial_temperature)
        return equation_object

    def get_energy_equation(self) -> EquationObject:
        """Returns an EquationObject that represents the energy equation for the node.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation
        """
        equation_object = EquationObject()
        equation_object.indices = np.array(
            [
                self.get_index_matrix(property_name="mass_flow_rate", use_relative_indexing=False),
                self.get_index_matrix(property_name="internal_energy", use_relative_indexing=False),
            ]
        )
        # Be aware that the coefficients are in reverse order
        equation_object.coefficients = np.array(self.prev_sol)[
            (equation_object.indices - self.matrix_index)[::-1]
        ]
        equation_object.rhs = float(np.prod(equation_object.coefficients))
        # Extend the equation_object with the indices and coefficients of the connected assets
        for asset, asset_connection_id in self.connected_assets:
            # Extended asset indices
            extra_indices = np.array(
                [
                    asset.get_index_matrix(
                        "mass_flow_rate", asset_connection_id, use_relative_indexing=False
                    ),
                    asset.get_index_matrix(
                        "internal_energy", asset_connection_id, use_relative_indexing=False
                    ),
                ]
            )
            # Extend the indices and coefficients of the equation object
            equation_object.indices = np.append(
                equation_object.indices,
                extra_indices,
            )
            # Extend the coefficients of the equation object
            prev_sol = np.array(asset.prev_sol)
            equation_object.coefficients = np.append(
                equation_object.coefficients,
                prev_sol[(extra_indices - asset.matrix_index)[::-1]],
            )
            # Extend the right-hand side of the equation object
            equation_object.rhs += np.prod(prev_sol[extra_indices - asset.matrix_index])
        return equation_object

    def is_connected(self) -> bool:
        """Returns True if the node is connected to any asset, False otherwise.

        :return: bool
            A boolean value that indicates whether the node is connected or not.
        """
        return len(self.connected_assets) > 0

    def get_connected_assets(self) -> list[tuple[BaseItem, int]]:
        """Returns the connected assets of the node.

        :return: Tuple[BaseItem, int]
            A tuple of the connected asset and the connection point index.
        """
        return self.connected_assets
