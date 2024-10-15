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
"""This module contains the fluid properties class."""

import numpy as np
from fluidprop import FluidProperties


class Interpolation:
    """Class to enable interpolation in a set of data points."""

    def __init__(self, x: list[float], y: list[float], order: int = 5):
        """Constructor of the interpolation class.

        It stores the x and y data and determine the coefficients of a polynomial of the given
        order. This polynomial is used to interpolate the data. Please note that no checks on
        the bounds have been included.

        :param x: The x values of the data points.
        :param y: The y values of the data points.
        :param order: The order of the polynomial to use for the interpolation.
        """
        self.x = x
        self.y = y
        self.order = order
        self.coefficients = np.polyfit(x, y, order)
        self._check_interpolation()

    def _check_interpolation(self) -> None:
        """Check if the interpolation gives acceptable results.

        For every data point the difference with the interpolated value is calculated.
        If this difference is more than 2% and value error is raised.
        """
        for i in range(len(self.x)):
            if self.y[i] == 0:
                continue
            error = abs(self.y[i] - self(self.x[i])) / self.y[i]
            if error == np.inf:
                continue
            if error > 0.02:
                raise ValueError("Interpolation error: error is more then 2%.")

    def __call__(self, value: float) -> float:
        """Returns the interpolated value at a given point.

        The calculate the value at the given point, the coefficients of the polynomial are used.
        A backwards loop is used, since the first value in the list is the one which is multiplied
        with the highest order. In this way we can step by step multiply the temp value with the
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

        The bounds check is set 10% wider, since we are fitting a curve on the data points.
        The result is that the curve can be a bit wider than the data points.
        """
        if value < self.x[0] * 0.9 or value > self.x[-1] * 1.1:
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

    def __init__(self) -> None:
        """Constructor of the fluid properties class.

        Initializes the class properties. Loads a list of the fluid property as function of the
        temperature using the fluidprop library. These are then used interpolation class objects.

        """
        self.T = []
        self.cp = []
        self.rho = []
        self.visc = []
        self.therm_cond = []
        p_ref = 20.00  # Reference pressure [barg]
        fluid = "Water"  # fluid to be used

        for t in range(150):
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
