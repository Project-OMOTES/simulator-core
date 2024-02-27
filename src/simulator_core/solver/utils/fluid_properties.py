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
import csv
from pathlib import Path

import numpy as np


class FluidProperties:
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

        Initializes the class properties and loads the fluid properties from a csv file.
        """
        file = Path(__file__).parent / "temp_props.csv"
        self.T = []
        self.cp = []
        self.rho = []
        self.visc = []
        self.therm_cond = []
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            for row in csv_reader:
                self.T.append(float(row[0]))
                self.cp.append(float(row[1]))
                self.rho.append(float(row[2]))
                self.visc.append(float(row[3]))
                self.therm_cond.append(float(row[4]))

        self.IE = [0.0]
        for i in range(1, len(self.T)):
            self.IE.append(
                self.IE[-1] + (self.cp[i - 1] + self.cp[i]) / 2 * (self.T[i] - self.T[i - 1])
            )

    def get_ie(self, t: float) -> float:
        """Returns the internal energy of the fluid at a given temperature.

        :param t: The temperature of the fluid.
        :return: The internal energy of the fluid at the given temperature.
        """
        return float(np.interp(np.array([t]), self.T, self.IE).item())

    def get_t(self, ie: float) -> float:
        """Returns the temperature of the fluid at a given internal energy.

        :param ie: The internal energy of the fluid.
        :return: The temperature of the fluid at the given internal energy.
        """
        return float(np.interp(np.array([ie]), self.IE, self.T).item())

    def get_density(self, t: float) -> float:
        """Returns the density of the fluid at a given temperature.

        :param t: The temperature of the fluid.
        :return: The density of the fluid at the given temperature.
        """
        return float(np.interp(np.array([t]), self.T, self.rho).item())

    def get_viscosity(self, t: float) -> float:
        """Returns the viscosity of the fluid at a given temperature.

        :param t: The temperature of the fluid.
        :return: The viscosity of the fluid at the given temperature.
        """
        return float(np.interp(np.array([t]), self.T, self.visc).item())

    def get_heat_capacity(self, t: float) -> float:
        """Returns the heat capacity of the fluid at a given temperature.

        :param t: The temperature of the fluid.
        :return: The capacity of the fluid at the given temperature.
        """
        return float(np.interp(np.array([t]), self.T, self.cp).item())

    def get_thermal_conductivity(self, t: float) -> float:
        """Returns the thermal conductivity of the fluid at a given temperature.

        :param t: The temperature of the fluid.
        :return: The thermal conductivity of the fluid at the given temperature.
        """
        return float(np.interp(np.array([t]), self.T, self.therm_cond)[0])


fluid_props = FluidProperties()
