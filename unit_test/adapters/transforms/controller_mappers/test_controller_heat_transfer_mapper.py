#  Copyright (c) 2025. Deltares & TNO
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

"""Test ControllerConsumerMapper."""

import unittest
from pathlib import Path

from omotes_simulator_core.adapter.transforms.controller_mappers import (
    ControllerHeatTransferMapper,
)
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file


class TestControllerHeatTransferMapper(unittest.TestCase):

    def test_to_entity_method_heat_pump(self):
        # Arrange
        # Load the test esdl file
        esdl_file_path = (
            Path(__file__).parent / ".." / ".." / ".." / ".." / "testdata" / "simple_heat_pump.esdl"
        )
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        # Create a ControllerConsumerMapper object
        mapper = ControllerHeatTransferMapper()
        heat_transfer_assets = esdl_object.get_all_assets_of_type("heat_transfer")

        # Act
        controller_heat_pump = mapper.to_entity(heat_transfer_assets[0])

        # Assert
        pass

    def test_to_entity_method_heat_exchanger(self):
        esdl_file_path = (
            Path(__file__).parent
            / ".."
            / ".."
            / ".."
            / ".."
            / "testdata"
            / "Simple_heat_exchange.esdl"
        )
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        # Create a ControllerConsumerMapper object
        mapper = ControllerHeatTransferMapper()
        heat_transfer_assets = esdl_object.get_all_assets_of_type("heat_transfer")

        # Act
        controller_heat_exchange = mapper.to_entity(heat_transfer_assets[0])

        # Assert
        pass
