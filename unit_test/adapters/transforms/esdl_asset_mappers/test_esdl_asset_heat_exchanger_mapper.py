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

"""Test HeatExchanger mapper."""

import unittest
from pathlib import Path

from omotes_simulator_core.adapter.transforms.esdl_asset_mappers.heat_exchanger_mapper import (
    EsdlAssetHeatExchangerMapper,
)
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file


class TestEsdlAssetHeatExchangerMapper(unittest.TestCase):
    """Test class for heat exchanger mapper."""

    def setUp(self) -> None:
        """Set up test case."""
        esdl_file_path = (
            Path(__file__).parent
            / ".."
            / ".."
            / ".."
            / ".."
            / "testdata"
            / "simple_heat_exchanger.esdl"
        )
        self.esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        self.mapper = EsdlAssetHeatExchangerMapper()

    def test_to_entity_method(self):
        """Test for to_entity method."""
        # Arrange
        exchangers = self.esdl_object.get_all_assets_of_type("heat_exchanger")
        esdl_asset = exchangers[0]

        # Act
        heat_exchanger_entity = self.mapper.to_entity(esdl_asset)

        # Assert
        self.assertEqual(heat_exchanger_entity.name, esdl_asset.esdl_asset.name)
        self.assertEqual(heat_exchanger_entity.asset_id, esdl_asset.esdl_asset.id)
        self.assertEqual(heat_exchanger_entity.connected_ports, esdl_asset.get_port_ids())
