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
from unittest.mock import Mock, patch

from omotes_simulator_core.adapter.transforms.esdl_asset_mappers.pipe_mapper import (
    EsdlAssetPipeMapper,
)
from omotes_simulator_core.entities.assets.asset_defaults import PIPE_DEFAULTS, PipeSchedules
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

    def test_pipe_get_diameter_with_inner_diameter(self):
        """Returns the innerDiameter if it is specified and non-zero."""
        # Arrange
        esdl_asset_mock = Mock()

        def mock_get_property(key, default=None):
            if key == "innerDiameter":
                return 0.5
            if key == "diameter":
                return None
            return default

        esdl_asset_mock.get_property = mock_get_property

        # Act
        diameter = EsdlAssetPipeMapper._get_diameter(esdl_asset_mock)

        # Assert
        self.assertEqual(diameter, 0.5)

    def test_get_diameter_with_nominal_diameter_uses_edr(self):
        """Returns converted diameter from EDR when innerDiameter is zero and DN is provided."""
        # Arrange
        esdl_asset_mock = Mock()
        dn_mock = Mock()
        dn_mock.name = "DN50"

        def mock_get_property(key, default=None):
            if key == "innerDiameter":
                return 0
            if key == "diameter":
                return dn_mock
            return default

        esdl_asset_mock.get_property = mock_get_property
        edr_object_mock = Mock()
        edr_object_mock.innerDiameter = 0.42

        with patch.object(
            EsdlAssetPipeMapper, "_get_esdl_object_from_edr", return_value=edr_object_mock
        ):
            # Act
            diameter = EsdlAssetPipeMapper._get_diameter(esdl_asset_mock)

            # Assert
            self.assertEqual(diameter, 0.42)

    def test_get_diameter_default_when_none_provided(self):
        """Returns default diameter when both innerDiameter is 0 and diameter is None."""
        # Arrange
        esdl_asset_mock = Mock()

        def mock_get_property(key, default=None):
            if key == "innerDiameter":
                return 0
            if key == "diameter":
                return None
            return default

        esdl_asset_mock.get_property = mock_get_property

        # Act
        diameter = EsdlAssetPipeMapper._get_diameter(esdl_asset_mock)

        # Assert
        self.assertEqual(diameter, PIPE_DEFAULTS.diameter)

    def test_get_esdl_object_from_edr(self):
        """Test that the correct ESDL object is returned from EDR using DN and default schedule."""
        # Arrange
        with patch(
            "omotes_simulator_core.adapter.transforms.esdl_asset_mappers.pipe_mapper.EDRClient"
        ) as mock_edr_client_class:
            mock_edr_client = mock_edr_client_class.return_value
            expected_object = Mock()
            mock_edr_client.get_object_esdl.return_value = expected_object
            # Act
            result = EsdlAssetPipeMapper._get_esdl_object_from_edr("DN100")
            # Assert
            mock_edr_client.get_object_esdl.assert_called_once_with(
                "/edr/Public/Assets/Logstor/Steel-S1-DN-100.edd"
            )
            self.assertEqual(result, expected_object)

    def test_get_diameter_with_specified_diameter_and_default_pipe_schedule(self):
        """Test that _get_diameter uses default schedule when none provided in ESDL asset."""
        # Arrange
        esdl_asset_mock = Mock()
        dn_mock = Mock()
        dn_mock.name = "DN50"

        def mock_get_property(key, default=None):
            if key == "innerDiameter":
                return 0
            if key == "diameter":
                return dn_mock
            return default

        esdl_asset_mock.get_property = mock_get_property
        edr_object_mock = Mock()
        edr_object_mock.innerDiameter = 0.08

        with patch.object(
            EsdlAssetPipeMapper, "_get_esdl_object_from_edr", return_value=edr_object_mock
        ) as mock_edr:
            # Act
            diameter = EsdlAssetPipeMapper._get_diameter(esdl_asset_mock)

            # Assert
            self.assertEqual(diameter, 0.08)
            mock_edr.assert_called_once_with("DN50", PipeSchedules.S1)

    def test_get_esdl_object_from_edr_with_schedule_specified(self):
        """Test for when a schedule is filled in."""
        # Arrange
        with patch(
            "omotes_simulator_core.adapter.transforms.esdl_asset_mappers.pipe_mapper.EDRClient"
        ) as mock_edr_client_class:
            mock_edr_client = mock_edr_client_class.return_value
            expected_object = Mock()
            mock_edr_client.get_object_esdl.return_value = expected_object

            # Act
            result = EsdlAssetPipeMapper._get_esdl_object_from_edr("DN100", PipeSchedules.S3)

            # Assert
            mock_edr_client.get_object_esdl.assert_called_once_with(
                "/edr/Public/Assets/Logstor/Steel-S3-DN-100.edd"
            )
            self.assertEqual(result, expected_object)

    def test_get_diameter_with_invalid_schedule_raises_runtime_error(self):
        """Test that _get_diameter raises RuntimeError for invalid schedule values."""
        # Arrange
        esdl_asset_mock = Mock()

        def mock_get_property(key, default=None):
            if key == "innerDiameter":
                return 0
            if key == "diameter":
                return None
            if key == "schedule":
                return 999  # Invalid schedule value
            return default

        esdl_asset_mock.get_property = mock_get_property

        # Act & Assert
        with self.assertRaises(RuntimeError) as context:
            EsdlAssetPipeMapper._get_diameter(esdl_asset_mock)

        self.assertIn("Failed to retrieve ESDL object for schedule '999'", str(context.exception))
