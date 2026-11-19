#  Copyright (c) 2026. Deltares & TNO
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

"""Test the EsdlAssetObject class."""

import unittest
from unittest.mock import patch

import esdl

from omotes_simulator_core.entities.assets.asset_defaults import PIPE_DEFAULTS, PipeSchedules
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject

EDR_PATCH_TARGET = "omotes_simulator_core.entities.assets.esdl_asset_object.get_diameter_from_edr"


class EsdlAssetObjectGetDiameterTest(unittest.TestCase):
    """Tests for EsdlAssetObject.get_diameter."""

    def test_get_diameter_with_inner_diameter(self) -> None:
        """Returns the innerDiameter if it is specified and non-zero."""
        # Arrange
        esdl_asset = EsdlAssetObject(
            esdl.Pipe(
                id="pipe", name="pipe", innerDiameter=0.5, diameter=esdl.PipeDiameterEnum.DN50
            )
        )

        # Act
        with patch(EDR_PATCH_TARGET) as mock_edr:
            diameter = esdl_asset.get_diameter()

        # Assert
        self.assertEqual(diameter, 0.5)
        mock_edr.assert_not_called()

    def test_get_diameter_with_nominal_diameter_uses_edr(self) -> None:
        """Returns diameter from EDR with default schedule when only DN is provided."""
        # Arrange
        esdl_asset = EsdlAssetObject(
            esdl.Pipe(id="pipe", name="pipe", diameter=esdl.PipeDiameterEnum.DN50)
        )

        # Act
        with patch(EDR_PATCH_TARGET, return_value=0.42) as mock_edr:
            diameter = esdl_asset.get_diameter()

        # Assert
        self.assertEqual(diameter, 0.42)
        mock_edr.assert_called_once_with("DN50", PipeSchedules.S1)

    def test_get_diameter_with_inner_diameter_zero_uses_edr(self) -> None:
        """Falls back to EDR when innerDiameter is set to 0 but a DN diameter is provided."""
        # Arrange
        esdl_asset = EsdlAssetObject(
            esdl.Pipe(
                id="pipe", name="pipe", innerDiameter=0.0, diameter=esdl.PipeDiameterEnum.DN125
            )
        )

        # Act
        with patch(EDR_PATCH_TARGET, return_value=0.1273) as mock_edr:
            diameter = esdl_asset.get_diameter()

        # Assert
        self.assertEqual(diameter, 0.1273)
        mock_edr.assert_called_once_with("DN125", PipeSchedules.S1)

    def test_get_diameter_default_when_none_provided(self) -> None:
        """Returns default diameter when innerDiameter and DN diameter are not provided."""
        # Arrange
        esdl_asset = EsdlAssetObject(esdl.Pipe(id="pipe", name="pipe"))

        # Act
        with patch(EDR_PATCH_TARGET) as mock_edr:
            diameter = esdl_asset.get_diameter()

        # Assert
        self.assertEqual(diameter, PIPE_DEFAULTS.diameter)
        mock_edr.assert_not_called()

    def test_get_diameter_raises_for_asset_without_diameter(self) -> None:
        """Raises a ValueError for assets that have no inner diameter attribute."""
        # Arrange
        esdl_asset = EsdlAssetObject(esdl.HeatingDemand(id="demand", name="demand"))

        # Act / Assert
        with self.assertRaises(ValueError):
            esdl_asset.get_diameter()
