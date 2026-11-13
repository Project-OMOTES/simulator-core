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

import numpy as np
import numpy.testing as npt

from omotes_simulator_core.solver.utils.fluid_properties import Interpolation, OmotesFluidProperties


def _power_sum(interpolation: Interpolation, value: float) -> float:
    """Evaluate the fitted polynomial using the original explicit-power algorithm."""
    result = 0.0
    power = 1.0
    for index in range(interpolation.order, -1, -1):
        result += interpolation.coefficients[index] * power
        power *= value
    return float(result)


class InterpolationTest(unittest.TestCase):
    """Test the Interpolation class."""

    def test_init(self):
        """Test the initialization of the Interpolation class."""
        # Arrange
        x = [1, 2, 3]
        y = [2, 4, 6]
        order = 1

        # Act
        interpolation = Interpolation(x, y, order)

        # Assert
        self.assertEqual(interpolation.x, x)
        self.assertEqual(interpolation.y, y)
        self.assertEqual(interpolation.order, order)
        npt.assert_almost_equal(interpolation.coefficients, np.array([2, 0]))

    def test_init_order_5(self):
        """Test the initialization of the Interpolation class."""
        # Arrange
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        order = 5
        y = [value**order for value in x]

        # Act
        interpolation = Interpolation(x, y, order)

        # Assert
        self.assertEqual(interpolation.x, x)
        self.assertEqual(interpolation.y, y)
        self.assertEqual(interpolation.order, order)
        npt.assert_almost_equal(interpolation.coefficients, np.array([1, 0, 0, 0, 0, 0]))

    def test_call(self):
        """Test the call method of the Interpolation class."""
        # Arrange
        x = [1, 2, 3]
        y = [2, 4, 6]
        order = 1
        interpolation = Interpolation(x, y, order)

        # Act
        interpolated_value = interpolation(2)

        # Assert
        self.assertAlmostEqual(interpolated_value, 4)

    def test_call_order_5(self):
        """Test the call method of the Interpolation class."""
        # Arrange
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        order = 5
        y = [value**order for value in x]
        interpolation = Interpolation(x, y, order)

        # Act
        interpolated_value = interpolation(2)

        # Assert
        self.assertAlmostEqual(interpolated_value, 32)

    def test_horner_evaluation_for_scalar_types_and_polynomial_orders(self) -> None:
        for order in (1, 5, 6):
            coefficients = np.array([(-1.0) ** i / (i + 1) for i in range(order + 1)])
            x = np.linspace(1.0, 2.0, 12)
            interpolation = Interpolation(x.tolist(), np.polyval(coefficients, x).tolist(), order)
            self.assertIsInstance(interpolation.coefficients, np.ndarray)
            for value in np.linspace(0.9, 2.2, 21):
                for scalar_type in (float, np.float64):
                    with self.subTest(order=order, value=value, scalar_type=scalar_type):
                        scalar = scalar_type(value)
                        result = interpolation(scalar)
                        self.assertIs(type(result), float)
                        npt.assert_allclose(result, _power_sum(interpolation, scalar), rtol=1e-10)
                        npt.assert_allclose(
                            result, np.polyval(coefficients, scalar), rtol=1e-10, atol=1e-10
                        )

    def test_constant_polynomial_preserves_numpy_validation_semantics(self) -> None:
        for constant in (0.0, 2.0):
            with self.subTest(constant=constant):
                with self.assertWarns(RuntimeWarning):
                    interpolation = Interpolation([1.0, 2.0, 3.0], [constant] * 3, 0)
                self.assertAlmostEqual(interpolation(1.5), constant)
                self.assertIs(type(interpolation(np.float64(1.5))), float)

    def test_evaluation_at_and_immediately_outside_bounds(self) -> None:
        interpolation = Interpolation([1.0, 2.0, 3.0], [2.0, 4.0, 6.0], 1)
        lower = interpolation.x[0] * (1.0 - interpolation.bounds)
        upper = interpolation.x[-1] * (1.0 + interpolation.bounds)
        for value in (lower, interpolation.x[0], interpolation.x[-1], upper):
            with self.subTest(value=value):
                self.assertAlmostEqual(interpolation(value), 2.0 * value)
        for value in (np.nextafter(lower, -np.inf), np.nextafter(upper, np.inf)):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, r"^Value is out of bounds\.$"):
                    interpolation(value)

    def test_evaluation_observes_coefficient_mutations(self) -> None:
        interpolation = Interpolation([1.0, 2.0, 3.0], [2.0, 4.0, 6.0], 1)
        self.assertAlmostEqual(interpolation(2.0), 4.0)
        interpolation.coefficients[:] = [3.0, -1.0]
        self.assertAlmostEqual(interpolation(2.0), 5.0)
        interpolation.coefficients = np.array([4.0, 5.0])
        self.assertAlmostEqual(interpolation(2.0), 13.0)

    def test_validation_error(self):
        """Test the validation error method of the Interpolation class."""
        # Arrange
        x = [1, 2, 3]
        y = [2, 4, 6]
        order = 1
        interpolation = Interpolation(x, y, order)
        interpolation.coefficients = np.array([0, 1])

        # Act
        with self.assertRaises(ValueError) as cm:
            interpolation._check_interpolation()

        # Assert
        self.assertEqual(str(cm.exception), "Interpolation error: error is more then 2%.")
        self.assertIsInstance(cm.exception, ValueError)

    def test_check_bounds(self):
        """Test the check bounds method of the Interpolation class."""
        # Arrange
        x = [1, 2, 3]
        y = [2, 4, 6]
        order = 1
        interpolation = Interpolation(x, y, order)

        # Act
        with self.assertRaises(ValueError) as cm:
            interpolation._check_bounds(0)

        # Assert
        self.assertEqual(str(cm.exception), "Value is out of bounds.")
        self.assertIsInstance(cm.exception, ValueError)

    def test_check_real_polynomial(self):
        """Test the check real polynomial method of the Interpolation class."""
        # Arrange
        a = 2.0
        b = 3.0
        c = 4.0
        x = [*range(10)]
        y = [a * i**2 + b * i + c for i in x]
        interpol = Interpolation(x, y, 2)
        # Act
        result = interpol(5)

        # Assert
        self.assertAlmostEqual(result, 2 * 5**2 + 3 * 5 + 4, 3)


class OmotesFluidPropertiesTest(unittest.TestCase):
    """Test the OmotesFluidProperties class."""

    def setUp(self):
        """Set up the test."""
        self.omotes_fluid_properties = OmotesFluidProperties()

    def test_init(self):
        """Test the initialization of the OmotesFluidProperties class."""
        # Arrange
        T = [i + 273.15 for i in range(150)]

        # Act
        omotes_fluid_properties = OmotesFluidProperties()

        # Assert
        self.assertEqual(omotes_fluid_properties.T, T)
        self.assertAlmostEqual(len(omotes_fluid_properties.rho), 150)
        self.assertAlmostEqual(len(omotes_fluid_properties.visc), 150)
        self.assertAlmostEqual(len(omotes_fluid_properties.therm_cond), 150)
        self.assertAlmostEqual(len(omotes_fluid_properties.cp), 150)
        self.assertAlmostEqual(len(omotes_fluid_properties.IE), 150)

    def test_all_property_fits_match_power_sums_over_accepted_bounds(self) -> None:
        for name in (
            "ie_func",
            "temp_func",
            "density_func",
            "visc_func",
            "heat_cap_func",
            "therm_cond_func",
        ):
            with self.subTest(property=name):
                interpolation = getattr(self.omotes_fluid_properties, name)
                lower = interpolation.x[0] * (1.0 - interpolation.bounds)
                upper = interpolation.x[-1] * (1.0 + interpolation.bounds)
                values = np.unique(
                    np.concatenate((np.linspace(lower, upper, 1001), interpolation.x))
                )
                reference = np.array([_power_sum(interpolation, value) for value in values])
                evaluated = [interpolation(value) for value in values]
                self.assertTrue(all(type(value) is float for value in evaluated))
                magnitudes = np.polyval(np.abs(interpolation.coefficients), np.abs(values))
                roundoff_bound = 32 * np.finfo(float).eps * magnitudes
                npt.assert_array_less(np.abs(evaluated - reference), roundoff_bound)

    def test_get_density(self):
        """Test the get_density method of the OmotesFluidProperties class."""
        # Arrange
        T = 300

        # Act
        density = self.omotes_fluid_properties.get_density(T)

        # Assert
        self.assertAlmostEqual(density, 997.4151741509487, 3)

    def test_get_viscosity(self):
        """Test the get_viscosity method of the OmotesFluidProperties class."""
        # Arrange
        T = 300

        # Act
        viscosity = self.omotes_fluid_properties.get_viscosity(T)

        # Assert
        self.assertAlmostEqual(viscosity, 8.498706251104486e-07, 3)

    def test_get_heat_capacity(self):
        """Test the get_heat_capacity method of the OmotesFluidProperties class."""
        # Arrange
        T = 300

        # Act
        heat_capacity = self.omotes_fluid_properties.get_heat_capacity(T)

        # Assert
        self.assertAlmostEqual(heat_capacity, 4175.063249530409, 3)

    def test_get_ie(self):
        """Test the get_ie method of the OmotesFluidProperties class."""
        # Arrange
        T = 300

        # Act
        ie = self.omotes_fluid_properties.get_ie(T)

        # Assert
        self.assertAlmostEqual(ie, 112413.55124584399, 3)

    def test_get_t(self):
        """Test the get_t method of the OmotesFluidProperties class."""
        # Arrange
        ie = 0.0

        # Act
        T = self.omotes_fluid_properties.get_t(ie)

        # Assert
        self.assertAlmostEqual(T, 273.1442035399455, 3)
