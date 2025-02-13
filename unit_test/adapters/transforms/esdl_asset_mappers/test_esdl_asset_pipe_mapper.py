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

"""Test pipe mapper."""
import typing
import unittest
from pathlib import Path
from unittest.mock import Mock

from omotes_simulator_core.adapter.transforms.esdl_asset_mappers.pipe_mapper import (
    EsdlAssetPipeMapper,
)
from omotes_simulator_core.entities.assets.asset_defaults import PIPE_DEFAULTS
from omotes_simulator_core.entities.assets.pipe import Pipe
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file


class TestEsdlAssetPipeMapper(unittest.TestCase):
    """Test class for pipe mapper."""

    def setUp(self) -> None:
        """Define the variables used in the tests."""
        self.length: float = 1
        self.inner_diameter: float = 1
        self.roughness: float = 0.001
        self.alpha_value: float = 0.8
        self.minor_loss_coefficient: float = 0.0
        self.external_temperature: float = 273.15 + 20.0
        self.qheat_external: float = 0.0

        # Arranging standard objects for the other test
        esdl_file_path = (
            Path(__file__).parent
            / ".."
            / ".."
            / ".."
            / ".."
            / "testdata"
            / "test_pipe_roughness.esdl"
        )
        self.esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        self.mapper = EsdlAssetPipeMapper()

    def test_to_entity_method(self) -> None:
        """Test for to_entity method."""
        # Arrange
        pipes = self.esdl_object.get_all_assets_of_type("pipe")
        self.assertGreater(len(pipes), 0, "No pipes found in the ESDL file.")
        self.esdl_asset = pipes[0]
        esdl_asset = pipes[0]

        # Act
        pipe_entity = typing.cast(Pipe, self.mapper.to_entity(esdl_asset))

        # Assert
        self.assertIsInstance(pipe_entity, Pipe)
        self.assertEqual(pipe_entity.name, esdl_asset.esdl_asset.name)
        self.assertEqual(pipe_entity.asset_id, esdl_asset.esdl_asset.id)
        self.assertEqual(pipe_entity.connected_ports, esdl_asset.get_port_ids())  # type: ignore
        self.assertEqual(
            pipe_entity.length,
            esdl_asset.get_property("length", PIPE_DEFAULTS.length),  # type: ignore
        )
        self.assertEqual(
            pipe_entity.inner_diameter,  # type: ignore
            esdl_asset.get_property("innerDiameter", PIPE_DEFAULTS.diameter),
        )
        self.assertEqual(
            pipe_entity.roughness,  # type: ignore
            esdl_asset.get_property("roughness", PIPE_DEFAULTS.roughness),
        )
        self.assertEqual(
            pipe_entity.alpha_value,  # type: ignore
            self.mapper._get_heat_transfer_coefficient(esdl_asset),
        )
        self.assertEqual(
            pipe_entity.minor_loss_coefficient,  # type: ignore
            esdl_asset.get_property("minor_loss_coefficient", PIPE_DEFAULTS.minor_loss_coefficient),
        )
        self.assertEqual(
            pipe_entity.external_temperature,  # type: ignore
            esdl_asset.get_property("external_temperature", PIPE_DEFAULTS.external_temperature),
        )
        self.assertEqual(
            pipe_entity.qheat_external,  # type: ignore
            esdl_asset.get_property("qheat_external", PIPE_DEFAULTS.qheat_external),
        )

    def test_pipe_get_property_diameter(self) -> None:
        """Evaluate the get property diameter method to retrieve diameters."""
        # Arrange
        esdl_asset_mock = Mock()
        esdl_asset_mock.get_property.return_value = 1.0
        esdl_asset_mock.has_property.return_value = True

        # Act
        pass

        # Assert
        self.assertEqual(EsdlAssetPipeMapper._get_diameter(esdl_asset=esdl_asset_mock), 1.0)

    def test_pipe_get_heat_transfer_coefficient(self) -> None:
        """Evaluate the get heat transfer coefficient method."""
        # Arrange
        # - Load esdl pipe asset
        esdl_file_path = (
            Path(__file__).parent
            / ".."
            / ".."
            / ".."
            / ".."
            / "testdata"
            / "test_pipe_material.esdl"
        )
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        esdl_pipes = esdl_object.get_all_assets_of_type("pipe")
        esdl_pipe = [pipe for pipe in esdl_pipes if pipe.esdl_asset.name == "pipe_with_material"][0]

        # Act
        alpha_value = EsdlAssetPipeMapper._get_heat_transfer_coefficient(
            esdl_asset=esdl_pipe
        )  # act

        # Assert
        self.assertEqual(alpha_value, 0.8901927763663371)
