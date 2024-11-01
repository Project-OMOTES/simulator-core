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
    order_prim_sec_ports,
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
            ("Prim port1", PortType.IN),
            ("Prim port2", PortType.OUT),
            ("Sec port3", PortType.IN),
            ("Sec port4", PortType.OUT),
        ]

        # arrange
        result = sort_ports(connected_ports)

        # assert
        self.assertEqual(result, ["Prim port1", "Prim port2", "Sec port3", "Sec port4"])

    def test_sort_ports_4_ports_reverse(self):
        """Test the port sorting function with 4 ports, the order is reversed."""
        # act
        connected_ports = [
            ("Sec port4", PortType.OUT),
            ("Sec port3", PortType.IN),
            ("Prim port1", PortType.IN),
            ("Prim port2", PortType.OUT),
        ]

        # arrange
        result = sort_ports(connected_ports)

        # assert
        self.assertEqual(result, ["Prim port1", "Prim port2", "Sec port3", "Sec port4"])

    def test_sort_port_error_number_of_ports(self):
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

    def test_order_prim_sec_ports(self):
        """Test the order primary secondary ports function."""
        # act
        connected_ports = ["Prim port1", "Prim port2", "Sec port3", "Sec port4"]

        # arrange
        result = order_prim_sec_ports(connected_ports)

        # assert
        self.assertEqual(result, ["Prim port1", "Prim port2", "Sec port3", "Sec port4"])

    def test_order_prim_sec_ports_error_prim(self):
        """Test the order primary secondary ports function.

        This test has different number of primary ports resulting in error.
        """
        # act
        connected_ports = ["Prim port1", "Prim port2", "Prim port3", "Sec port4"]

        # arrange
        with self.assertRaises(ValueError) as cm:
            order_prim_sec_ports(connected_ports)

        # assert
        self.assertEqual(
            str(cm.exception), "The number of ports with prim in the name is not equal to 2"
        )

    def test_order_prim_sec_ports_error_sec(self):
        """Test the order primary secondary ports function.

        This test has different number of secondary ports resulting in error.
        """
        # act
        connected_ports = ["Prim port1", "Prim port2", "Sec port3", "Sec port4", "Sec port5"]

        # arrange
        with self.assertRaises(ValueError) as cm:
            order_prim_sec_ports(connected_ports)

        # assert
        self.assertEqual(
            str(cm.exception), "The number of ports with sec in the name is not equal to 2"
        )

    def test_order_prim_sec_ports_reversed(self):
        """Test the order primary secondary ports function.

        This test has the order reversed.
        """
        # act
        connected_ports = ["Sec port4", "Sec port3", "Prim port2", "Prim port1"]

        # arrange
        result = order_prim_sec_ports(connected_ports)

        # assert
        self.assertEqual(result, ["Prim port2", "Prim port1", "Sec port4", "Sec port3"])

    def test_reverse_dict(self):
        """Test the reverse dict function."""
        # act
        original_dict = {"key1": "value1", "key2": "value2", "key3": "value1"}

        # arrange
        result = reverse_dict(original_dict)

        # assert
        self.assertEqual(result, {"value1": ["key1", "key3"], "value2": ["key2"]})
