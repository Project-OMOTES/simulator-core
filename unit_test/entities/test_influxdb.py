#  Copyright (c) 2024. Deltares & TNO
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

"""Test influxdb reader."""
import unittest
from simulator_core.entities.utility.influxdb_reader import get_data_from_profile, get_unit
from pathlib import Path
import esdl
from esdl.esdl_handler import EnergySystemHandler
from unittest.mock import Mock


class InfluxdbTest(unittest.TestCase):
    """Testcase for Influxdb class."""

    def test_get_unit(self) -> None:
        """Test get_unit."""
        # Arrange
        unit = Mock()
        unit.profileQuantityAndUnit.reference.physicalQuantity = esdl.PhysicalQuantityEnum.POWER

        unit_energy = Mock()
        del unit_energy.profileQuantityAndUnit.reference.physicalQuantity
        unit_energy.profileQuantityAndUnit.physicalQuantity = esdl.PhysicalQuantityEnum.ENERGY
        unit_pressure_mock = Mock()
        unit_pressure_mock.profileQuantityAndUnit.reference.physicalQuantity = (
            esdl.PhysicalQuantityEnum.PRESSURE)
        # Act
        unit = get_unit(unit)
        unit_energy = get_unit(unit_energy)
        unit_pressure = get_unit(unit_pressure_mock)
        # Assert
        self.assertEqual(unit.id, "POWER_in_W")
        self.assertEqual(unit_energy.id, "ENERGY_in_J")
        self.assertEqual(unit_pressure, esdl.PhysicalQuantityEnum.PRESSURE)

    def test_get_data_from_profile(self) -> None:
        """Test get_data_from_profile."""
        # Arrange
        esdl_file_path = Path(__file__).parent / ".." / ".." / "testdata" / "test1.esdl"
        esdl_file_path = str(esdl_file_path)
        es = EnergySystemHandler()
        es.load_file(esdl_file_path)
        asset = es.get_all_instances_of_type(esdl.HeatingDemand)[0]
        profile = asset.port[1].profile[0]
        # Act
        data = get_data_from_profile(profile)
        # Assert
        self.assertEqual(len(data), 24 * 365)
        self.assertAlmostEqual(data['values'][0], 364133.913, 5)
