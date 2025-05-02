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

import numpy as np
from scipy.optimize import root

from omotes_simulator_core.entities.assets.asset_defaults import (
    DEFAULT_MISSING_VALUE,
    PROPERTY_ALPHA_VALUE,
    PROPERTY_DIAMETER,
    PROPERTY_LENGTH,
    PROPERTY_ROUGHNESS,
)
from omotes_simulator_core.solver.network.assets.fall_type import FallType
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


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

    _use_fluid_capacity: bool = False
    """ A boolean to determine if the fluid capacity is used in the heat transfer calculation. """

    def __init__(
        self,
        name: str,
        _id: str,
        length: float = 1000.0,
        diameter: float = 0.2,
        roughness: float = 0.001,
    ):
        """Constructor of pipe class.

        :param str name: The name of the pipe.
        :param str _id: The unique identifier of the pipe.
        :param float length: The length of the pip [m] with a default value of 1000.0 m.
        :param float diameter: The diameter of the pipe [m] with a default value of 0.2 m.
        :param float roughness: The roughness of the pipe [m] with a default value of 1E-3 m.
        """
        super().__init__(name=name, _id=_id)
        # Set the physical properties of the pipe
        self.length: float = length
        self.diameter: float = diameter
        self.roughness: float = roughness
        # Calculate the area of the pipe
        self.area: float = np.pi * self.diameter**2 / 4

    def set_physical_properties(self, physical_properties: dict[str, float]) -> None:
        """Method to set the physical properties of the pipe.

        :param physical_properties: dictionary containing the physical properties of the pipe.
        expected properties are: length [m], diameter [m], roughness [m]
        """
        expected_properties = [
            PROPERTY_LENGTH,
            PROPERTY_DIAMETER,
            PROPERTY_ROUGHNESS,
            PROPERTY_ALPHA_VALUE,
        ]

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
        r"""Method to update the loss coefficient of the pipe.

        The loss coefficient is calculated using the following equation:

        .. math:: \lambda \frac{L}{D} \frac{1}{2} \frac{1}{\rho A^2}

        using the mass flow rate to velocity conversion:

        .. math:: v = \frac{\dot{m}}{\rho A}

        with the density of the fluid defined at the first connection point.
        """
        self.calc_lambda_loss()
        density = fluid_props.get_density(
            fluid_props.get_t(
                self.prev_sol[
                    self.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=0,
                        use_relative_indexing=True,
                    )
                ]
            )
        )
        self.loss_coefficient = (
            self.lambda_loss
            * (self.length / self.diameter)
            * (1 / 2)
            * (1 / (self.area**2 * density))
        )

    # TODO: Do we want to implement a dependency on the connection point?
    def calculate_reynolds_number(
        self,
        mass_flow_rate: float = DEFAULT_MISSING_VALUE,
        temperature: float = DEFAULT_MISSING_VALUE,
    ) -> float:
        r"""Method to calculate the Reynolds number of the flow in the pipe.

        The Reynolds number is calculated using the following equation:

        .. math:: \frac{v D}{\nu}

        with the fluid properties defined in the fluid properties module. If
        the mass flow rate and temperature are not provided, the mass flow rate
        and temperature at the first connection point from the previous solution
        are used.

        :param float mass_flow_rate: The mass flow rate of the fluid (kg/s).
        :param float temperature: The temperature of the fluid (K).
        """
        # Retrieve properties from previous solution
        if mass_flow_rate == DEFAULT_MISSING_VALUE:
            mass_flow_rate = self.prev_sol[
                self.get_index_matrix(
                    property_name="mass_flow_rate", connection_point=0, use_relative_indexing=True
                )
            ]
        if temperature == DEFAULT_MISSING_VALUE:
            temperature = fluid_props.get_t(
                self.prev_sol[
                    self.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=0,
                        use_relative_indexing=True,
                    )
                ]
            )
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

        For Reynolds numbers higher than 2000 use the Tkachenko and Mileikovsky (2020) correlation:
            .. math::

                f = \left( \frac{8.128943 + A_1}{8.128943 A_0 - 0.86859209 A_1 \ln \left(
                        \frac{A_1}{3.7099535 Re} \right)} \right)^2

        with the following coefficients:

            .. math::

                    A_0 = -0.79638 \ln \left( \frac{\frac{\epsilon}{D}}{8.208}
                        + \frac{7.3357}{Re} \right)

                    A_1 = Re \left( \frac{\epsilon}{D} \right) + 9.3120665 A_0

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
            f_upper = self._calculate_explicit_friction_factor(
                reynolds_number=4000.0
            )  # self._colebrook_white(reynolds_number=4000.0)
            self.lambda_loss = f_lower + ((f_upper - f_lower) / 2000.0) * (
                self.reynolds_number - 2000.0
            )
        else:
            self.lambda_loss = self._calculate_explicit_friction_factor()  # self._colebrook_white()

    def _calculate_explicit_friction_factor(self, reynolds_number: float | None = None) -> float:
        r"""Method to calculate the explicit friction factor of the pipe.

        The explicit friction factor is calculated with the Tkaenko and Mileikovsky (2020)
        correlation:

        .. math::

            f = \left( \frac{8.128943 + A_1}{8.128943 A_0 - 0.86859209 A_1 \ln \left(
                    \frac{A_1}{3.7099535 Re} \right)} \right)^2

        with the following coefficients:

        .. math::

                A_0 = -0.79638 \ln \left( \frac{\frac{\epsilon}{D}}{8.208}
                    + \frac{7.3357}{Re} \right)

                A_1 = Re \left( \frac{\epsilon}{D} \right) + 9.3120665 A_0


        :param float reynolds_number: The Reynolds number of the flow in the pipe.
        :return: float, the friction factor.
        """
        # Check existence of Reynolds number
        if reynolds_number is None:
            reynolds_number = self.reynolds_number
        # Calculate the coefficients
        A0 = -0.79638 * np.log((self.roughness / self.diameter) / 8.208 + 7.3357 / reynolds_number)
        A1 = reynolds_number * (self.roughness / self.diameter) + 9.3120665 * A0

        # Calculate the friction factor
        return float(
            (
                (8.128943 + A1)
                / (8.128943 * A0 - 0.86859209 * A1 * np.log(A1 / (3.7099535 * reynolds_number)))
            )
            ** 2
        )

    def _colebrook_white_objective(self, lambda_guess: float) -> float:
        r"""Root function for the Colebrook-White equation.

        Solves the following optimization objective:

        .. math::

            - 2 \log \left( \frac{\epsilon}{D 3.71} +   \frac{2.51}{Re \sqrt{\lambda}}
            \right) - \frac{1}{\sqrt{\lambda}} = 0

        :param float lambda_val: The friction factor.
        :return: float, the friction factor.
        """
        # Calculate the friction factor using the Colebrook-White equation
        return float(
            (
                -2
                * np.log10(
                    (2.51 / (self.reynolds_number * np.sqrt(lambda_guess)))
                    + (self.roughness / (3.7 * self.diameter))
                )
                - 1.0 / np.sqrt(lambda_guess)
            ).item()
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
        r"""Calculate the Graetz number of the flow in the pipe.

        If the mass flow rate is not provided, the mass flow rate from the previous solution is
         used.

        The Graetz number is calculated using the following equation:

        .. math:: \text{Gz} = \frac{\alpha A}{D v}

        If the velocity is zero, a large number is returned to indicate a low heat
        transfer coefficient.

        :param float temperature: The temperature of the fluid.
        :param float mass_flow_rate: The mass flow rate of the fluid.
        :return: float, the Graetz number.
        """
        # Calculate the Reynolds number
        reynolds_number = self.calculate_reynolds_number(
            mass_flow_rate=mass_flow_rate, temperature=temperature
        )

        # Calculate the Prandtl number
        prandtl_number = self.calculate_prandtl_number(temperature=temperature)

        # Check velocity
        if abs(reynolds_number) >= 1e-6:
            return self.diameter / self.length * reynolds_number * prandtl_number
        else:
            # Return a large number so that the heat transfer coefficient is very low
            return 10.0

    def calculate_prandtl_number(self, temperature: float = DEFAULT_MISSING_VALUE) -> float:
        r"""Calculate the Prandtl number of the fluid.

        The Prandtl number is calculated using the following equation:

        .. math:: \text{Pr} = \frac{\mu}{\alpha}

        with the dynamic viscosity and thermal diffusivity of the fluid. The thermal diffusivity is
        calculated as:

        .. math:: \alpha = \frac{k}{\rho c_p}

        which is the ratio of the dynamic viscosity to the thermal diffusivity of the fluid.

        :param float temperature: The temperature of the fluid.
        :return: float, the Prandtl number.
        """
        # Check the temperature
        if temperature == DEFAULT_MISSING_VALUE:
            temperature = fluid_props.get_t(
                self.prev_sol[
                    self.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=0,
                        use_relative_indexing=True,
                    )
                ]
            )

        # Calculate the thermal diffusivity
        thermal_diffusivity = fluid_props.get_thermal_conductivity(temperature) / (
            fluid_props.get_density(temperature) * fluid_props.get_heat_capacity(temperature)
        )
        # Calculate the Prandtl number
        return fluid_props.get_viscosity(temperature) / thermal_diffusivity

    def _calculate_heat_transfer_coefficient_fluid(
        self, temperature: float, mass_flow_rate: float
    ) -> float:
        r"""Calculate the heat transfer coefficient of the fluid.

        The heat transfer coefficient is calculated using the Nusselt number and the thermal
        conductivity of the fluid.

        If the Reynolds number is less than 1e4, the Nusselt number is calculated using the
        Graetz number. For a Graetz number greater than 0.1, the Nusselt number is set to 3.66.
        For a Graetz number less than 0.1, the Nusselt number is calculated using the following
        equation:

        .. math:: Nu = 1.62 \cdot \text{Gz}^{-1/3}

        Otherwise, the Nusselt number is calculated using the Reynolds number and

        .. math:: Nu = 0.023 \cdot \text{Re}^{0.8} \cdot \text{Pr}^{0.33}

        where Pr is the Prandtl number of the fluid as:

        .. math:: \text{Pr} = \frac{\mu}{\alpha}

        The heat transfer coefficient is then calculated using the following equation:

        .. math:: \alpha = Nu \cdot k / D

        Source: R. Mudde, 'Fysische transportverschijnselen', 1998 p. 133 - p.134

        :param float temperature: The temperature of the fluid.
        :param float mass_flow_rate: The mass flow rate of the fluid.
        """
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
            # TODO: Discuss Graetz is defined for (1/Gz) < 0.05 and (1/Gz) > 0.1
            if (1 / graetz_number) >= 0.1:
                nusselt_number = 3.66
            else:
                nusselt_number = 1.62 * graetz_number ** (-1 / 3)
        else:
            prandtl_number = self.calculate_prandtl_number(temperature=temperature)
            nusselt_number = 0.023 * reynolds_number**0.8 * prandtl_number**0.33
        # Calculate the heat transfer coefficient
        return nusselt_number * fluid_props.get_thermal_conductivity(temperature) / self.diameter

    def _determine_inflow_temperature(self) -> tuple[float, float]:
        """Determine the inflow temperature and mass flow rate of the pipe.

        The inflow temperature is determined by looking at the flow direction in the pipe
        """
        mass_flow_rate = self.prev_sol[
            self.get_index_matrix(
                property_name="mass_flow_rate", connection_point=0, use_relative_indexing=True
            )
        ]
        # Determine the flow direction
        if mass_flow_rate < 0:
            # Flow from connection point 1 to connection point 0
            tin = fluid_props.get_t(
                self.prev_sol[
                    self.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=1,
                        use_relative_indexing=True,
                    )
                ]
            )
            mass_flow_rate = abs(mass_flow_rate)
        elif mass_flow_rate > 0:
            # Flow from connection point 0 to connection point 1
            tin = fluid_props.get_t(
                self.prev_sol[
                    self.get_index_matrix(
                        property_name="internal_energy",
                        connection_point=0,
                        use_relative_indexing=True,
                    )
                ]
            )
        else:
            # No flow
            tin = self.ambient_temperature
        return tin, float(mass_flow_rate)

    def _calculate_total_heat_transfer_coefficient(
        self, temperature: float, mass_flow_rate: float
    ) -> float:
        r"""Calculate the total heat transfer coefficient of the pipe.

        The total heat transfer coefficient is calculated using the following equation:

        .. math::

            \frac{1}{\alpha} = \frac{1}{\alpha_{\text{fluid}}} +
            \frac{1}{\alpha_{\text{wall}}}

        where the heat transfer coefficient of the fluid is calculated using the
        '_calculate_heat_transfer_coefficient_fluid' method and the heat transfer coefficient of the
        wall is the alpha value of the pipe.

        :param float temperature: The temperature of the fluid.
        :param float mass_flow_rate: The mass flow rate of the fluid.
        :return: float, the total heat transfer coefficient.
        """
        if self._use_fluid_capacity:
            # Determine the heat transfer coefficient including fluid properties
            heat_transfer_coefficient_fluid = self._calculate_heat_transfer_coefficient_fluid(
                temperature=temperature,
                mass_flow_rate=mass_flow_rate,
            )
            if self.alpha_value > 0.0:
                return 1 / (1 / heat_transfer_coefficient_fluid + 1 / self.alpha_value)
            else:
                return heat_transfer_coefficient_fluid
        else:
            return self.alpha_value

    def _calculate_total_heat_loss(self, tin: float, mass_flow_rate: float) -> float:
        r"""Calculate the total heat loss of the pipe.

        The heat loss is calculated with the following formula:
        .. math::

        \dot{m} c_p \left(T_{in} - T_{out}\right) \left(1 -
        \exp{\frac{-\alpha \pi D L}{\dot{m} c_p}})\right

        :param float tin: The temperature of the fluid at the inlet of the pipe.
        :param float mass_flow_rate: The mass flow rate of the fluid in the pipe.
        :return: float, the total heat loss of the pipe.
        """
        if mass_flow_rate == 0:
            return 0.0
        cp = fluid_props.get_heat_capacity(tin)
        heat_loss = (
            mass_flow_rate
            * cp
            * (tin - self.ambient_temperature)
            * (
                1
                - np.exp(
                    -self.alpha_value * np.pi * self.diameter * self.length / (mass_flow_rate * cp)
                )
            )
        )
        return float(heat_loss)

    def update_heat_supplied(self) -> None:
        """Calculate the heat supplied by the pipe.

        Definition: positive if heat is supplied to the fluid, negative if heat is extracted from
        the fluid.

        """
        tin, mass_flow_rate = self._determine_inflow_temperature()

        self._calculate_total_heat_transfer_coefficient(
            temperature=tin, mass_flow_rate=mass_flow_rate
        )
        self.heat_supplied = -self._calculate_total_heat_loss(
            tin=tin, mass_flow_rate=mass_flow_rate
        )
