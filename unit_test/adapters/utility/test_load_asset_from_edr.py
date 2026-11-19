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

"""Test the load asset from EDR utility."""

import unittest
from unittest.mock import Mock, patch

from omotes_simulator_core.adapter.utility.load_asset_from_edr import get_diameter_from_edr
from omotes_simulator_core.entities.assets.asset_defaults import PipeSchedules

EDR_CLIENT_PATCH_TARGET = "omotes_simulator_core.adapter.utility.load_asset_from_edr.EDRClient"


class GetDiameterFromEdrTest(unittest.TestCase):
    """Tests for get_diameter_from_edr."""

    def test_get_diameter_from_edr_default_schedule(self) -> None:
        """Retrieves the inner diameter using the default schedule."""
        # Arrange
        with patch(EDR_CLIENT_PATCH_TARGET) as mock_edr_client_class:
            mock_edr_client = mock_edr_client_class.return_value
            mock_edr_client.get_object_esdl.return_value = Mock(innerDiameter=0.1071)

            # Act
            result = get_diameter_from_edr("DN100")

            # Assert
            mock_edr_client.get_object_esdl.assert_called_once_with(
                "/edr/Public/Assets/Logstor/Steel-S1-DN-100.edd"
            )
            self.assertEqual(result, 0.1071)

    def test_get_diameter_from_edr_with_schedule_specified(self) -> None:
        """Retrieves the inner diameter using the given schedule."""
        # Arrange
        with patch(EDR_CLIENT_PATCH_TARGET) as mock_edr_client_class:
            mock_edr_client = mock_edr_client_class.return_value
            mock_edr_client.get_object_esdl.return_value = Mock(innerDiameter=0.1071)

            # Act
            result = get_diameter_from_edr("DN100", PipeSchedules.S3)

            # Assert
            mock_edr_client.get_object_esdl.assert_called_once_with(
                "/edr/Public/Assets/Logstor/Steel-S3-DN-100.edd"
            )
            self.assertEqual(result, 0.1071)

    def test_get_diameter_from_edr_raises_runtime_error(self) -> None:
        """Wraps errors from the EDR client in a RuntimeError."""
        # Arrange
        with patch(EDR_CLIENT_PATCH_TARGET) as mock_edr_client_class:
            mock_edr_client_class.return_value.get_object_esdl.side_effect = Exception("down")

            # Act / Assert
            with self.assertRaises(RuntimeError):
                get_diameter_from_edr("DN100")
