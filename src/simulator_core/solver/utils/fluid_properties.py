import numpy as np
import csv


class FluidProperties:

    def __init__(self):
        """Constructor of the fluid properties class.

        Initializes the class properties and loads the fluid properties from a csv file.
        """
        file = r'.\src\simulator_core\solver\utils\temp_props.csv'
        self.T = []
        self.cp = []
        self.rho = []
        self.visc = []
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                self.T.append(float(row[0]))
                self.cp.append(float(row[1]))
                self.rho.append(float(row[2]))
                self.visc.append(float(row[3]))

        self.IE = [0.0]
        for i in range(1, len(self.T)):
            self.IE.append(self.IE[-1] + (self.cp[i-1] + self.cp[i]) / 2 * (self.T[i] - self.T[i-1]))

    def get_ie(self, t: float) -> float:
        """Returns the internal energy of the fluid at a given temperature.

        :param t: The temperature of the fluid.
        :return: The internal energy of the fluid at the given temperature.
        """
        return float(np.interp(t, self.T, self.IE))

    def get_t(self, ie: float) -> float:
        """Returns the temperature of the fluid at a given internal energy.

        :param ie: The internal energy of the fluid.
        :return: The temperature of the fluid at the given internal energy.
        """
        return float(np.interp(ie, self.IE, self.T))

    def get_density(self, t: float) -> float:
        """Returns the density of the fluid at a given temperature.

        :param t: The temperature of the fluid.
        :return: The density of the fluid at the given temperature.
        """
        return float(np.interp(t, self.T, self.rho))

    def get_viscosity(self, t: float) -> float:
        """Returns the viscosity of the fluid at a given temperature.

        :param t: The temperature of the fluid.
        :return: The viscosity of the fluid at the given temperature.
        """
        return float(np.interp(t, self.T, self.visc))