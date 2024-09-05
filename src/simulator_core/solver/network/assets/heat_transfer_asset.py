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

"""Module containing a Heat Transfer asset."""
import typing
from enum import Enum
from typing import List, Optional

import numpy as np

from simulator_core.solver.matrix.core_enum import NUMBER_CORE_QUANTITIES, IndexEnum
from simulator_core.solver.matrix.equation_object import EquationObject
from simulator_core.solver.network.assets.base_asset import BaseAsset
from simulator_core.solver.utils.fluid_properties import fluid_props


class FlowDirection(Enum):
    """Enum class to define the flow direction of the heat transfer asset."""

    POSITIVE = 1
    NEGATIVE = -1
    ZERO = 0


class HeatTransferAsset(BaseAsset):
    """Matrix object for the heat transfer asset."""

    def __init__(
        self,
        name: str,
        _id: str,
        primary_side: Optional[List[int]] = None,
        supply_temperature_primary: float = 293.15,
        mass_flow_rate_set_point_primary: float = -20.0,
        heat_transfer_coefficient: float = 1.0,
        pre_scribe_mass_flow_secondary: bool = False,
        supply_temperature_secondary: float = 293.15,
        mass_flow_rate_set_point_secondary: float = 80.0,
        pressure_set_point_secondary: float = 10000.0,
        primary_side_inflow: int = 0,
        primary_side_outflow: int = 1,
        secondary_side_inflow: int = 2,
        secondary_side_outflow: int = 3,
    ):
        """
        Initializes the Heat Transfer Asset with the given parameters.

        Parameters
        ----------
        name : str
            The unique identifier of the asset.
        supply_temperature_primary: float, optional
            The supply temperature of the asset on the primary side (i.e., hot side).
            The default value is 293.15 K.
        mass_flow_rate_set_point_primary: float, optional
            The mass flow rate set point for the asset on the primary side.
            The default is -20.0 kg/s.
        heat_transfer_coefficient : float, optional
            The heat transfer coefficient between the primary and secondary side.
            The default value is 1.0.
        supply_temperature_secondary: float, optional
            The supply temperature of the asset on the secondary side (i.e., cold side).
            The default value is 293.15 K.
        pre_scribe_mass_flow_secondary : bool
            A boolean flag that indicates whether the mass flow rate or the pressure is prescribed
            at the secondary side of the heat transfer asset.
        mass_flow_rate_set_point_secondary : float, optional
            The mass flow rate set point for the asset. The default is 10.0 kg/s.
        pressure_set_point_secondary : float, optional
            The pressure set point for the asset. The default is 10000.0 Pa.
        primary_side : List[int], optional
            The connection points on the primary side of the heat transfer asset.
            The default is [0, 1].
        """
        super().__init__(
            name=name,
            _id=_id,
            number_of_unknowns=NUMBER_CORE_QUANTITIES * 4,
            number_connection_points=4,
        )
        # Define the supply temperature of the asset on the cold side
        self.supply_temperature_primary = supply_temperature_primary
        # Define the supply temperature of the asset on the hot side
        self.supply_temperature_secondary = supply_temperature_secondary
        # Define the heat transfer coefficient
        self.heat_transfer_coefficient = heat_transfer_coefficient
        # Define the flag that indicates whether the mass flow rate or the pressure is prescribed
        # at the hot side of the heat pump
        self.pre_scribe_mass_flow_secondary = pre_scribe_mass_flow_secondary
        # Define the mass flow rate set point for the asset on the secondary side
        self.mass_flow_rate_set_point_secondary = mass_flow_rate_set_point_secondary
        # Define the mass flow rate set point for the asset on the primary side
        self.mass_flow_rate_set_point_primary = mass_flow_rate_set_point_primary
        # Define the pressure set point for the asset
        self.pressure_set_point_secondary = pressure_set_point_secondary
        # Define the primary side of the heat transfer asset
        if primary_side is None:
            primary_side = [0, 1]
        self.primary_side = primary_side
        # Define the secondary side of the heat transfer asset
        self.secondary_side = list(set(range(4)).difference(set(primary_side)))
        # Define the connection points
        self.primary_side_inflow = primary_side_inflow
        self.primary_side_outflow = primary_side_outflow
        self.secondary_side_inflow = secondary_side_inflow
        self.secondary_side_outflow = secondary_side_outflow

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
        # Define the equations
        equations = self.get_equations_from_connection_point_list()
        return equations

    def flow_direction(self, connection_point: int) -> FlowDirection:
        """Returns the flow direction of the heat transfer asset.

        The flow direction is positive when the mass flow rate at the selected connection point is
         positive.

        :param int connection_point: The index of the connection point.
        :return: FlowDirection
            The flow direction of the heat transfer asset.
        """
        if self.prev_sol[IndexEnum.discharge + connection_point * NUMBER_CORE_QUANTITIES] > 0:
            return FlowDirection.POSITIVE
        elif self.prev_sol[IndexEnum.discharge + connection_point * NUMBER_CORE_QUANTITIES] < 0:
            return FlowDirection.NEGATIVE
        else:
            return FlowDirection.ZERO

    def get_connection_point_list(
        self, flow_direction_primary: FlowDirection, flow_direction_secondary: FlowDirection
    ) -> List[int]:
        """Determine the list of connection points based on the flow direction.

        The method returns the connection points based on the flow direction of the primary and
        secondary side of the heat transfer asset.

        If the flow direction of the primary and secondary side is positive, the connection points
        are [0, 1, 2, 3].

        If the flow direction of the primary side is positive and the flow direction of the
        secondary side is negative, the connection points are [0, 1, 3, 2].

        If the flow direction of the primary side is negative and the flow direction of the
        secondary side is positive, the connection points are [1, 0, 2, 3].

        If the flow direction of the primary and secondary side is negative, the connection points
        are [1, 0, 3, 2].

        If the flow direction of the primary or secondary side is zero, the connection points are
        [0, 1, 2, 3].

        :param flow_direction_primary: FlowDirection
            The flow direction of the primary side of the heat transfer asset.
        :param flow_direction_secondary: FlowDirection
            The flow direction of the secondary side of the heat transfer asset.
        :return: List[int]
            List of connection points as [primary_side_inflow, primary_side_outflow,
            secondary_side_inflow, secondary_side_outflow].
        """
        # Determine the connection points based on the flow direction
        if (
            flow_direction_primary == FlowDirection.NEGATIVE
            and flow_direction_secondary == FlowDirection.POSITIVE
        ):
            return [0, 1, 2, 3]
        elif (
            flow_direction_primary == FlowDirection.POSITIVE
            and flow_direction_secondary == FlowDirection.POSITIVE
        ):
            return [1, 0, 2, 3]
        elif (
            flow_direction_primary == FlowDirection.POSITIVE
            and flow_direction_secondary == FlowDirection.NEGATIVE
        ):
            return [1, 0, 3, 2]
        elif (
            flow_direction_primary == FlowDirection.NEGATIVE
            and flow_direction_secondary == FlowDirection.NEGATIVE
        ):
            return [0, 1, 3, 2]
        else:
            return [
                self.primary_side_inflow,
                self.primary_side_outflow,
                self.secondary_side_inflow,
                self.secondary_side_outflow,
            ]

    def get_equations_from_connection_point_list(self) -> List[EquationObject]:
        r"""Return the heat transfer equations.

        The method returns the heat transfer equations for the heat transfer asset.

        The internal energy at the connection points with mass inflow are linked to the nodes.

        .. math::

                u_{connection_point} = u_{node}

        The temperature is prescribed through the internal energy at the outlet on the
        primary and secondary side of the heat transfer asset.

        .. math::

            u_{connection_point} = u_{supply_temperature}

        The mass flow rate or pressure is prescribed at the secondary side of the heat transfer
        asset.

        On the primary side, continuity of mass flow rate is enforced.

        .. math::

            \dot{m}_{0} + \dot{m}_{1} = 0

        If the mass flow at the inflow node of the primary and secondary side is not zero, we
         prescribe the follwoing energy balance equation for the heat transfer asset:

        .. math::

            \dot{m}_0 \left{ u_0 - u_1 \right} + C \left{ u_2 \dot{m}_2 + u_3 \dot{m}_3 \right} = 0

        If the mass flow at the inflow node of the primary and secondary side is zero, we prescribe
         we prescribe the mass flow rate at the primary side of the heat transfer asset.

        .. math::

            \dot{m}_{asset} = 10.0

        :return: List[EquationObject]
        """
        # Initialize the equations list
        equations = []
        # Determine the flow direction of the primary and secondary side
        flow_direction_primary = self.flow_direction(connection_point=self.primary_side[0])
        flow_direction_secondary = self.flow_direction(connection_point=self.secondary_side[1])
        # Determine the connection points based on the flow direction
        primary_side_inflow, primary_side_outflow, secondary_side_inflow, secondary_side_outflow = (
            self.get_connection_point_list(
                flow_direction_primary=flow_direction_primary,
                flow_direction_secondary=flow_direction_secondary,
            )
        )
        # -- Internal energy (4x) --
        # Add the internal energy equations at connection points 0, and 2 to define
        # the connection with the nodes.
        equations.append(
            self.add_internal_energy_to_node_equation(connection_point=primary_side_inflow)
        )
        equations.append(
            self.add_internal_energy_to_node_equation(connection_point=secondary_side_inflow)
        )
        # Add the internal energy equations at connection points 1, and 3 to set
        # the temperature through internal energy at the outlet of the heat transfer asset.
        equations.append(
            self.prescribe_temperature_at_connection_point(
                connection_point=primary_side_outflow,
                supply_temperature=self.supply_temperature_primary,
            )
        )
        equations.append(
            self.prescribe_temperature_at_connection_point(
                connection_point=secondary_side_outflow,
                supply_temperature=self.supply_temperature_secondary,
            )
        )
        # -- Mass flow rate or pressure on secnodary side (2x) --
        # Prescribe the pressure at the secondary side of the heat transfer asset.
        if self.pre_scribe_mass_flow_secondary:
            equations.append(
                self.prescribe_mass_flow_at_connection_point(
                    connection_point=secondary_side_inflow,
                    mass_flow_value=-self.mass_flow_rate_set_point_secondary,
                )
            )
            equations.append(
                self.prescribe_mass_flow_at_connection_point(
                    connection_point=secondary_side_outflow,
                    mass_flow_value=+self.mass_flow_rate_set_point_secondary,
                )
            )
        else:
            equations.append(
                self.prescribe_pressure_at_connection_point(
                    connection_point=secondary_side_inflow,
                    pressure_value=self.pressure_set_point_secondary / 2,
                )
            )
            equations.append(
                self.prescribe_pressure_at_connection_point(
                    connection_point=secondary_side_outflow,
                    pressure_value=self.pressure_set_point_secondary / 1,
                )
            )
        # -- Pressure (4x) --
        # Connect the pressure at the nodes to the asset
        equations.append(self.add_press_to_node_equation(connection_point=primary_side_inflow))
        equations.append(self.add_press_to_node_equation(connection_point=primary_side_outflow))
        equations.append(self.add_press_to_node_equation(connection_point=secondary_side_inflow))
        equations.append(self.add_press_to_node_equation(connection_point=secondary_side_outflow))
        # -- Internal continuity (2x) --
        # Add the internal continuity equation at the primary side.
        equations.append(
            self.add_continuity_equation(
                connection_point_1=primary_side_inflow, connection_point_2=primary_side_outflow
            )
        )
        # -- Energy balance equation for the heat transfer asset (1x) --
        # Defines the energy balance between the primary and secondary side of the
        # heat transfer asset.
        # If the mass flow at the inflow node of the primary and secondary side is not zero,
        if (flow_direction_primary != FlowDirection.ZERO) or (
            flow_direction_secondary != FlowDirection.ZERO
        ):
            # equations.append(
            #     self.add_heat_transfer_equation(
            #         primary_side_inflow=primary_side_inflow,
            #         primary_side_outflow=primary_side_outflow,
            #         secondary_side_inflow=secondary_side_inflow,
            #         secondary_side_outflow=secondary_side_outflow,
            #     )
            # )
            equations.append(
                self.prescribe_mass_flow_at_connection_point(
                    connection_point=primary_side_inflow,
                    mass_flow_value=self.get_mass_flow_setpoint_from_prev_solution(),
                )
            )
        # If the mass flow at the inflow node of the primary and secondary side is zero,
        else:
            # TODO: Fix when mass flow rate is zero.
            # TODO: Fix when controller prescribes mass flow rate is zero.
            equations.append(
                self.prescribe_mass_flow_at_connection_point(
                    connection_point=primary_side_inflow,
                    mass_flow_value=self.mass_flow_rate_set_point_primary,
                )
            )
        # Return the equations
        return equations

    def get_mass_flow_setpoint_from_prev_solution(self) -> float:
        internal_energy_difference_primary = (
            self.prev_sol[
                IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * self.primary_side_inflow
            ]
            - self.prev_sol[
                IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * self.primary_side_outflow
            ]
        )
        # Define the energy on the secondary side
        energy_secondary_side = self.heat_transfer_coefficient * (
            self.prev_sol[IndexEnum.discharge + NUMBER_CORE_QUANTITIES * self.secondary_side_inflow]
            * self.prev_sol[
                IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * self.secondary_side_inflow
            ]
            + self.prev_sol[
                IndexEnum.discharge + NUMBER_CORE_QUANTITIES * self.secondary_side_outflow
            ]
            * self.prev_sol[
                IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * self.secondary_side_outflow
            ]
        )
        return float(-1 * abs(-energy_secondary_side / internal_energy_difference_primary))

    def add_mass_flow_to_node_equation(self, connection_point: int) -> EquationObject:
        r"""Links the mass flow rate at the connection point to the node.

        .. math::

            \dot{m}_{asset} - \dot{m}_{node} = 0

        :param int connection_point: The index of the connection point.
        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side value
            of the equation.
        """
        # Add the equations
        equation_object = EquationObject()
        equation_object.indices = np.array(
            [
                self.matrix_index + IndexEnum.discharge + connection_point * NUMBER_CORE_QUANTITIES,
                self.connected_nodes[connection_point].matrix_index + IndexEnum.discharge,
            ]
        )
        equation_object.coefficients = np.array([1, -1])
        equation_object.rhs = 0.0
        return equation_object

    def add_continuity_equation(
        self, connection_point_1: int, connection_point_2: int
    ) -> EquationObject:
        r"""Returns an EquationObject that represents the continuity equation for the asset.

        The continuity equation is given by:

        .. math::

            \dot{m}_1 + \dot{m}_2 = 0

        where :math:`\dot{m}_1` is the mass flow rate at 'connection_point_1', and
        :math:`\dot{m}_2` is the mass flow rate at 'connection_point_2'.

        :param int connection_point_1: The index of the first connection point.
        :param int connection_point_2: The index of the second connection point.
        :return: EquationObject
            An EquationObject that contains the indices, coefficients, and right-hand side value of
            the equation.
        """
        # Add the equations
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

    def prescribe_temperature_at_connection_point(
        self, connection_point: int, supply_temperature: float
    ) -> EquationObject:
        """Prescribe the temperature at a connection point via the internal energy.

        .. math::

            u_{connection_point} = u_{supply_temperature}

        :param connection_point: The index of the connection point to add the equation for.
        :type connection_point: int
        :param supply_temperature: The prescribed temperature at the connection point.
        :type supply_temperature: float
        :return: An equation object representing the prescribed temperature equation.
        :rtype: EquationObject
        """
        # Create the equation object
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

    def prescribe_mass_flow_at_connection_point(
        self, connection_point: int, mass_flow_value: float
    ) -> EquationObject:
        """Prescribe the mass flow rate at the selected connection point.

        The returned equation object represents the prescribed mass flow rate or pressure equation
        for the asset at the given connection point.

        :param int connection_point: The connection point for which to add the equation.
        :param float mass_flow_value: The prescribed mass flow rate at the connection point.
        :return: EquationObject
        """
        # Add the equations
        equation_object = EquationObject()
        equation_object.indices = np.array(
            [self.matrix_index + IndexEnum.discharge + connection_point * NUMBER_CORE_QUANTITIES]
        )
        equation_object.coefficients = np.array([1])
        equation_object.rhs = mass_flow_value
        return equation_object

    def prescribe_pressure_at_connection_point(
        self, connection_point: int, pressure_value: float
    ) -> EquationObject:
        """Prescribe the pressure at the selected connection point.

        .. math::

            P_{connection_point} = P_{set_point}

        :param int connection_point: The connection point for which to add the equation.
        :param float pressure_value: The prescribed pressure at the connection point.
        :return: EquationObject
        """
        # Add the equations
        equation_object = EquationObject()
        equation_object.indices = np.array(
            [self.matrix_index + IndexEnum.pressure + connection_point * NUMBER_CORE_QUANTITIES]
        )
        equation_object.coefficients = np.array([1.0])
        equation_object.rhs = pressure_value
        return equation_object

    def get_heat_transfer_equation_coefficients(
        self, connection_point_list: List[int]
    ) -> np.ndarray:
        r"""Determine the coefficients of the heat transfer equation.

        The heat transfer coefficients are given by:

        .. math::

            \frac{\partial F}{\partial \vec{x}}  & = \left[ u_0 - u_1, \dot{m}_0, \\\\
            & 0, -\dot{m}_0, \\\\
            & +C u_2, +C \dot{m}_2, \\\\
            & +C u_3, +C \dot{m}_3 \right]

        with :math:'\vec{x}' as :math:\sum_0^3 \left[\dot{m}_0, u_0\right].

        :param connection_point_list: List of connection points as
            [primary_side_inflow, primary_side_outflow,
            secondary_side_inflow, secondary_side_outflow]
        :return: np.ndarray
            The coefficients for the heat pump equation.
        """
        # Determine coefficients
        coefficient_array = np.array(
            [
                [
                    self.prev_sol[
                        IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * connection_point
                    ],
                    self.prev_sol[IndexEnum.discharge + NUMBER_CORE_QUANTITIES * connection_point],
                ]
                for connection_point in connection_point_list
            ]
        )
        # Reshape array to a 1D array of size (8,)
        coefficient_array = coefficient_array.reshape((8,))
        # Multiply the coefficients with the heat transfer coefficient
        temp_array = coefficient_array * np.array(
            [
                +1,
                +1,
                +0,
                +0,
                +self.heat_transfer_coefficient,
                +self.heat_transfer_coefficient,
                +self.heat_transfer_coefficient,
                +self.heat_transfer_coefficient,
            ]
        )
        temp_array[3] = -temp_array[1]
        temp_array[0] = temp_array[0] - coefficient_array[2]
        return typing.cast(
            np.ndarray,
            temp_array,
        )

    def get_heat_transfer_equation_rhs(self, connection_point_list: List[int]) -> float:
        r"""RHS for the heat transfer equation.

        The right-hand side of the heat transfer equation is given by:

        .. math::

            \mathrm{RHS} = \dot{m}_0 \left( u_0 - u_1 \right) + \\\\
            C \left( u_2 \dot{m}_2 + u_3 \dot{m}_3 \right)

        :param connection_point_list: The list of connection points to determine the
            right-hand side
        :return: float
            The right-hand side value of the heat transfer
        """
        # Define the energy on the primary side
        energy_primary_side = self.prev_sol[
            IndexEnum.discharge + NUMBER_CORE_QUANTITIES * connection_point_list[0]
        ] * (
            self.prev_sol[
                IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * connection_point_list[0]
            ]
            - self.prev_sol[
                IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * connection_point_list[1]
            ]
        )
        # Define the energy on the secondary side
        energy_secondary_side = self.heat_transfer_coefficient * (
            self.prev_sol[IndexEnum.discharge + NUMBER_CORE_QUANTITIES * connection_point_list[2]]
            * self.prev_sol[
                IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * connection_point_list[2]
            ]
            + self.prev_sol[IndexEnum.discharge + NUMBER_CORE_QUANTITIES * connection_point_list[3]]
            * self.prev_sol[
                IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * connection_point_list[3]
            ]
        )
        # Return the sum of the energy on the primary and secondary side
        return float(energy_primary_side + energy_secondary_side)

    def add_heat_transfer_equation(
        self,
        primary_side_inflow: int,
        primary_side_outflow: int,
        secondary_side_inflow: int,
        secondary_side_outflow: int,
    ) -> EquationObject:
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
        # Create a connection point list
        connection_point_list = [
            primary_side_inflow,
            primary_side_outflow,
            secondary_side_inflow,
            secondary_side_outflow,
        ]
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
            + np.repeat(connection_point_list, 2, axis=0) * NUMBER_CORE_QUANTITIES
        )
        index_sort = np.argsort(equation_object.indices)
        equation_object.indices = equation_object.indices[index_sort]
        # Define the coefficients for the equation
        coefficients = self.get_heat_transfer_equation_coefficients(
            connection_point_list=connection_point_list
        )
        equation_object.coefficients = coefficients[index_sort]
        # Define the right-hand side value for the equation
        equation_object.rhs = self.get_heat_transfer_equation_rhs(
            connection_point_list=connection_point_list
        )

        return equation_object

    def update_loss_coefficient(self) -> None:
        """Basic function which does not do anything, but can be overwritten in derived classes."""

    def update_heat_supplied(self) -> None:
        """Basic function which does not do anything, but can be overwritten in derived classes."""
