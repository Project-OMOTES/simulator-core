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
    initialize_energy_equation() -> None
        Creates and stores the energy equation object with its matrix indices.
    get_energy_equation() -> EquationObject
        Returns an EquationObject that represents the energy equation for the node.
    reset_cached_equations() -> None
        Invalidates the equation objects which are stored on the node.
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

        :param str name: The name of the node.
        :param str _id: The unique identifier of the node.
        :param int number_of_unknowns: The number of unknown variables for the node.
            The default is 3.
        :param float height: The node height [m].
        :param float initial_temperature: The initial node temperature [K].
        :param float set_pressure: The prescribed node pressure [Pa].
        """
        super().__init__(name=name, _id=_id, number_of_unknowns=number_of_unknowns)
        self.connected_assets: list[tuple[BaseItem, int]] = []
        self.height = height
        self.initial_temperature = initial_temperature
        self._cached_initial_temperature: float | None = None
        self._cached_initial_internal_energy: float = 0.0
        self.set_pressure = set_pressure
        self.energy_equation_object: EquationObject | None = None
        self._energy_equation_contributors: list[tuple[BaseItem | "Node", int, int]] = []
        self._mass_flow_lookup: list[tuple[BaseItem, int]] | None = None
        self.node_cont_equation_object: EquationObject | None = None
        self.discharge_equation_object: EquationObject | None = None
        self.temperature_equation_object: EquationObject | None = None

    def reset_cached_equations(self) -> None:
        """Resets the cached equation objects of the node.

        :return: None
        """
        self.energy_equation_object = None
        self._energy_equation_contributors = []
        self._mass_flow_lookup = None
        self.node_cont_equation_object = None
        self.discharge_equation_object = None
        self.temperature_equation_object = None

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
            # The structure of the equations changed, so the cache is invalidated.
            self.reset_cached_equations()

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
        if self._mass_flow_lookup is None:
            self._mass_flow_lookup = [
                (
                    asset,
                    asset.get_index_matrix(
                        "mass_flow_rate", asset_connection_point, use_relative_indexing=True
                    ),
                )
                for asset, asset_connection_point in self.connected_assets
            ]
        # The node prescribes its temperature when all flows are positive, all flows are
        # negative or all flows are zero within the mass flow limit.
        all_positive = True
        all_negative = True
        all_zero = True
        massflow_zero_limit = self.massflow_zero_limit
        for asset, mass_flow_index in self._mass_flow_lookup:
            mass_flow_rate = asset.prev_sol[mass_flow_index]
            if mass_flow_rate <= 0.0:
                all_positive = False
            if mass_flow_rate >= 0.0:
                all_negative = False
            if not -massflow_zero_limit <= mass_flow_rate <= massflow_zero_limit:
                all_zero = False
            if not (all_positive or all_negative or all_zero):
                return self.get_energy_equation()
        return self.set_temperature_equation()

    def get_node_cont_equation(self) -> EquationObject:
        """Returns an EquationObject that represents the mass continuity equation for the node.

        The equation is constant, so it is created once and stored on the node. Do not modify
        the returned equation object, since it is reused for every iteration.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side value
            of the equation.
        """
        if self.node_cont_equation_object is not None:
            return self.node_cont_equation_object
        equation_object = EquationObject()
        indices = [
            self.get_index_matrix(property_name="mass_flow_rate", use_relative_indexing=False)
        ]
        for asset, asset_connection_point in self.connected_assets:
            indices.append(
                asset.get_index_matrix(
                    property_name="mass_flow_rate",
                    connection_point=asset_connection_point,
                    use_relative_indexing=False,
                )
            )
        equation_object.indices = np.array(indices)
        equation_object.coefficients = np.ones(len(indices))
        equation_object.rhs = 0.0
        self.node_cont_equation_object = equation_object
        return equation_object

    def get_discharge_equation(self) -> EquationObject:
        """Returns an EquationObject that represents the discharge is zero equation for the node.

        The equation is constant, so it is created once and stored on the node. Do not modify
        the returned equation object, since it is reused for every iteration.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation.
        """
        if self.discharge_equation_object is not None:
            return self.discharge_equation_object
        equation_object = EquationObject()
        equation_object.indices = np.array(
            [self.get_index_matrix(property_name="mass_flow_rate", use_relative_indexing=False)]
        )
        equation_object.coefficients = np.array([1.0])
        equation_object.rhs = 0.0
        self.discharge_equation_object = equation_object
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

        The indices and coefficients of the equation are constant, so they are created once and
        stored on the node. Only the right-hand side is updated. Do not modify the returned
        equation object, since it is reused for every iteration.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation.
        """
        equation_object = self.temperature_equation_object
        if equation_object is None:
            equation_object = EquationObject()
            equation_object.indices = np.array(
                [
                    self.get_index_matrix(
                        property_name="internal_energy", use_relative_indexing=False
                    )
                ]
            )
            equation_object.coefficients = np.array([1.0])
            self.temperature_equation_object = equation_object
        # The initial temperature only changes between time steps, so the internal energy is
        # calculated once per initial temperature instead of once per iteration.
        initial_temperature = self.initial_temperature
        if initial_temperature != self._cached_initial_temperature:
            self._cached_initial_internal_energy = fluid_props.get_ie(initial_temperature)
            self._cached_initial_temperature = initial_temperature
        equation_object.rhs = self._cached_initial_internal_energy
        return equation_object

    def initialize_energy_equation(self) -> None:
        """Creates the energy equation object and stores it on the node.

        The matrix indices of the equation only depend on the matrix index of the node, the
        matrix indices of the connected assets and the connection points. These are fixed once
        the matrix indices have been set, so they are determined once and reused every
        iteration. Only the coefficients and the right-hand side are updated afterwards, see
        :meth:`get_energy_equation`.

        :return: None
        """
        equation_object = EquationObject()
        contributors: list[tuple[BaseItem | "Node", int, int]] = []
        # Indices of the node itself.
        node_mass_flow_index = self.get_index_matrix(
            property_name="mass_flow_rate", use_relative_indexing=False
        )
        node_internal_energy_index = self.get_index_matrix(
            property_name="internal_energy", use_relative_indexing=False
        )
        indices = [node_mass_flow_index, node_internal_energy_index]
        contributors.append(
            (
                self,
                node_mass_flow_index - self.matrix_index,
                node_internal_energy_index - self.matrix_index,
            )
        )
        # Indices of the connected assets.
        for asset, asset_connection_id in self.connected_assets:
            asset_mass_flow_index = asset.get_index_matrix(
                "mass_flow_rate", asset_connection_id, use_relative_indexing=False
            )
            asset_internal_energy_index = asset.get_index_matrix(
                "internal_energy", asset_connection_id, use_relative_indexing=False
            )
            indices.append(asset_mass_flow_index)
            indices.append(asset_internal_energy_index)
            contributors.append(
                (
                    asset,
                    asset_mass_flow_index - asset.matrix_index,
                    asset_internal_energy_index - asset.matrix_index,
                )
            )
        # Verify that the relative indices fit in the previous solution of their owner.
        for item, mass_flow_index, internal_energy_index in contributors:
            number_of_unknowns = len(item.prev_sol)
            if (
                max(mass_flow_index, internal_energy_index) >= number_of_unknowns
                or min(mass_flow_index, internal_energy_index) < 0
            ):
                raise IndexError(
                    f"Energy equation of node {self.name} requires indices "
                    f"{[mass_flow_index, internal_energy_index]} of {item.name}, which only has "
                    f"{number_of_unknowns} unknowns."
                )
        equation_object.indices = np.array(indices)
        equation_object.coefficients = np.zeros(len(indices))
        equation_object.rhs = 0.0
        self.energy_equation_object = equation_object
        self._energy_equation_contributors = contributors

    def get_energy_equation(self) -> EquationObject:
        """Returns an EquationObject that represents the energy equation for the node.

        The equation object is created once by :meth:`initialize_energy_equation`. This method
        only updates the coefficients and the right-hand side of the stored equation object
        using the latest previous solution of the node and the connected assets.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side
            value of the equation
        """
        if self.energy_equation_object is None:
            self.initialize_energy_equation()
        equation_object = self.energy_equation_object
        assert equation_object is not None
        coefficients = equation_object.coefficients
        rhs = 0.0
        position = 0
        for item, mass_flow_index, internal_energy_index in self._energy_equation_contributors:
            prev_sol = item.prev_sol
            mass_flow_rate = prev_sol[mass_flow_index]
            internal_energy = prev_sol[internal_energy_index]
            # Be aware that the coefficients are in reverse order
            coefficients[position] = internal_energy
            coefficients[position + 1] = mass_flow_rate
            rhs += mass_flow_rate * internal_energy
            position += 2
        equation_object.rhs = rhs
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
