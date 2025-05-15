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
"""Module for computing fluid properties."""

import numpy as np

from omotes_simulator_core.solver.utils.fluidprop import FluidProperties


class Interpolation:
    """Class to enable interpolation in a set of data points."""

    def __init__(self, x: list[float], y: list[float], order: int = 5, bounds: float = 0.1):
        """Constructor of the interpolation class.

        It stores the x and y data and determine the coefficients of a polynomial of the given
        order. This polynomial is used to interpolate the data.

        :param x: The x values of the data points.
        :param y: The y values of the data points.
        :param order: The order of the polynomial to use for the interpolation.
        :param bounds: The bounds on the x values used to check if the value is within bounds.
        """
        self.x = x
        self.y = y
        self.order = order
        self.bounds = bounds
        self.coefficients = np.polyfit(x, y, order)
        self._check_interpolation()

    def _check_interpolation(self) -> None:
        """Check if the interpolation gives acceptable results.

        For every data point the difference with the interpolated value is calculated.
        If this difference is more than 2% and value error is raised.
        """
        series_range = max(self.y) - min(self.y)
        error = [abs(y - self(x)) / series_range for x, y in zip(self.x, self.y)]
        if any(e > 0.02 and e != np.inf for e in error):
            raise ValueError("Interpolation error: error is more then 2%.")

    def __call__(self, value: float) -> float:
        """Returns the interpolated value at a given point.

        The calculate the value at the given point, the coefficients of the polynomial are used.
        A backwards loop is used, since the first value in the list is the one which is multiplied
        with the highest order. In this way we can first use 1, then multiply it with the value to
         get first order, then again multiply it with the value to get second order and so on.
         In this way we can step by step multiply the temp value with the
        value at the given point.

        :param value: The value to interpolate.
        :return: The interpolated value at the given point.
        """
        self._check_bounds(value=value)
        result = 0
        temp_value = 1.0
        for i in range(self.order, -1, -1):
            result += self.coefficients[i] * temp_value
            temp_value *= value
        return result

    def _check_bounds(self, value: float) -> None:
        """Check if the value is within the bounds of the data.

        The bounds check is within the set bounds default 10%, since we are fitting a curve
        on the data points. The result is that the curve can be a bit wider than the data points.
        """
        if value < self.x[0] * (1.0 - self.bounds) or value > self.x[-1] * (1.0 + self.bounds):
            raise ValueError("Value is out of bounds.")


class OmotesFluidProperties:
    """Class to represent the fluid properties.

    This class contains methods to get the internal energy, temperature, density,
    and viscosity of the fluid. THe data is loaded from a csv file in the same folder as this file.
    """

    T: list[float]
    """A list of floats that store the temperature of the fluid [K] per temperature."""

    cp: list[float]
    """A list of floats that store the heat capacity of the fluid [J/kg/K] per temperature."""

    rho: list[float]
    """A list of floats that store the density of the fluid [kg/m^3] per temperature."""

    visc: list[float]
    """A list of floats that store the viscosity of the fluid [Pa.s] per temperature."""

    therm_cond: list[float]
    """A list of floats that store the thermal conductivity of the fluid [W/m/K] per temperature."""

    IE: list[float]
    """A list of floats that store the internal energy of the fluid [J/kg] per temperature."""

    def __init__(
        self, p_ref: float = 20, fluid: str = "Water", T_min: int = 0, T_max: int = 150
    ) -> None:
        """Constructor of the fluid properties class.

        Initializes the class properties. Loads a list of the fluid property as function of the
        temperature using the fluidprop library. These are then used interpolation class objects.
        :param p_ref: The reference pressure of the fluid.
        :param fluid: The fluid to use for the fluid properties.
        :param T_min: The minimum temperature in Celsius to load the fluid properties for.
        :param T_max: The maximum temperature in Celsius to load the fluid properties for.
        """
        self.T = []
        self.cp = []
        self.rho = []
        self.visc = []
        self.therm_cond = []

        for t in range(T_min, T_max):
            self.T.append(t + 273.15)
            fluidprops = FluidProperties(fluid, t, p_ref)
            self.cp.append(float(fluidprops.Cp[0]))
            self.rho.append(float(fluidprops.rho[0]))
            self.visc.append(float(fluidprops.nu[0]))
            self.therm_cond.append(float(fluidprops.lambda_[0]))

        self.IE = [0.0]
        for i in range(1, len(self.T)):
            self.IE.append(
                self.IE[-1] + (self.cp[i - 1] + self.cp[i]) / 2 * (self.T[i] - self.T[i - 1])
            )

        # Create interpolation objects for the fluid properties
        self.ie_func = Interpolation(self.T, self.IE, 5)
        self.temp_func = Interpolation(self.IE, self.T, 5)
        self.density_func = Interpolation(self.T, self.rho, 5)
        self.visc_func = Interpolation(self.T, self.visc, 6)
        self.heat_cap_func = Interpolation(self.T, self.cp, 5)
        self.therm_cond_func = Interpolation(self.T, self.therm_cond, 5)

    def get_ie(self, t: float) -> float:
        """Returns the internal energy of the fluid at a given temperature.

        :param t: The temperature of the fluid.
        :return: The internal energy of the fluid at the given temperature.
        """
        return self.ie_func(t)

    def get_t(self, ie: float) -> float:
        """Returns the temperature of the fluid at a given internal energy.

        :param ie: The internal energy of the fluid.
        :return: The temperature of the fluid at the given internal energy.
        """
        return self.temp_func(ie)

    def get_density(self, t: float) -> float:
        """Returns the density of the fluid at a given temperature.

        :param t: The temperature of the fluid.
        :return: The density of the fluid at the given temperature.
        """
        return self.density_func(t)

    def get_viscosity(self, t: float) -> float:
        """Returns the viscosity of the fluid at a given temperature.

        :param t: The temperature of the fluid.
        :return: The viscosity of the fluid at the given temperature.
        """
        return self.visc_func(t)

    def get_heat_capacity(self, t: float) -> float:
        """Returns the heat capacity of the fluid at a given temperature.

        :param t: The temperature of the fluid.
        :return: The capacity of the fluid at the given temperature.
        """
        return self.heat_cap_func(t)

    def get_thermal_conductivity(self, t: float) -> float:
        """Returns the thermal conductivity of the fluid at a given temperature.

        :param t: The temperature of the fluid.
        :return: The thermal conductivity of the fluid at the given temperature.
        """
        return self.therm_cond_func(t)


fluid_props = OmotesFluidProperties()
