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
from omotes_simulator_core.adapter.transforms.transform_utils import (
    sort_ports,
    reverse_dict,
    PortType,
)


class TransformUtilsTest(unittest.TestCase):
    """Class to test the transform utils functions."""

    def test_sort_ports_basic(self):
        """Test the port sorting function. THe order is nto changed."""
        # act
        connected_ports = [("port1", PortType.IN), ("port2", PortType.OUT)]

        # arrange
        result = sort_ports(connected_ports)

        # assert
        self.assertEqual(result, ["port1", "port2"])

    def test_sort_ports_reverse(self):
        """Test the port sorting function. The order is reversed."""
        # act
        connected_ports = [("port2", PortType.OUT), ("port1", PortType.IN)]

        # arrange
        result = sort_ports(connected_ports)

        # assert
        self.assertEqual(result, ["port1", "port2"])

    def test_sort_ports_4_ports(self):
        """Test the port sorting function with 4 ports, the order remains the same."""
        # act
        connected_ports = [
            ("port1", PortType.IN),
            ("port2", PortType.OUT),
            ("port3", PortType.IN),
            ("port4", PortType.OUT),
        ]

        # arrange
        result = sort_ports(connected_ports)

        # assert
        self.assertEqual(result, ["port1", "port2", "port3", "port4"])

    def test_sort_ports_4_ports_reverse(self):
        """Test the port sorting function with 4 ports, the order is reversed."""
        # act
        connected_ports = [
            ("port4", PortType.OUT),
            ("port3", PortType.IN),
            ("port1", PortType.IN),
            ("port2", PortType.OUT),
        ]

        # arrange
        result = sort_ports(connected_ports)

        # assert
        self.assertEqual(result, ["port3", "port4", "port1", "port2"])

    def test_sort_port_errror_number_of_ports(self):
        """Test the port sorting function.

        This test has different number of in and out port resulting in error.
        """
        # act
        connected_ports = [("port1", PortType.IN), ("port2", PortType.OUT), ("port3", PortType.IN)]

        # arrange
        with self.assertRaises(ValueError) as cm:
            sort_ports(connected_ports)

        # assert
        self.assertEqual(str(cm.exception), "The number of in ports and out ports are not equal")

    def test_reverse_dict(self):
        """Test the reverse dict function."""
        # act
        original_dict = {"key1": "value1", "key2": "value2", "key3": "value1"}

        # arrange
        result = reverse_dict(original_dict)

        # assert
        self.assertEqual(result, {"value1": ["key1", "key3"], "value2": ["key2"]})
