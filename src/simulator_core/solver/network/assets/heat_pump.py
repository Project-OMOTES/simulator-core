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

"""Module containing the HeatPump type class."""
import typing
import uuid
from typing import List

import numpy as np

from simulator_core.solver.matrix.core_enum import NUMBER_CORE_QUANTITIES, IndexEnum
from simulator_core.solver.matrix.equation_object import EquationObject
from simulator_core.solver.network.assets.base_asset import BaseAsset
from simulator_core.solver.utils.fluid_properties import fluid_props


class HeatPumpAsset(BaseAsset):
    """A class to represent a HeatPump asset in a network.

    This class inherits from the BaseAsset class and implements the methods to generate the
    equations for the HeatPump model.

    The HeatPump model has four connection points and thereby 12 unknowns. The equations for the
    HeatPump model are:
    1. Pressure to node equation at connection point 0
    2. Pressure to node equation at connection point 1
    3. Pressure to node equation at connection point 2
    4. Pressure to node equation at connection point 3

    # Internal energy at outflowing nodes
    5. Internal energy equation at connection point 0 when the flow direction is out of
    the node connected to connection point 0 (i.e., flow from nodes is positive).
    6. Internal energy equation at connection point 2 when the flow direction is out of
    the node connected to connection point 2 (i.e., flow from nodes is positive).

    # Temperature at inflowing nodes
    7. Temperature - via internal energy - at node connected to connection point 1 when
    the flow direction is out of the node connected to connection point 0 (i.e., flow from
    nodes is positive).
    8. Temperature - via internal energy - at node connected to connection point 3 when
    the flow direction is out of the node connected to connection point 2 (i.e., flow from
    nodes is positive).

    # Mass flow rate or pressure at nodes of producer side
    9. - 10.  Pre-scribe setpoint at the inflow of the producer side.
        - Set the mass flow at connection point 2, 3 to the prescribed value.
        - Set the pressure at connection point 2, 3 to the prescribed value.

    # Energy balance equation of the heat pump
    11. Continuity equation at consumer side.
    12. Energy balance equation for the HeatPump model.

    Assumptions:
    - The flow is positive when the mass flow rate at connection point 0 is positive.
    - There is no elevation difference between the connection points.

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

    def __init__(
        self,
        name: uuid.UUID,
        supply_temperature_primary: float = 293.15,
        supply_temperature_secondary: float = 293.15,
        cop_h: float = 1.0,
        pre_scribe_mass_flow: bool = True,
        mass_flow_rate_set_point: float = 10.0,
        pressure_set_point: float = 10000.0,
    ):
        """
        Initializes the HeatPump object with the given parameters.

        Parameters
        ----------
        name : uuid.UUID
            The unique identifier of the asset.
        supply_temperature_primary: float, optional
            The supply temperature of the asset on the hot side. The default is 293.15 K.
        supply_temperature_secondary: float, optional
            The supply temperature of the asset on the cold side. The default is 293.15 K.
        cop_h : float, optional
            The coefficient of performance of the heat pump. The default is 1.0.
        pre_scribe_mass_flow : bool
            A boolean flag that indicates whether the mass flow rate or the pressure is prescribed
            at the hot side of the heat pump.
        mass_flow_rate_set_point : float, optional
            The mass flow rate set point for the asset. The default is 10.0 kg/s.
        pressure_set_point : float, optional
            The pressure set point for the asset. The default is 10000.0 Pa.

        """
        super().__init__(
            name=name,
            number_of_unknowns=NUMBER_CORE_QUANTITIES * 4,
            number_connection_points=4,
        )
        # Define the supply temperature of the asset on the cold side
        self.supply_temperature_primary = supply_temperature_primary
        # Define the supply temperature of the asset on the hot side
        self.supply_temperature_secondary = supply_temperature_secondary
        # Define the coefficient of performance of the heat pump
        self.cop_h = cop_h
        # Define the flag that indicates whether the mass flow rate or the pressure is prescribed
        # at the hot side of the heat pump
        self.pre_scribe_mass_flow = pre_scribe_mass_flow
        # Define the mass flow rate set point for the asset
        self.mass_flow_rate_set_point = mass_flow_rate_set_point
        # Define the pressure set point for the asset
        self.pressure_set_point = pressure_set_point
        # Define the direction boolean
        self._direction_boolean = None

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
        # Check if there are two nodes connected to the asset
        if len(self.connected_nodes) != 4:
            raise ValueError("The number of connected nodes must be 4!")
        # Check if the number of unknowns is 12
        if self.number_of_unknowns != 12:
            raise ValueError("The number of unknowns must be 12!")
        # Set the direction boolean
        self._direction_boolean = self._set_direction_boolean()
        # Add the equations for the asset
        equations = [
            *[self.add_press_to_node_equation(connection_point=i) for i in range(4)],  # 4 equations
            *self.add_internal_energy_equations(),  # 2 equations
            *self.add_temperature_equations(),  # 2 equations
            *self.add_prescribed_mass_flow_or_pressure(),  # 2 equations
            self.add_internal_cont_equation(),  # 1 equation
            self.add_heat_pump_energy_equation(),  # 1 equation
        ]
        return equations

    def _set_direction_boolean(self) -> bool | None:
        """Returns a boolean that indicates the direction of the flow.

        The flow is positive when the mass flow rate at connection point 0 is positive.

        :return: bool
            A boolean that indicates the direction of the flow.
        """
        # if self.prev_sol[IndexEnum.discharge] < 0:
        #     return True
        # elif self.prev_sol[IndexEnum.discharge] > 0:
        #     return False
        # else:
        #     return None
        if self.supply_temperature_primary < self.supply_temperature_secondary:
            if self.prev_sol[IndexEnum.discharge + 0 * NUMBER_CORE_QUANTITIES] != 0:
                return True
            else:
                return None
        elif self.supply_temperature_primary > self.supply_temperature_secondary:
            if self.prev_sol[IndexEnum.discharge + 3 * NUMBER_CORE_QUANTITIES] != 0:
                return False
            else:
                return None
        else:
            return None

    def add_internal_energy_equations(self) -> List[EquationObject]:
        """Adds the internal energy equations for the asset.

        The connection points on which the internal energy is defined depend on the flow direction.
        The flow is positive when the mass flow rate at connection point 0 is positive.

        If the flow is:
        - Positive: The internal energy is defined at connection points 0 and 2.
        - Negative: The internal energy is defined at connection points 1 and 3.
        - Zero: The internal energy is defined at connection points 0 and 2.

        Connection points 0, 1 are on the producer side, and connection points 2, 3 are on the
        consumer side.

        :return: list[EquationObject]
            A list of EquationObjects that contain the indices, coefficients, and right-hand side
            values of the equations.
        """
        connection_point_1 = 0
        connection_point_2 = 2
        # if self._direction_boolean is True:  # self.prev_sol[IndexEnum.discharge] < 0:
        #     connection_point_1 = 0
        #     connection_point_2 = 2
        # elif self._direction_boolean is False:  # self.prev_sol[IndexEnum.discharge] > 0:
        #     connection_point_1 = 1
        #     connection_point_2 = 3
        # else:
        #     if self.supply_temperature_primary < self.supply_temperature_secondary:
        #         connection_point_1 = 0
        #         connection_point_2 = 2
        #     else:
        #         connection_point_1 = 1
        #         connection_point_2 = 3
        return [
            self.add_temp_to_node_equation(connection_point=connection_point_1),
            self.add_temp_to_node_equation(connection_point=connection_point_2),
        ]

    def add_temperature_equations(self) -> List[EquationObject]:
        """Adds the temperature equations for the asset.

        The connection points on which the temperature is defined depend on the flow direction.
        The flow is positive when the mass flow rate at connection point 0 is positive.

        If the flow is:
        - Positive: The temperature is defined at connection points 1 and 3. The temperature at
            connection point 1 is set to the supply temperature of the cold side, and the
            temperature at connection point 3 is set to the supply temperature of the hot side.
        - Negative: The temperature is defined at connection points 0 and 2. The temperature at
            connection point 0 is set to the supply temperature of the hot side, and the temperature
            at connection point 2 is set to the supply temperature of the cold side.
        - Zero: The temperature is defined at connection points 1 and 3. The temperature at
            connection point 1 is set to the supply temperature of the cold side, and the
            temperature at connection point 3 is set to the supply temperature of the hot side.

        :return: list[EquationObject]
            A list of EquationObjects that contain the indices, coefficients, and right-hand side
            values of the equations.
        """
        connection_point_1 = 1
        connection_point_2 = 3
        # if self._direction_boolean is True:  # self.prev_sol[IndexEnum.discharge] < 0:
        #     connection_point_1 = 1
        #     connection_point_2 = 3
        # elif self._direction_boolean is False:  # self.prev_sol[IndexEnum.discharge] > 0:
        #     connection_point_1 = 1
        #     connection_point_2 = 3
        # else:
        #     if self.supply_temperature_primary < self.supply_temperature_secondary:
        #         connection_point_1 = 1
        #         connection_point_2 = 3
        #     else:
        #         connection_point_1 = 1
        #         connection_point_2 = 3
        return [
            self.prescribe_temperature_at_connection_point(
                connection_point=connection_point_1,
                supply_temperature=self.supply_temperature_primary,
            ),
            self.prescribe_temperature_at_connection_point(
                connection_point=connection_point_2,
                supply_temperature=self.supply_temperature_secondary,
            ),
        ]

    def prescribe_temperature_at_connection_point(
        self, connection_point: int, supply_temperature: float
    ) -> EquationObject:
        """Adds a prescribed temperature equation for a connection point of the asset.

        :param connection_point: The index of the connection point to add the equation for.
        :type connection_point: int
        :param supply_temperature: The prescribed temperature at the connection point.
        :type supply_temperature: float
        :return: An equation object representing the prescribed temperature equation.
        :rtype: EquationObject
        """
        if not self.is_connected(connection_point=connection_point):
            raise ValueError(
                f"Connection point {connection_point} of asset {self.name} is not connected to a"
                + " node."
            )
        equation_object = EquationObject()
        equation_object.indices = np.array(
            [
                self.matrix_index
                + IndexEnum.internal_energy
                + connection_point * NUMBER_CORE_QUANTITIES
            ]
        )
        equation_object.coefficients = np.array([1.0])
        equation_object.rhs = fluid_props.get_ie(supply_temperature)
        return equation_object

    def add_internal_cont_equation(self) -> EquationObject:
        r"""Returns an EquationObject that represents the internal continuity equation for the asset.

        The internal continuity equation is set on either the hot or the cold side. The equation is
        given by:

        .. math::

                \sum{\dot{m}_i}_{i}^{N} = 0

        where :math:`\dot{m}_i` is the mass flow rate at connection point i.

        If the flow is:
        - Positive: The equation is set on the hot side.
        - Negative: The equation is set on the cold side.
        - Zero: The equation is set on the hot side.

        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side value
            of the equation.
        """
        # Determine flow direction
        if self._direction_boolean is True:  # self.prev_sol[IndexEnum.discharge] < 0:
            connection_point_1 = 0
            connection_point_2 = 1
        elif self._direction_boolean is False:  # self.prev_sol[IndexEnum.discharge] > 0:
            connection_point_1 = 2
            connection_point_2 = 3
        else:
            if self.supply_temperature_primary < self.supply_temperature_secondary:
                connection_point_1 = 0
                connection_point_2 = 1
            else:
                connection_point_1 = 2
                connection_point_2 = 3

        equation_object = EquationObject()
        equation_object.indices = np.array(
            [
                self.matrix_index
                + IndexEnum.discharge
                + connection_point_1 * NUMBER_CORE_QUANTITIES,
                self.matrix_index
                + IndexEnum.discharge
                + connection_point_2 * NUMBER_CORE_QUANTITIES,
            ]
        )
        equation_object.coefficients = np.array([1.0, 1.0])
        equation_object.rhs = 0.0
        return equation_object

    def _mass_flow_equations(self, connection_point: int, direction: float) -> EquationObject:
        """Returns an EquationObject that represents the prescribed mass flow rate or pressure.

        The returned equation object represents the prescribed mass flow rate or pressure equation
        for the asset at the given connection point.

        :param int connection_point: The connection point for which to add the equation.
        :param float direction: The direction of the flow to set the coefficients. The value should
        be -1.0 if the flow is from the node and 1.0 if the flow is to the node.
        :return: EquationObject
        """
        # Add the equations
        equation_object = EquationObject()
        equation_object.indices = np.array(
            [self.matrix_index + IndexEnum.discharge + connection_point * NUMBER_CORE_QUANTITIES]
        )
        equation_object.coefficients = np.array([direction])
        # TODO: Check if the correct sign is used for the mass flow rate set point
        equation_object.rhs = self.mass_flow_rate_set_point
        return equation_object

    def _pressure_equations(self, connection_point: int, pressure_side: bool) -> EquationObject:
        """Returns an EquationObject that represents the prescribed mass flow rate or pressure.

        The returned equation object represents the prescribed mass flow rate or pressure equation
        for the asset at the given connection point.

        :param int connection_point: The connection point for which to add the equation.
        :param float pressure_side: If True, the setpoint pressure is prescribed. If False, the
            half of the setpoint pressure is prescribed.
        :return: EquationObject
        """
        # Add the equations
        equation_object = EquationObject()
        # TODO: Check implementation if the hot/cold side of the heat pump are switched.
        equation_object.indices = np.array(
            [self.matrix_index + IndexEnum.pressure + connection_point * NUMBER_CORE_QUANTITIES]
        )
        equation_object.coefficients = np.array([1.0])
        # TODO: The connection point should be based on the flow direction!
        if pressure_side:
            equation_object.rhs = self.pressure_set_point
        else:
            equation_object.rhs = 0.5 * self.pressure_set_point
        return equation_object

    def add_prescribed_mass_flow_or_pressure(self) -> List[EquationObject]:
        """Returns a list of EquationObjects that represent the prescribed mass flow rate or
        pressure equations for the asset.

        The equations are:

        - If pre_scribe_mass_flow is True, then Mass flow rate at connection point = Mass flow rate
        property
        - If pre_scribe_mass_flow is False, then Pressure at connection point = Set pressure
        property

        The connection points on which the mass flow rate or pressure is prescribed depend on the
        flow direction.

        If the flow is:
        - Positive: The mass flow rate or pressure is prescribed at connection points 2 and 3.
        - Negative: The mass flow rate or pressure is prescribed at connection points 0 and 1.
        - Zero: The mass flow rate or pressure is prescribed at connection points 2 and 3.

        :return: list[EquationObject]
            A list of EquationObjects that contain the indices, coefficients, and right-hand side
            values of the equations.
        """
        # Determine flow direction
        if self._direction_boolean is True:  # self.prev_sol[IndexEnum.discharge] < 0:
            connection_point_1 = 2
            connection_point_2 = 3
        elif self._direction_boolean is False:  # self.prev_sol[IndexEnum.discharge] > 0:
            connection_point_1 = 0
            connection_point_2 = 1
        else:
            if self.supply_temperature_primary < self.supply_temperature_secondary:
                connection_point_1 = 2
                connection_point_2 = 3
            else:
                connection_point_1 = 0
                connection_point_2 = 1

        if self.pre_scribe_mass_flow:
            return [
                self._mass_flow_equations(connection_point=connection_point_1, direction=+1.0),
                self._mass_flow_equations(connection_point=connection_point_2, direction=-1.0),
            ]
        else:
            return [
                self._pressure_equations(connection_point=connection_point_1, pressure_side=False),
                self._pressure_equations(connection_point=connection_point_2, pressure_side=True),
            ]

    def _heat_pump_coefficients(self, direction: bool = True) -> np.ndarray:
        """Returns the coefficients for the heat pump equation.

        :param direction: bool
            The direction of the flow. True if the flow is positive, False otherwise.
        :return: np.ndarray
            The coefficients for the heat pump equation.
        """
        coefficient_array = np.array(
            [
                [
                    self.prev_sol[
                        IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * connection_point
                    ],
                    self.prev_sol[IndexEnum.discharge + NUMBER_CORE_QUANTITIES * connection_point],
                ]
                for connection_point in range(4)
            ]
        )
        # Reshape array
        coefficient_array = coefficient_array.reshape((8,))
        if direction:
            return typing.cast(
                np.ndarray,
                coefficient_array
                * np.array([-1, -1, +1, +1, +(1 - 1 / self.cop_h), +1, -(1 - 1 / self.cop_h), -1]),
            )
        else:
            return typing.cast(
                np.ndarray,
                coefficient_array
                * np.array(
                    [
                        +(1 - 1 / self.cop_h),
                        +1,
                        -(1 - 1 / self.cop_h),
                        -1,
                        -1,
                        -1,
                        +1,
                        +1,
                    ]
                ),
            )

    def _heat_pump_rhs(self, direction: bool = True) -> float:
        """Returns the right-hand side value for the heat pump equation.

        :param direction: bool
            The direction of the flow. True if the flow is positive, False otherwise.
            The direction defines the order of the connection points in the RHS of
            the heat pump equation.
        :return: float
        """
        if direction:
            connection_point_array = np.array([0, 1, 2, 3])
        else:
            connection_point_array = np.array([2, 3, 0, 1])
        return float(
            -self.prev_sol[IndexEnum.discharge + NUMBER_CORE_QUANTITIES * connection_point_array[0]]
            * self.prev_sol[
                IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * connection_point_array[0]
            ]
            + self.prev_sol[
                IndexEnum.discharge + NUMBER_CORE_QUANTITIES * connection_point_array[1]
            ]
            * self.prev_sol[
                IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * connection_point_array[1]
            ]
            + (1 - 1 / self.cop_h)
            * (
                self.prev_sol[
                    IndexEnum.discharge + NUMBER_CORE_QUANTITIES * connection_point_array[2]
                ]
                * self.prev_sol[
                    IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * connection_point_array[2]
                ]
                - self.prev_sol[
                    IndexEnum.discharge + NUMBER_CORE_QUANTITIES * connection_point_array[3]
                ]
                * self.prev_sol[
                    IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * connection_point_array[3]
                ]
            )
        )

    def add_heat_pump_energy_equation(self) -> EquationObject:
        r"""Returns an EquationObject of the energy balance equation for the HeatPump model.

        The equation is given by:

        .. math::

            \dot{m}_1 u_1 + \dot{m}_2 u_2 + \left( 1 + \frac{1}{\\mathrm{COP}_h} \right) \\
            \left[ \dot{m}_3 u_3 - \dot{m}_4 u_4 \right] = 0

        The coefficients depend on the flow direction, which is determined by the mass flow rate at
        connection point 0. If the mass flow rate at connection point 0 is greater than 0, the flow
        direction is positive; otherwise, the flow direction is negative.


        :param: None
        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side value of
            the equation.  
        """
        # Initialize the EquationObject
        equation_object = EquationObject()
        # Define indices for the equation
        equation_object.indices = (
            np.tile(
                np.array(
                    [
                        self.matrix_index + IndexEnum.discharge,
                        self.matrix_index + IndexEnum.internal_energy,
                    ]
                ),
                NUMBER_CORE_QUANTITIES + 1,
            )
            + np.repeat(range(NUMBER_CORE_QUANTITIES + 1), 2, axis=0) * NUMBER_CORE_QUANTITIES
        )

        # Check if the mass flow rate at connection point 0 is greater than 0
        # TODO: switch around 0
        if self._direction_boolean is True:  # self.prev_sol[IndexEnum.discharge] < 0:
            # Mass flow rate at connection point 0 is greater than 0; the flow direction is positive
            equation_object.coefficients = self._heat_pump_coefficients(direction=True)
            equation_object.rhs = self._heat_pump_rhs(direction=True)
        elif self._direction_boolean is False:  # self.prev_sol[IndexEnum.discharge] > 0:
            # Mass flow rate at connection point 0 is less than 0; the flow direction is negative
            equation_object.coefficients = self._heat_pump_coefficients(direction=False)
            equation_object.rhs = self._heat_pump_rhs(direction=False)
        else:
            # equation_object.indices = np.array([self.matrix_index + IndexEnum.discharge])
            # equation_object.coefficients = np.array([1])
            # equation_object.rhs = -1.0
            if self.supply_temperature_primary < self.supply_temperature_secondary:
                equation_object.indices = np.array(
                    [self.matrix_index + IndexEnum.discharge + NUMBER_CORE_QUANTITIES * 0]
                )
            else:
                equation_object.indices = np.array(
                    [self.matrix_index + IndexEnum.discharge + NUMBER_CORE_QUANTITIES * 2]
                )

            equation_object.coefficients = np.array([1])
            equation_object.rhs = -1.0
            # Mass flow rate at connection point 0 is greater than 0; the flow direction is positive
            # equation_object.coefficients = self._heat_pump_coefficients(direction=True)
            # equation_object.rhs = self._heat_pump_rhs(direction=True)
        return equation_object

    def update_loss_coefficient(self) -> None:
        """Basic function which does not do anything, but can be overwritten in derived classes."""

    def update_heat_supplied(self) -> None:
        """Basic function which does not do anything, but can be overwritten in derived classes."""
