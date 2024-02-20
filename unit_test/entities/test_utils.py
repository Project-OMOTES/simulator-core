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

"""Test utility functions."""
import unittest
from pathlib import Path
import numpy as np
from unittest.mock import Mock

from simulator_core.entities.assets.utils import (
    calculate_inverse_heat_transfer_coefficient,
    get_thermal_conductivity_table,
    heat_demand_and_temperature_to_mass_flow,
    mass_flow_and_temperature_to_heat_demand,
)
from simulator_core.entities.esdl_object import EsdlObject
from simulator_core.infrastructure.utils import pyesdl_from_file


class UtilFunctionTest(unittest.TestCase):
    """Testcase for Utility functions class."""

    def setUp(self) -> None:
        """Set up test case."""
        # Mock pandapipes net
        # Load esdl pipe asset
        esdl_file_path = (
            Path(__file__).parent / ".." / ".." / "testdata" / "test_pipe_material.esdl"
        )
        esdl_file_path = str(esdl_file_path)
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        pipes = esdl_object.get_all_assets_of_type("pipe")
        self.pipe_with_material = [
            pipe for pipe in pipes if pipe.esdl_asset.name == "pipe_with_material"
        ][0]
        self.pipe_without_material = [
            pipe for pipe in pipes if pipe.esdl_asset.name == "pipe_without_material"
        ][0]
        self.pipe_with_reference = [
            pipe for pipe in pipes if pipe.esdl_asset.name == "pipe_with_reference_01"
        ][0]

    def test_heat_demand_and_temperature_to_mass_flow(self) -> None:
        """Test heat_demand_and_temperature_to_mass_flow."""
        # Arrange
        thermal_demand = 1000  # [w]
        temperature_supply = 373  # [K]
        temperature_return = 353  # [K]

        # act
        mass_flow_calculated = heat_demand_and_temperature_to_mass_flow(
            thermal_demand, temperature_supply, temperature_return
        )  # act

        # Assert
        assert mass_flow_calculated == 0.011891030595621722

    def test_mass_flow_and_temperature_to_heat_demand(self) -> None:
        """Test mass_flow_and_temperature_to_heat_demand."""
        # Arrange
        temperature_supply = 373  # [K]
        temperature_return = 353  # [K]
        mass_flow = 0.011956001912960305

        # Act
        heat_demand_calculated = mass_flow_and_temperature_to_heat_demand(
            temperature_supply, temperature_return, mass_flow
        )  # act

        # Assert
        assert heat_demand_calculated == 1005.5263629842184

    def test_calculate_inverse_heat_transfer_coefficient(self) -> None:
        """Test calculate_inverse_heat_transfer_coefficient.

        The method returns the inverse of the heat transfer coefficient.
        """
        # Arrange
        inner_diameter = np.array([0.1])
        outer_diameter = np.array([0.2])
        thermal_conductivity = np.array([0.5])

        # Act
        heat_transfer_coefficient = calculate_inverse_heat_transfer_coefficient(
            inner_diameter, outer_diameter, thermal_conductivity
        )  # act

        # Assert
        assert heat_transfer_coefficient == 0.06931471805599453

    def test_get_thermal_conductivity_table_component(self) -> None:
        """Test get_thermal_conductivity_table."""
        # Arrange

        # Act
        diameters, heat_coefficients = get_thermal_conductivity_table(
            esdl_asset=self.pipe_with_material
        )  # act

        # Assert
        assert diameters == [0.1071, 0.1143, 0.1936, 0.2]
        assert heat_coefficients == [52.15, 0.027, 0.4]

    def test_get_thermal_conductivity_table_no_material(self) -> None:
        """Test get_thermal_conductivity_table."""
        # Arrange

        # Act
        diameters, heat_coefficients = get_thermal_conductivity_table(
            esdl_asset=self.pipe_without_material
        )  # act

        # Assert
        assert diameters == []
        assert heat_coefficients == []

    def test_get_thermal_conductivity_table_error(self) -> None:
        """Test get_thermal_conductivity_table."""
        # Arrange
        esdl_asset_mock = Mock()

        # Act
        esdl_asset_mock.esdl_asset.material.Error = "Error"
        delattr(esdl_asset_mock.esdl_asset.material, "component")
        delattr(esdl_asset_mock.esdl_asset.material, "reference")

        # Assert
        with self.assertRaises(NotImplementedError):
            get_thermal_conductivity_table(esdl_asset=esdl_asset_mock)
