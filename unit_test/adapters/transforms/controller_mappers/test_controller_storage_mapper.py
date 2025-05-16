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

"""Test ControllerStorageMapper."""

import unittest
from pathlib import Path

from omotes_simulator_core.adapter.transforms.controller_mappers import (
    ControllerStorageMapper,
)
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file


class TestControllerStorageMapper(unittest.TestCase):
    """Test ControllerStorageMapper."""

    def setUp(self) -> None:
        """Set up test case."""
        # Load the test esdl file
        esdl_file_path = (
            Path(__file__).parent / ".." / ".." / ".." / ".." / "testdata" / "test_ates.esdl"
        )
        self.esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        # Create a ControllerStorageMapper object
        self.mapper = ControllerStorageMapper()

    def test_to_entity_method(self):
        """Test settings of controller for Storage."""
        # Arrange
        storage_assets = self.esdl_object.get_all_assets_of_type("storage")

        # Act
        controller_storage = self.mapper.to_entity(storage_assets[0])

        # Assert
        self.assertEqual(controller_storage.temperature_out, 353.15)
        self.assertEqual(controller_storage.temperature_in, 313.15)
        self.assertEqual(controller_storage.max_charge_power, 11.61e6)
        self.assertEqual(controller_storage.max_discharge_power, 11.61e6)
