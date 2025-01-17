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

"""Test producer mapper."""

import unittest
from pathlib import Path

from omotes_simulator_core.adapter.transforms.esdl_asset_mappers.producer_mapper import (
    EsdlAssetProducerMapper,
)
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file


class TestEsdlAssetProducerMapper(unittest.TestCase):
    """Test class for producer mapper."""

    def setUp(self) -> None:
        """Set up test case."""
        esdl_file_path = (
            Path(__file__).parent / ".." / ".." / ".." / ".." / "testdata" / "test1.esdl"
        )
        self.esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        self.mapper = EsdlAssetProducerMapper()

    def test_to_entity_method(self):
        """Test for to_entity method."""
        # Arrange
        producers = self.esdl_object.get_all_assets_of_type("producer")
        esdl_asset = producers[0]

        # Act
        producer_entity = self.mapper.to_entity(esdl_asset)

        # Assert
        self.assertEqual(producer_entity.name, esdl_asset.esdl_asset.name)
        self.assertEqual(producer_entity.asset_id, esdl_asset.esdl_asset.id)
        self.assertEqual(producer_entity.connected_ports, esdl_asset.get_port_ids())
