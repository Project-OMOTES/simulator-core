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
"""module containing pipe class."""

import uuid
from typing import Dict

import numpy as np
from scipy.optimize import root

from simulator_core.entities.assets.asset_defaults import (
    DEFAULT_MISSING_VALUE,
    PROPERTY_DIAMETER,
    PROPERTY_LENGTH,
    PROPERTY_ROUGHNESS,
)
from simulator_core.solver.matrix.core_enum import NUMBER_CORE_QUANTITIES, IndexEnum
from simulator_core.solver.network.assets.fall_type import FallType
from simulator_core.solver.utils.fluid_properties import fluid_props


class SolverPipe(FallType):
    """Class to represent a pipe in a network."""

    lambda_loss: float = 0.01
    """ The dimensionless lambda loss value for the pipe. """

    loss_coefficient: float = 0.0
    r""" The loss coefficient of the pipe equal to .. math:: \frac{\lambda L}{2D A^2 g} """

    reynolds_number: float = 0.0
    r""" The Reynolds number of the flow in the pipe .. math:: \frac{v D}{\nu}  """

    alpha_value: float = 0.0
    """ The heat transfer coefficient of the pipe with units [W/m^2/K] """

    ambient_temperature: float = 293.15
    """ The ambient temperature of the pipe with units [K] """

    _grid_size: int = 10
    """ The number of grid points in the internal grid of the pipe. """

    def __init__(
        self,
        name: uuid.UUID,
        length: float = 1000.0,
        diameter: float = 0.2,
        roughness: float = 0.001,
    ):
        """Constructor of pipe class.

        :param uuid.UUID name: The unique identifier of the pipe.
        :param float length: The length of the pip [m] with a default value of 1000.0 m.
        :param float diameter: The diameter of the pipe [m] with a default value of 0.2 m.
        :param float roughness: The roughness of the pipe [m] with a default value of 1E-3 m.
        """
        super().__init__(
            name=name, number_of_unknowns=NUMBER_CORE_QUANTITIES * 2, number_con_points=2
        )
        # Set the physical properties of the pipe
        self.length: float = length
        self.diameter: float = diameter
        self.roughness: float = roughness
        # Calculate the area of the pipe
        self.area: float = np.pi * self.diameter**2 / 4
        # Create internal grid
        self._internal_energy_grid = np.zeros((self._grid_size + 1, 1))

    def set_physical_properties(self, physical_properties: Dict[str, float]) -> None:
        """Method to set the physical properties of the pipe.

        :param physical_properties: dictionary containing the physical properties of the pipe.
        expected properties are: length [m], diameter [m], roughness [m]
        """
        expected_properties = [PROPERTY_LENGTH, PROPERTY_DIAMETER, PROPERTY_ROUGHNESS]

        for expected_property in expected_properties:
            if expected_property not in physical_properties:
                raise ValueError(f"Property {expected_property} is missing in physical_properties")
            if hasattr(self, expected_property):
                setattr(self, expected_property, physical_properties[expected_property])
            else:
                raise ValueError(
                    f"Property {expected_property} is not a valid property " f"of the pipe"
                )
        # Update the area of the pipe
        self.area = np.pi * self.diameter**2 / 4

    def update_loss_coefficient(self) -> None:
        """Method to update the loss coefficient of the pipe."""
        self.area = np.pi * self.diameter**2 / 4
        self.calc_lambda_loss()
        self.loss_coefficient = (
            self.lambda_loss * self.length / (2 * self.diameter * self.area**2 * 9.81)
        )

    # TODO: Do we want to implement a dependency on the connection point?
    def calculate_reynolds_number(
        self,
        mass_flow_rate: float = DEFAULT_MISSING_VALUE,
        temperature: float = DEFAULT_MISSING_VALUE,
    ) -> float:
        """Method to calculate the Reynolds number of the flow in the pipe."""
        # Retrieve properties from previous solution
        if mass_flow_rate == DEFAULT_MISSING_VALUE:
            mass_flow_rate = self.prev_sol[IndexEnum.discharge]
        if temperature == DEFAULT_MISSING_VALUE:
            temperature = fluid_props.get_t(self.prev_sol[IndexEnum.internal_energy])
        # Calculate the Reynolds number
        density = fluid_props.get_density(temperature)
        discharge = mass_flow_rate / density
        velocity = discharge / self.area
        return velocity * self.diameter / fluid_props.get_viscosity(temperature)

    def calc_lambda_loss(self) -> None:
        r"""Method to calculate the lambda loss of the pipe.

        For Reynolds numbers lower than 100:
            .. math:: \lambda = 0.64

        For Reynolds numbers between 100 and 2000:
            .. math:: \lambda = \frac{64}{Re}

        For Reynolds numbers higher than 2000 use the Colebrook-White equation:
            .. math::

                \frac{1}{\lambda} = -2 \log \left( \frac{\varepsilon}{D} +
                \frac{2.51}{Re \lambda} \right)
        """
        # Update the Reynolds number
        self.reynolds_number = self.calculate_reynolds_number()
        # Determine the loss
        if self.reynolds_number < 100:
            self.lambda_loss = 0.64
        elif self.reynolds_number < 2000:
            self.lambda_loss = 64 / self.reynolds_number
        elif self.reynolds_number < 4000:
            # Interpolate between f calculated with Reynolds = 2000.0 and f calculated with
            # Reynolds = 4000
            f_lower = 64.0 / 2000.0
            f_upper = self._colebrook_white(reynolds_number=4000.0)
            self.lambda_loss = f_lower + ((f_upper - f_lower) / 2000.0) * (
                self.reynolds_number - 2000.0
            )
        else:
            self.lambda_loss = self._colebrook_white()

    def _colebrook_white_objective(self, lambda_guess: float) -> float:
        """Root function for the Colebrook-White equation.

        :param float lambda_val: The friction factor.
        :return: float, the friction factor.
        """
        # Calculate the friction factor using the Colebrook-White equation
        return float(
            -2
            * np.log10(
                (2.51 / (self.reynolds_number * np.sqrt(lambda_guess)))
                + (self.roughness / (3.71 * self.diameter))
            )
            - 1.0 / np.sqrt(lambda_guess)
        )

    def _colebrook_white(
        self,
        lambda_guess: float = 0.001,
        convergence_limit: float = 1e-4,
        reynolds_number: float = DEFAULT_MISSING_VALUE,
    ) -> float:
        r"""Method to iteratively calculate the Colebrook-White friction factor.

        :param float lambda_guess: The initial guess for the 1/\sqrt{friction factor}.
        :param float convergence_limit: The convergence limit for the iterative calculation.
        :param float reynolds_number: The Reynolds number of the flow in the pipe.
        :return: float, the friction factor.
        """
        if reynolds_number == DEFAULT_MISSING_VALUE:
            reynolds_number = self.reynolds_number
        # Iterative calculation
        return float(
            root(
                self._colebrook_white_objective, lambda_guess, method="hybr", tol=convergence_limit
            ).x[0]
        )

    def _calculate_graetz_number(
        self, temperature: float, mass_flow_rate: float = DEFAULT_MISSING_VALUE
    ) -> float:
        """Calculate the Graetz number of the flow in the pipe."""
        # Calculate the thermal diffusivity
        thermal_diffusivity = fluid_props.get_thermal_conductivity(temperature) / (
            fluid_props.get_density(temperature) * fluid_props.get_heat_capacity(temperature)
        )
        # Calculate the velocity of the fluid
        if mass_flow_rate == DEFAULT_MISSING_VALUE:
            mass_flow_rate = self.prev_sol[IndexEnum.discharge]
        density = fluid_props.get_density(temperature)
        velocity = (mass_flow_rate / density) * (1 / self.area)
        # Check velocity
        if abs(velocity) >= 1e-6:
            return thermal_diffusivity * (1 / (self.diameter * velocity))
        else:
            # Return a large number so that the heat transfer coefficient is very low
            return 10.0

    def _calculate_heat_transfer_coefficient_fluid(
        self, temperature: float, mass_flow_rate: float
    ) -> float:
        """Calculate the heat transfer coefficient of the fluid."""
        # Calculate the thermal diffusivity
        thermal_diffusivity = fluid_props.get_thermal_conductivity(temperature) / (
            fluid_props.get_density(temperature) * fluid_props.get_heat_capacity(temperature)
        )
        # Calculate the Reynolds number
        reynolds_number = self.calculate_reynolds_number(
            mass_flow_rate=mass_flow_rate, temperature=temperature
        )
        # Determine the Nusselt number
        if reynolds_number < 1e4:
            # Laminar flow assumptions
            graetz_number = self._calculate_graetz_number(
                temperature=temperature, mass_flow_rate=mass_flow_rate
            )
            if graetz_number >= 0.1:
                nusselt_number = 3.66
            else:
                nusselt_number = 1.62 * graetz_number ** (-1 / 3)
        else:
            praendtl_number = fluid_props.get_viscosity(temperature) / thermal_diffusivity
            nusselt_number = 0.023 * reynolds_number**0.8 * praendtl_number**0.33
        # Calculate the heat transfer coefficient
        return nusselt_number * fluid_props.get_thermal_conductivity(temperature) / self.diameter

    def _determine_flow_direction(self) -> tuple[float, int, int, int]:
        """Determine the flow direction of the pipe."""
        # Reset the internal energy grid
        self._internal_energy_grid = np.zeros((self._grid_size + 1, 1))
        # Determine the flow direction
        if self.prev_sol[IndexEnum.discharge] < 0:
            # Flow from connection point 1 to connection point 0
            start_index = self._grid_size - 1
            end_index = -1
            step = -1
            # Set the internal energy at the connection point
            self._internal_energy_grid[-1] = self.prev_sol[
                IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES
            ]
            # Retrieve the mass flow rate
            mass_flow_rate = abs(self.prev_sol[IndexEnum.discharge])
        elif self.prev_sol[IndexEnum.discharge] > 0:
            # Flow from connection point 0 to connection point 1
            start_index = 1
            end_index = self._grid_size + 1
            step = 1
            # Set the internal energy at the connection point
            self._internal_energy_grid[0] = self.prev_sol[IndexEnum.internal_energy]
            # Retrieve the mass flow rate
            mass_flow_rate = self.prev_sol[IndexEnum.discharge]
        else:
            # No flow
            start_index = 1
            end_index = 0
            step = 1
            # Set the internal energy grid
            self._internal_energy_grid[: self._grid_size] = fluid_props.get_ie(
                self.ambient_temperature
            )
            # Retrieve the mass flow rate
            mass_flow_rate = self.prev_sol[IndexEnum.discharge]
        return mass_flow_rate, start_index, end_index, step

    def _calculate_heat_loss_grid_point(self, iteration_index: int) -> float:
        """Calculate the heat loss over a grid point."""
        # Retrieve the internal energy
        internal_energy_current = self._internal_energy_grid[iteration_index]
        # Retrieve the temperature of the fluid
        temperature_current = fluid_props.get_t(internal_energy_current)
        # Calculate the heat loss
        return -(
            self.alpha_value
            * np.pi
            * self.diameter
            * self.length
            / self._grid_size
            * (temperature_current - self.ambient_temperature)
        )

    def _internal_energy_steady_state_objective(
        self,
        internal_energy_iteration: float,
        internal_energy: float,
        mass_flow_rate: float,
        use_fluid_capacity: bool,
    ) -> float:
        """Root function for the internal energy steady state equation.

        :param float internal_energy_guess: The internal energy guess.
        :return: float, the internal energy.
        """
        # Calculate the temperature of the fluid
        temperature = fluid_props.get_t(internal_energy_iteration)

        if use_fluid_capacity:
            # Determine the heat transfer coefficient including fluid properties
            heat_transfer_coefficient_fluid = self._calculate_heat_transfer_coefficient_fluid(
                temperature=temperature,
                mass_flow_rate=mass_flow_rate,
            )
            if self.alpha_value > 0.0:
                total_heat_transfer_coefficient = 1 / (
                    1 / heat_transfer_coefficient_fluid + 1 / self.alpha_value
                )
            else:
                total_heat_transfer_coefficient = heat_transfer_coefficient_fluid
        else:
            total_heat_transfer_coefficient = self.alpha_value

        # Return the objective function
        element_size = self.length / self._grid_size
        objective = mass_flow_rate * (
            internal_energy - internal_energy_iteration
        ) - total_heat_transfer_coefficient * np.pi * self.diameter * element_size * (
            temperature - self.ambient_temperature
        )
        return float(objective)

    def _update_internal_energy_grid(self) -> float:
        # Retrieve the flow direction
        mass_flow_rate, start_index, end_index, step = self._determine_flow_direction()
        use_fluid_capacity = True
        heat_supplied = 0.0
        # Update the internal energy grid
        for iteration_index in np.arange(start_index, end_index, step):
            # Retrieve the previous value of the internal energy
            previous_internal_energy = self._internal_energy_grid[iteration_index - step]
            # Use root finding to determine the internal energy at the current grid point
            internal_energy_iteration = root(
                self._internal_energy_steady_state_objective,
                previous_internal_energy,
                args=(previous_internal_energy, mass_flow_rate, use_fluid_capacity),
                method="hybr",
                tol=1e-6,
            ).x[0]
            # Update the internal energy grid
            self._internal_energy_grid[iteration_index] = internal_energy_iteration
            # Calculate the loss over the grid cell
            heat_loss_grid_cell = self._calculate_heat_loss_grid_point(
                iteration_index=iteration_index
            )
            # Update the heat supplied
            heat_supplied += heat_loss_grid_cell
        return heat_supplied

    def update_heat_supplied(self) -> None:
        """Calculate the heat supplied by the pipe.

        Definition: positive if heat is supplied to the fluid, negative if heat is extracted from
        the fluid.

        """
        # Update the internal energy grid
        self.heat_supplied = self._update_internal_energy_grid()
