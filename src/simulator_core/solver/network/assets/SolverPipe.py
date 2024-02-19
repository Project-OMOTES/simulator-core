"""module containing pipe class"""
import uuid
from simulator_core.solver.network.assets.Fall_type import FallType
import numpy as np
from simulator_core.solver.utils.fluid_properties import fluid_props


class SolverPipe(FallType):
    """Class to represent a pipe in a network."""

    def __init__(self, name: uuid.UUID,
                 number_of_unknowns: int = 6,
                 number_con_points: int = 2):
        """Constructor of pipe class.

        :param uuid.UUID name: The unique identifier of the pipe.
        :param int, optional number_of_unknowns: The number of unknown variables for the pipe.
        :param int, optional number_con_points: The number of connection points for the pipe.
        """
        super().__init__(name, number_of_unknowns, number_con_points)
        self.length = 1000
        self.diam = 0.2
        self.roughness = 0.0001
        self.area = np.pi * self.diam ** 2 / 4
        self.lambda_loss = 0.01
        self.loss_coefficient = 0.0
        self.reynolds_number = 0.0

    def update_loss_coefficient(self):
        """Method to update the loss coefficient of the pipe."""
        self.area = np.pi * self.diam ** 2 / 4
        self.calc_lambda_loss()
        self.loss_coefficient = (self.lambda_loss * self.length /
                                 (2 * self.diam * self.area ** 2 * 9.81))

    def calc_reynolds_number(self, mass_flow_rate: float, temperature: float = 20.0) :
        """Method to calculate the Reynolds number of the flow in the pipe.

        :param float mass_flow_rate: The mass flow rate of the fluid in the pipe.
        :param float, optional temperature: The temperature of the fluid in the pipe.
        """
        density = fluid_props.get_density(temperature)
        discharge = mass_flow_rate / density
        velocity = discharge / self.area
        self.reynolds_number = (density * velocity * self.diam
                                / fluid_props.get_viscosity(temperature))

    def calc_lambda_loss(self):
        """Method to calculate the lambda loss of the pipe."""
        self.calc_reynolds_number(1000.0)
        if self.reynolds_number < 100:
            self.lambda_loss = 0.64
        elif self.reynolds_number < 2000:
            self.lambda_loss = 64 / self.reynolds_number
        else:
            part1 = self.roughness / self.diam / 3.7
            lambda_star = 0.001
            while True:
                lambda_star_new = -2 * np.log10(part1 + 2.51 / (self.reynolds_number * lambda_star))
                if abs(lambda_star - lambda_star_new) < 0.0001:
                    break
                lambda_star = lambda_star_new
            self.lambda_loss = (1 / lambda_star) ** 2
