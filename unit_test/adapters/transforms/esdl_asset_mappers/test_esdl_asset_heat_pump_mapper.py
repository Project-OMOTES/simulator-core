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

"""Test heat pump mapper."""

import unittest
from pathlib import Path

from omotes_simulator_core.adapter.transforms.esdl_asset_mappers.heat_pump_mapper import (
    EsdlAssetHeatPumpMapper,
)
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file


class TestEsdlAssetHeatPumpMapper(unittest.TestCase):
    """Test class for heat pump mapper."""

    def setUp(self) -> None:
        """Set up test case."""
        esdl_file_path = (
            Path(__file__).parent / ".." / ".." / ".." / ".." / "testdata" / "simple_heat_pump.esdl"
        )
        self.esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        self.mapper = EsdlAssetHeatPumpMapper()

    def test_to_entity_method(self):
        """Test for to_entity method."""
        # Arrange
        pumps = self.esdl_object.get_all_assets_of_type("pump")
        esdl_asset = pumps[0]

        # Act
        heatpump_entity = self.mapper.to_entity(esdl_asset)

        # Assert
        self.assertEqual(heatpump_entity.name, esdl_asset.esdl_asset.name)
        self.assertEqual(heatpump_entity.asset_id, esdl_asset.esdl_asset.id)
        self.assertEqual(heatpump_entity.connected_ports, esdl_asset.get_port_ids())

if __name__ == '__main__':
    test = TestEsdlAssetHeatPumpMapper()
    test.setUp()
    test.test_to_entity_method()