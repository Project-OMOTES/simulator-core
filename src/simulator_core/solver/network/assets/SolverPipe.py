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
from simulator_core.solver.network.assets.Fall_type import FallType
import numpy as np
from scipy.optimize import root

from simulator_core.solver.matrix.core_enum import NUMBER_CORE_QUANTITIES, IndexEnum
from simulator_core.solver.network.assets.Fall_type import FallType
from simulator_core.solver.utils.fluid_properties import fluid_props
from simulator_core.entities.assets.asset_defaults import (PROPERTY_LENGTH, PROPERTY_DIAMETER,
                                                           PROPERTY_ROUGHNESS)


class SolverPipe(FallType):
    """Class to represent a pipe in a network."""

    def __init__(self, name: uuid.UUID,
                 number_of_unknowns: int = 6,
                 number_con_points: int = 2,
                 length: float = 1000,
                 diameter: float = 0.2,
                 roughness: float = 0.0001):
        """Constructor of pipe class.

        :param uuid.UUID name: The unique identifier of the pipe.
        :param int, optional number_of_unknowns: The number of unknown variables for the pipe.
        :param int, optional number_con_points: The number of connection points for the pipe.
        """
        super().__init__(name, number_of_unknowns, number_con_points)
        self.length: float = length
        self.diameter: float = diameter
        self.roughness: float = roughness
        self.area: float = np.pi * self.diameter**2 / 4
        self.lambda_loss: float = 0.01
        self.loss_coefficient: float = 0.0
        self.reynolds_number: float = 0.0
        self.alpha_value: float = 0.0
        self.ambient_temperature: float = 20 + 273.15

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
                raise ValueError(f"Property {expected_property} is not a valid property "
                                 f"of the pipe")
        self.area = np.pi * self.diameter ** 2 / 4

    def update_loss_coefficient(self) -> None:
        """Method to update the loss coefficient of the pipe."""
        self.area = np.pi * self.diameter**2 / 4
        self.calc_lambda_loss()
        self.loss_coefficient = (
            self.lambda_loss * self.length / (2 * self.diameter * self.area**2 * 9.81)
        )

    def calc_reynolds_number(
        self, mass_flow_rate: float, temperature: float = 20.0 + 273.15
    ) -> None:
        """Method to calculate the Reynolds number of the flow in the pipe.

        :param float mass_flow_rate: The mass flow rate of the fluid in the pipe.
        :param float, optional temperature: The temperature of the fluid in the pipe.
        """
        density = fluid_props.get_density(temperature)
        discharge = mass_flow_rate / density
        velocity = discharge / self.area
        self.reynolds_number = velocity * self.diameter / fluid_props.get_viscosity(temperature)

    def calc_lambda_loss(self) -> None:
        """Method to calculate the lambda loss of the pipe."""
        self.calc_reynolds_number(1000.0)
        if self.reynolds_number < 100:
            self.lambda_loss = 0.64
        elif self.reynolds_number < 2000:
            self.lambda_loss = 64 / self.reynolds_number
        else:
            part1 = self.roughness / self.diameter / 3.7
            lambda_star = 0.001
            while True:
                lambda_star_new = -2 * np.log10(part1 + 2.51 / (self.reynolds_number * lambda_star))
                if abs(lambda_star - lambda_star_new) < 0.0001:
                    break
                lambda_star = lambda_star_new
            self.lambda_loss = (1 / lambda_star) ** 2

    def _heat_supply_objective(self, internal_energy_x: float) -> float:
        """Objective function to minimize for the heat supply calculation.

        :param float internal_energy_x: The internal energy at the outlet of the pipe.
        :return: float
        """
        # Define properties
        pipe_area = self.length * np.pi * self.diameter
        mass_flow_rate = self.prev_sol[IndexEnum.discharge + NUMBER_CORE_QUANTITIES * 0]
        # - Internal energy at the inlet and outlet
        internal_energy_1 = self.prev_sol[IndexEnum.internal_energy + NUMBER_CORE_QUANTITIES * 0]
        # - Temperature at the outlet from internal_energy_x
        temperature_x = fluid_props.get_t(internal_energy_x)
        # Function to minimize
        return mass_flow_rate * (
            internal_energy_1 - internal_energy_x
        ) + self.alpha_value * pipe_area * (temperature_x - self.ambient_temperature)

    def update_heat_supplied(self) -> None:
        """Calculate the heat supplied by the pipe.

        The method calculates the heat supplied from the pipe to the fluid. The method assumes a
        constant heat transfer coefficient, and all
        The heat supplied is calculated using the following equation:


        Definition: positive if heat is supplied to the fluid, negative if heat is extracted from
         the fluid.

        """
        # Calculate the root of the objective function
        # Initial guess for the root is equal to the internal energy at the outlet
        x_guess = self.prev_sol[
            IndexEnum.internal_energy
            + (self.number_of_connection_point - 1) * NUMBER_CORE_QUANTITIES
        ]
        result = root(
            fun=self._heat_supply_objective,
            x0=x_guess,
            method="hybr",
        )
        # Return the internal energy at the outlet
        internal_energy_2 = result.x[0]
        # Calculate the heat loss
        self.heat_supplied = -1.0 * (
            self.alpha_value
            * self.length
            * np.pi
            * self.diameter
            * (fluid_props.get_t(internal_energy_2) - self.ambient_temperature)
        )
        # self.heat_supplied = 0.0
