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

import unittest
from pathlib import Path

from omotes_simulator_core.adapter.transforms.controller_mapper import EsdlControllerMapper
from omotes_simulator_core.entities.assets.controller import (
    ControllerIdealHeatStorage,
    ControllerAtesStorage,
)
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.entities.network_controller import NetworkController
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file


class TestEsdlControllerMapper(unittest.TestCase):

    def test_to_entity(self):
        esdl_file_path = (
            Path(__file__).parent
            / ".."
            / ".."
            / ".."
            / ".."
            / "testdata"
            / "heat_transfers_test.esdl"
        )
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        mapper = EsdlControllerMapper()

        # Act
        result = mapper.to_entity(esdl_object)
        # Assert
        self.assertIsInstance(result, NetworkController)
        self.assertEqual(len(result.networks), 3)
        self.assertEqual(result.networks[0].path, [])
        self.assertEqual(result.networks[1].path, ["1", "0"])
        self.assertEqual(result.networks[2].path, ["2", "1", "0"])

    def test_ideal_heat_storage_conversion(self):
        # Arrange
        esdl_file_path = (
            Path(__file__).parent / ".." / ".." / ".." / ".." / "testdata" / "test_buffer.esdl"
        )
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        mapper = EsdlControllerMapper()
        # Act
        storages = mapper.convert_heat_storages_and_ates(esdl_object)
        # Assert
        self.assertEqual(len(storages), 1)
        self.assertIsInstance(storages[0], ControllerIdealHeatStorage)

    def test_ates_conversion(self):
        # Arrange
        esdl_file_path = (
            Path(__file__).parent / ".." / ".." / ".." / ".." / "testdata" / "test_ates.esdl"
        )
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        mapper = EsdlControllerMapper()
        # Act
        storages = mapper.convert_heat_storages_and_ates(esdl_object)
        # Assert
        self.assertEqual(len(storages), 1)
        self.assertIsInstance(storages[0], ControllerAtesStorage)
