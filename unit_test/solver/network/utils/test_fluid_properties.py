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

"""Test Fluid properties entities."""
import unittest
from unittest.mock import patch

from simulator_core.solver.utils.fluid_properties import FluidProperties


class FluidPropertiesInitializationTest(unittest.TestCase):
    """Testcase for the initialization of the FluidProperties class."""

    @patch("csv.reader")
    def test_init_of_fluid_properties(self, mock_csv_reader):
        """Test the initialization of the fluid properties class."""
        # Arrange
        mock_csv_reader.return_value = [["1", "2", "3", "4", "5"], ["6", "7", "8", "9", "10"]]

        # Act
        fluid_props = FluidProperties()  # act

        # Assert
        self.assertEqual(fluid_props.T, [1, 6])
        self.assertEqual(fluid_props.cp, [2, 7])
        self.assertEqual(fluid_props.rho, [3, 8])
        self.assertEqual(fluid_props.visc, [4, 9])
        self.assertEqual(fluid_props.therm_cond, [5, 10])
        self.assertEqual(fluid_props.IE, [0, 22.5])
        self.assertEqual(mock_csv_reader.call_count, 1)


class FluidPropertiesTest(unittest.TestCase):
    """Testcase for FluidProperties class."""

    @patch("csv.reader")
    def setUp(self, mock_csv_reader):
        """Set up the test."""
        mock_csv_reader.return_value = [["1", "2", "3", "4", "5"], ["6", "7", "8", "9", "10"]]

        self.fluid_props = FluidProperties()

    def test_get_internal_energy(self):
        """Test the get_internal_energy method."""
        # Arrange
        T = 1

        # Act
        IE = self.fluid_props.get_ie(T)

        # Assert
        self.assertEqual(IE, 0)

    def test_get_internal_energy_with_invalid_temperature(self):
        """Test the get_internal_energy method with an invalid temperature."""
        # Arrange
        T = 0

        # Act
        with self.assertRaises(ValueError) as cm:
            self.fluid_props.get_ie(T)

        # Assert
        self.assertEqual(
            str(cm.exception), "The temperature 0 is outside the range of the fluid properties."
        )
        self.assertIsInstance(cm.exception, ValueError)

    def test_get_temperature(self):
        """Test the get_temperature method."""
        # Arrange
        IE = 0

        # Act
        T = self.fluid_props.get_t(IE)

        # Assert
        self.assertEqual(T, 1)

    def test_get_temperature_with_invalid_internal_energy(self):
        """Test the get_temperature method with an invalid internal energy."""
        # Arrange
        IE = -1

        # Act
        with self.assertRaises(ValueError) as cm:
            self.fluid_props.get_t(IE)

        # Assert
        self.assertEqual(
            str(cm.exception),
            "The internal energy -1 is outside the range of the fluid properties.",
        )
        self.assertIsInstance(cm.exception, ValueError)

    def test_get_density(self):
        """Test the get_density method."""
        # Arrange
        T = 1

        # Act
        rho = self.fluid_props.get_density(T)

        # Assert
        self.assertEqual(rho, 3)

    def test_get_density_with_invalid_temperature(self):
        """Test the get_density method with an invalid temperature."""
        # Arrange
        T = 0

        # Act
        with self.assertRaises(ValueError) as cm:
            self.fluid_props.get_density(T)

        # Assert
        self.assertEqual(
            str(cm.exception), "The temperature 0 is outside the range of the fluid properties."
        )
        self.assertIsInstance(cm.exception, ValueError)

    def test_get_viscosity(self):
        """Test the get_viscosity method."""
        # Arrange
        T = 1

        # Act
        visc = self.fluid_props.get_viscosity(T)

        # Assert
        self.assertEqual(visc, 4)

    def test_get_viscosity_with_invalid_temperature(self):
        """Test the get_viscosity method with an invalid temperature."""
        # Arrange
        T = 0

        # Act
        with self.assertRaises(ValueError) as cm:
            self.fluid_props.get_viscosity(T)

        # Assert
        self.assertEqual(
            str(cm.exception), "The temperature 0 is outside the range of the fluid properties."
        )
        self.assertIsInstance(cm.exception, ValueError)

    def test_get_heat_capacity(self):
        """Test the get_heat_capacity method."""
        # Arrange
        T = 1

        # Act
        cp = self.fluid_props.get_heat_capacity(T)

        # Assert
        self.assertEqual(cp, 2)

    def test_get_heat_capacity_with_invalid_temperature(self):
        """Test the get_heat_capacity method with an invalid temperature."""
        # Arrange
        T = 0

        # Act
        with self.assertRaises(ValueError) as cm:
            self.fluid_props.get_heat_capacity(T)

        # Assert
        self.assertEqual(
            str(cm.exception), "The temperature 0 is outside the range of the fluid properties."
        )
        self.assertIsInstance(cm.exception, ValueError)

    def test_get_thermal_conductivity(self):
        """Test the get_thermal_conductivity method."""
        # Arrange
        T = 1

        # Act
        therm_cond = self.fluid_props.get_thermal_conductivity(T)

        # Assert
        self.assertEqual(therm_cond, 5)

    def test_get_thermal_conductivity_with_invalid_temperature(self):
        """Test the get_thermal_conductivity method with an invalid temperature."""
        # Arrange
        T = 0

        # Act
        with self.assertRaises(ValueError) as cm:
            self.fluid_props.get_thermal_conductivity(T)

        # Assert
        self.assertEqual(
            str(cm.exception), "The temperature 0 is outside the range of the fluid properties."
        )
        self.assertIsInstance(cm.exception, ValueError)
