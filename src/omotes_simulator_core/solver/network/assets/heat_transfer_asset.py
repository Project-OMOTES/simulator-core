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
import logging
from enum import Enum

import numpy as np

from omotes_simulator_core.solver.matrix.equation_object import EquationObject
from omotes_simulator_core.solver.matrix.index_core_quantity import index_core_quantity
from omotes_simulator_core.solver.network.assets.base_asset import BaseAsset
from omotes_simulator_core.solver.solver_constants import MASSFLOW_ZERO_LIMIT
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props

logger = logging.getLogger(__name__)


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
        temperature_out_primary: float = 293.15,
        mass_flow_initialization_primary: float = -20.0,
        heat_transfer_coefficient: float = 1.0,
        pre_scribe_mass_flow_secondary: bool = False,
        temperature_out_secondary: float = 293.15,
        mass_flow_rate_set_point_secondary: float = -80.0,
        pressure_set_point_secondary: float = 10000.0,
        pre_scribe_mass_flow_primary: bool = False,
    ):
        """
        Initializes the Heat Transfer Asset with the given parameters.

        Parameters
        ----------
        name : str
            The unique identifier of the asset.
        temperature_out_primary: float, optional
            The outlet temperature of the asset on the primary side (i.e., hot side).
            The default value is 293.15 K.
        mass_flow_initialization_primary : float, optional
            The mass flow rate set point for the asset on the primary side. Required
            to ensure that the correct sign is used for the equations. Value is
            neglected after initialization.
            The default is -20.0 kg/s.
        heat_transfer_coefficient : float, optional
            The heat transfer coefficient between the primary and secondary side.
            The default value is 1.0.
        temperature_out_secondary: float, optional
            The outlet temperature of the asset on the secondary side (i.e., cold side).
            The default value is 293.15 K.
        pre_scribe_mass_flow_secondary : bool
            A boolean flag that indicates whether the mass flow rate or the pressure is prescribed
            at the secondary side of the heat transfer asset.
        pre_scribe_mass_flow_primary : bool
            A boolean flag that indicates whether the mass flow rate or the pressure is prescribed
            at the primary side of the heat transfer asset.
        mass_flow_rate_set_point_secondary : float, optional
            The mass flow rate set point for the asset. The default is 10.0 kg/s.
        pressure_set_point_secondary : float, optional
            The pressure set point for the asset. The default is 10000.0 Pa.
        """
        super().__init__(
            name=name,
            _id=_id,
            number_of_unknowns=index_core_quantity.number_core_quantities * 4,
            number_connection_points=4,
        )
        # Define the outlet temperature of the asset on the cold side
        self.temperature_out_primary = temperature_out_primary
        # Define the outlet temperature of the asset on the hot side
        self.temperature_out_secondary = temperature_out_secondary
        # Define the heat transfer coefficient
        self.heat_transfer_coefficient = heat_transfer_coefficient
        # Define the initialization mass flow rate for the primary side
        self.mass_flow_initialization_primary = mass_flow_initialization_primary
        # Define the flag that indicates whether the mass flow rate or the pressure is prescribed
        # at the hot side of the heat pump
        self.pre_scribe_mass_flow_secondary = pre_scribe_mass_flow_secondary
        # Define the flag that indicates whether the mass flow rate or the pressure is prescribed
        # at the hot side of the heat pump
        self.pre_scribe_mass_flow_primary = pre_scribe_mass_flow_primary
        # Define the mass flow rate set point for the asset on the secondary side
        self.mass_flow_rate_rate_set_point_secondary = mass_flow_rate_set_point_secondary
        # Define the pressure set point for the asset
        self.pressure_set_point_secondary = pressure_set_point_secondary
        # Define flow directions
        self.flow_direction_primary = self.flow_direction(self.mass_flow_initialization_primary)
        self.iteration_flow_direction_primary = self.flow_direction_primary
        self.flow_direction_secondary = self.flow_direction(
            self.mass_flow_rate_rate_set_point_secondary
        )
        self.iteration_flow_direction_secondary = self.flow_direction_secondary

        # Define connection points
        (
            self.primary_side_inflow,
            self.primary_side_outflow,
            self.secondary_side_inflow,
            self.secondary_side_outflow,
        ) = self.get_ordered_connection_point_list()
        self.bypass_mode = False

    def flow_direction(self, mass_flow: float) -> FlowDirection:
        """Returns the flow direction of the heat transfer asset.

        Flow direction is determined for the given mass_flow:
        - If mass_flow > MASSFLOW_ZERO_LIMIT, the flow direction is negative.
        - If mass_flow < -MASSFLOW_ZERO_LIMIT, the flow direction is positive.
        - If mass_flow is within the limits, the flow direction is zero.

        :param float mass_flow: Mass flow rate at the selected connection point.
        :return: FlowDirection
            The flow direction of the heat transfer asset.
        """
        if mass_flow > MASSFLOW_ZERO_LIMIT:
            return FlowDirection.NEGATIVE
        elif mass_flow < -MASSFLOW_ZERO_LIMIT:
            return FlowDirection.POSITIVE
        else:
            return FlowDirection.ZERO

    def get_ordered_connection_point_list(self) -> list[int]:
        """Determine the order of connection points based on the flow direction.

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
            self.flow_direction_primary == FlowDirection.NEGATIVE
            and self.flow_direction_secondary == FlowDirection.POSITIVE
        ):
            return [1, 0, 2, 3]
        elif (
            self.flow_direction_primary == FlowDirection.POSITIVE
            and self.flow_direction_secondary == FlowDirection.POSITIVE
        ):
            return [0, 1, 2, 3]
        elif (
            self.flow_direction_primary == FlowDirection.POSITIVE
            and self.flow_direction_secondary == FlowDirection.NEGATIVE
        ):
            return [0, 1, 3, 2]
        elif (
            self.flow_direction_primary == FlowDirection.NEGATIVE
            and self.flow_direction_secondary == FlowDirection.NEGATIVE
        ):
            return [1, 0, 3, 2]
        elif (
            self.flow_direction_primary == FlowDirection.ZERO
            and self.flow_direction_secondary == FlowDirection.ZERO
        ):
            return [0, 1, 2, 3]
        elif (
            self.flow_direction_primary == FlowDirection.ZERO
            and self.flow_direction_secondary == FlowDirection.POSITIVE
        ):
            return [0, 1, 2, 3]
        elif (
            self.flow_direction_primary == FlowDirection.ZERO
            and self.flow_direction_secondary == FlowDirection.NEGATIVE
        ):
            return [0, 1, 3, 2]
        elif (
            self.flow_direction_primary == FlowDirection.POSITIVE
            and self.flow_direction_secondary == FlowDirection.ZERO
        ):
            return [0, 1, 2, 3]
        elif (
            self.flow_direction_primary == FlowDirection.NEGATIVE
            and self.flow_direction_secondary == FlowDirection.ZERO
        ):
            return [1, 0, 2, 3]
        else:
            return [0, 1, 2, 3]

    def get_equations(self) -> list[EquationObject]:
        r"""Returns the list of equations to be solved for the heat transfer asset."""
        if self.bypass_mode:
            return self.get_equations_bypass_mode()
        return self.get_equations_heat_transfer_mode()

    def get_equations_heat_transfer_mode(self) -> list[EquationObject]:
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
         the mass flow rate at the primary side of the heat transfer asset.

        .. math::

            \dot{m}_{asset} = 10.0

        :return: List[EquationObject]
        """
        # Check if there are four nodes connected to the asset
        if len(self.connected_nodes) != 4:
            raise ValueError("The number of connected nodes must be 4!")
        # Check if the number of unknowns is 12
        if self.number_of_unknowns != 12:
            raise ValueError("The number of unknowns must be 12!")
        # Set connection points based on the flow direction
        self.flow_direction_primary = self.flow_direction(self.prev_sol[0])
        self.flow_direction_secondary = self.flow_direction(self.prev_sol[6])
        (
            self.primary_side_inflow,
            self.primary_side_outflow,
            self.secondary_side_inflow,
            self.secondary_side_outflow,
        ) = self.get_ordered_connection_point_list()

        if np.all(np.abs(self.prev_sol[0:-1:3]) < MASSFLOW_ZERO_LIMIT):
            self.iteration_flow_direction_primary = self.flow_direction(
                self.prev_sol[
                    self.get_index_matrix(
                        property_name="mass_flow_rate",
                        connection_point=self.primary_side_inflow,
                        use_relative_indexing=True,
                    )
                ]
            )
            self.iteration_flow_direction_secondary = self.flow_direction(
                self.prev_sol[
                    self.get_index_matrix(
                        property_name="mass_flow_rate",
                        connection_point=self.secondary_side_inflow,
                        use_relative_indexing=True,
                    )
                ]
            )
        else:
            self.iteration_flow_direction_primary = self.flow_direction_primary
            self.iteration_flow_direction_secondary = self.flow_direction_secondary
        # Initialize the equations list
        equations = []

        # -- Internal energy (4x) --
        # Add the internal energy equations at connection points 0, and 2 to define
        # the connection with the nodes.
        equations.append(
            self.get_internal_energy_to_node_equation(connection_point=self.primary_side_inflow)
        )
        equations.append(
            self.get_internal_energy_to_node_equation(connection_point=self.secondary_side_inflow)
        )
        # Add the internal energy equations at connection points 1, and 3 to set
        # the temperature through internal energy at the outlet of the heat transfer asset.
        if self.iteration_flow_direction_primary != FlowDirection.ZERO:
            equations.append(
                self.prescribe_temperature_at_connection_point(
                    connection_point=self.primary_side_outflow,
                    supply_temperature=self.temperature_out_primary,
                )
            )
        else:
            equations.append(
                self.get_internal_energy_to_node_equation(
                    connection_point=self.primary_side_outflow
                )
            )
        if self.iteration_flow_direction_secondary != FlowDirection.ZERO:
            equations.append(
                self.prescribe_temperature_at_connection_point(
                    connection_point=self.secondary_side_outflow,
                    supply_temperature=self.temperature_out_secondary,
                )
            )
        else:
            equations.append(
                self.get_internal_energy_to_node_equation(
                    connection_point=self.secondary_side_outflow
                )
            )
        # -- Mass flow rate or pressure on secondary side (2x) --
        # Prescribe the pressure at the secondary side of the heat transfer asset.
        if self.pre_scribe_mass_flow_secondary:
            if self.iteration_flow_direction_secondary == FlowDirection.ZERO:
                mset = abs(self.mass_flow_rate_rate_set_point_secondary)
            else:
                mset = abs(
                    self.get_mass_flow_from_prev_solution()
                )  # abs(self.mass_flow_rate_rate_set_point_secondary)
            equations.append(
                self.prescribe_mass_flow_at_connection_point(
                    connection_point=2,
                    mass_flow_value=-1 * mset,
                )
            )
            equations.append(
                self.prescribe_mass_flow_at_connection_point(
                    connection_point=3,
                    mass_flow_value=mset,
                )
            )
        else:
            if self.iteration_flow_direction_secondary == FlowDirection.ZERO:
                pset_out = self.pressure_set_point_secondary
                pset_in = self.pressure_set_point_secondary
            else:
                if self.iteration_flow_direction_secondary == FlowDirection.POSITIVE:
                    pset_out = self.pressure_set_point_secondary / 2
                    pset_in = self.pressure_set_point_secondary
                else:
                    pset_out = self.pressure_set_point_secondary
                    pset_in = self.pressure_set_point_secondary / 2
            equations.append(
                self.prescribe_pressure_at_connection_point(
                    connection_point=self.secondary_side_inflow,
                    pressure_value=pset_in,
                )
            )
            equations.append(
                self.prescribe_pressure_at_connection_point(
                    connection_point=self.secondary_side_outflow,
                    pressure_value=pset_out,
                )
            )
        # -- Pressure (4x) --
        # Connect the pressure at the nodes to the asset
        for connection_point in [
            self.primary_side_inflow,
            self.primary_side_outflow,
            self.secondary_side_inflow,
            self.secondary_side_outflow,
        ]:
            equations.append(self.get_press_to_node_equation(connection_point=connection_point))

        # -- Internal continuity (1x) --
        # Add the internal continuity equation at the primary side.

        # -- Energy balance equation for the heat transfer asset (1x) --
        # Defines the energy balance between the primary and secondary side of the
        # heat transfer asset.
        # If the mass flow at the inflow node of the primary and secondary side is not zero,
        if self.pre_scribe_mass_flow_primary:
            equations.append(
                self.prescribe_mass_flow_at_connection_point(
                    connection_point=0,
                    mass_flow_value=-1 * abs(self.mass_flow_initialization_primary),
                )
            )
            equations.append(
                self.prescribe_mass_flow_at_connection_point(
                    connection_point=1,
                    mass_flow_value=abs(self.mass_flow_initialization_primary),
                )
            )
        else:
            if self.iteration_flow_direction_primary == FlowDirection.ZERO:
                pset_out = self.pressure_set_point_secondary
                pset_in = self.pressure_set_point_secondary
            else:
                if self.iteration_flow_direction_primary == FlowDirection.POSITIVE:
                    pset_out = self.pressure_set_point_secondary / 2
                    pset_in = self.pressure_set_point_secondary
                else:
                    pset_out = self.pressure_set_point_secondary
                    pset_in = self.pressure_set_point_secondary / 2
            equations.append(
                self.prescribe_pressure_at_connection_point(
                    connection_point=self.primary_side_inflow,
                    pressure_value=pset_in,
                )
            )
            equations.append(
                self.prescribe_pressure_at_connection_point(
                    connection_point=self.primary_side_outflow,
                    pressure_value=pset_out,
                )
            )
        # Return the equations
        return equations

    def get_equations_bypass_mode(self) -> list[EquationObject]:
        r"""Return the heat transfer equations for bypass mode.

        The method returns the heat transfer equations for the heat transfer asset in bypass mode.

        The internal energy at the connection points with mass inflow are linked to the nodes.

        .. math::

                u_{connection_point} = u_{node}

        The temperature is prescribed through coupling the inflow connection poitn from primary
        side to the outflow connection point of the secondary side, and vice versa.

        The mass flow rate or pressure is prescribed at the secondary and primary side of the
        heat transfer asset.
        :return: List[EquationObject]
        """
        equations = []
        # pressure to node equations
        for connection_point in range(4):
            equations.append(self.get_press_to_node_equation(connection_point=connection_point))

        # Internal energy to node equations
        self.set_internal_energy_equations_bypass(equations)

        # set mass flow rate or pressure
        if self.pre_scribe_mass_flow_secondary:
            mset = self.mass_flow_rate_rate_set_point_secondary
            equations.append(
                self.prescribe_mass_flow_at_connection_point(
                    connection_point=2,
                    mass_flow_value=mset,
                )
            )
            equations.append(
                self.prescribe_mass_flow_at_connection_point(
                    connection_point=3,
                    mass_flow_value=-mset,
                )
            )
        else:
            if self.iteration_flow_direction_secondary == FlowDirection.ZERO:
                pset_out = self.pressure_set_point_secondary
                pset_in = self.pressure_set_point_secondary
            else:
                if self.iteration_flow_direction_secondary == FlowDirection.POSITIVE:
                    pset_out = self.pressure_set_point_secondary / 2
                    pset_in = self.pressure_set_point_secondary
                else:
                    pset_out = self.pressure_set_point_secondary
                    pset_in = self.pressure_set_point_secondary / 2
            equations.append(
                self.prescribe_pressure_at_connection_point(
                    connection_point=2,
                    pressure_value=pset_in,
                )
            )
            equations.append(
                self.prescribe_pressure_at_connection_point(
                    connection_point=3,
                    pressure_value=pset_out,
                )
            )
        # set mass flow rate or pressure
        if self.pre_scribe_mass_flow_primary:
            mset = self.mass_flow_initialization_primary
            equations.append(
                self.prescribe_mass_flow_at_connection_point(
                    connection_point=0,
                    mass_flow_value=mset,
                )
            )
            equations.append(
                self.prescribe_mass_flow_at_connection_point(
                    connection_point=1,
                    mass_flow_value=-1 * mset,
                )
            )
        else:
            if self.iteration_flow_direction_secondary == FlowDirection.ZERO:
                pset_out = self.pressure_set_point_secondary
                pset_in = self.pressure_set_point_secondary
            else:
                if self.iteration_flow_direction_secondary == FlowDirection.POSITIVE:
                    pset_out = self.pressure_set_point_secondary / 2
                    pset_in = self.pressure_set_point_secondary
                else:
                    pset_out = self.pressure_set_point_secondary
                    pset_in = self.pressure_set_point_secondary / 2
            equations.append(
                self.prescribe_pressure_at_connection_point(
                    connection_point=0,
                    pressure_value=pset_in,
                )
            )
            equations.append(
                self.prescribe_pressure_at_connection_point(
                    connection_point=1,
                    pressure_value=pset_out,
                )
            )
        return equations

    def set_internal_energy_equations_bypass(self, equations: list[EquationObject]) -> None:
        r"""Sets the internal energy equations.

        In bypass mode the internal energy of connecting point 0 and 3 are set equal to the node.
        This assumes inflow from does connection points into the heat transfer asset. Furthermore,
        since the heat transfer asset is in bypass mode the secondary outflow is set equal to
        the primary inflow, and vice versa.
        """
        equations.append(self.get_internal_energy_to_node_equation(connection_point=1))
        equations.append(self.get_internal_energy_to_node_equation(connection_point=3))
        equations.append(self.short_cut_internal_energy(con_point1=0, con_point2=3))
        equations.append(self.short_cut_internal_energy(con_point1=1, con_point2=2))

    def short_cut_internal_energy(self, con_point1: int, con_point2: int) -> EquationObject:
        """Return an equation object which set the internal energy equal between both connections"""
        equation_object = EquationObject()
        # Short-circuiting the primary and secondary side of the heat transfer asset.
        equation_object.indices = np.array(
            [
                self.get_index_matrix(
                    property_name="internal_energy",
                    connection_point=con_point1,
                    use_relative_indexing=False,
                ),
                self.get_index_matrix(
                    property_name="internal_energy",
                    connection_point=con_point2,
                    use_relative_indexing=False,
                ),
            ]
        )
        equation_object.coefficients = np.array([1.0, -1.0])
        equation_object.rhs = 0.0
        return equation_object

    def get_mass_flow_from_prev_solution(self) -> float:
        r"""Determine the mass flow rate from the previous solution.

        Method uses the following equation to determine the mass flow rate:

        .. math::
            \dot{m}_{primary_inflow} =
            - \left|\frac{c \left( \dot{m}_{secondary, inflow}u_{secondary, inflow} -
            \dot{m}_{secondary, outflow}u_{secondary, outflow} \right)}
            {u_{primary, inflow} - u_{primary, outflow}}
            \right|

        with :math:`c` as the heat transfer coefficient.

        :return: float, :math:`\dot{m}_{primary, inflow}`

        """
        internal_energy_difference_primary = (
            self.prev_sol[
                self.get_index_matrix(
                    property_name="internal_energy",
                    connection_point=self.primary_side_inflow,
                    use_relative_indexing=True,
                )
            ]
            - self.prev_sol[
                self.get_index_matrix(
                    property_name="internal_energy",
                    connection_point=self.primary_side_outflow,
                    use_relative_indexing=True,
                )
            ]
        )
        # Define the energy on the secondary side
        energy_secondary_side = self.heat_transfer_coefficient * (
            self.prev_sol[
                self.get_index_matrix(
                    property_name="mass_flow_rate",
                    connection_point=self.secondary_side_inflow,
                    use_relative_indexing=True,
                )
            ]
            * self.prev_sol[
                self.get_index_matrix(
                    property_name="internal_energy",
                    connection_point=self.secondary_side_inflow,
                    use_relative_indexing=True,
                )
            ]
            + self.prev_sol[
                self.get_index_matrix(
                    property_name="mass_flow_rate",
                    connection_point=self.secondary_side_outflow,
                    use_relative_indexing=True,
                )
            ]
            * self.prev_sol[
                self.get_index_matrix(
                    property_name="internal_energy",
                    connection_point=self.secondary_side_outflow,
                    use_relative_indexing=True,
                )
            ]
        )
        if (internal_energy_difference_primary == 0) | (energy_secondary_side == 0):
            return float(
                self.prev_sol[
                    self.get_index_matrix(
                        property_name="mass_flow_rate",
                        connection_point=self.primary_side_inflow,
                        use_relative_indexing=True,
                    )
                ]
            )
        return float(-1 * abs(-energy_secondary_side / internal_energy_difference_primary))

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
                self.get_index_matrix(
                    property_name="internal_energy",
                    connection_point=connection_point,
                    use_relative_indexing=False,
                )
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
            [
                self.get_index_matrix(
                    property_name="mass_flow_rate",
                    connection_point=connection_point,
                    use_relative_indexing=False,
                )
            ]
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
            [
                self.get_index_matrix(
                    property_name="pressure",
                    connection_point=connection_point,
                    use_relative_indexing=False,
                )
            ]
        )
        equation_object.coefficients = np.array([1.0])
        equation_object.rhs = pressure_value
        return equation_object

    def get_heat_power_primary(self) -> float:
        """Calculate the heat power on the primary side of the heat transfer asset.

        The heat power is calculated as the product of the mass flow rate and the internal energy
        difference between the inlet and outlet of the primary side.

        :return: float
            The heat power on the primary side of the heat transfer asset.
        """
        return float(
            self.prev_sol[
                self.get_index_matrix(
                    property_name="mass_flow_rate",
                    connection_point=self.primary_side_inflow,
                    use_relative_indexing=True,
                )
            ]
            * (
                self.prev_sol[
                    self.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=self.primary_side_outflow,
                        use_relative_indexing=True,
                    )
                ]
                - self.prev_sol[
                    self.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=self.primary_side_inflow,
                        use_relative_indexing=True,
                    )
                ]
            )
        )

    def get_heat_power_secondary(self) -> float:
        """Calculate the heat power on the secondary side of the heat transfer asset.

        The heat power is calculated as the product of the mass flow rate and the internal energy
        difference between the inlet and outlet of the secondary side.

        :return: float
            The heat power on the secondary side of the heat transfer asset.
        """
        return float(
            self.prev_sol[
                self.get_index_matrix(
                    property_name="mass_flow_rate",
                    connection_point=self.secondary_side_inflow,
                    use_relative_indexing=True,
                )
            ]
            * (
                self.prev_sol[
                    self.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=self.secondary_side_outflow,
                        use_relative_indexing=True,
                    )
                ]
                - self.prev_sol[
                    self.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=self.secondary_side_inflow,
                        use_relative_indexing=True,
                    )
                ]
            )
        )

    def get_electric_power_consumption(self) -> float:
        """Calculate the electric power consumption of the heat transfer asset.

        The electric power consumption is calculated as the absolute difference between the
        heat power on the primary and secondary side.

        :return: float
            The electric power consumption of the heat transfer asset.
        """
        return abs(abs(self.get_heat_power_primary()) - abs(self.get_heat_power_secondary()))
