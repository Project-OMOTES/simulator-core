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
    Port,
)


class TransformUtilsTest(unittest.TestCase):
    """Class to test the transform utils functions."""

    def setUp(self) -> None:
        """Set up test case."""
        self.connected_ports = [
            Port(port_id="port1", port_name="Prim port1", port_type=PortType.IN),
            Port(port_id="port2", port_name="Prim port2", port_type=PortType.OUT),
        ]

    def test_sort_ports_basic(self):
        """Test the port sorting function. THe order is nto changed."""
        # arrange

        # act
        result = sort_ports(self.connected_ports)

        # assert
        self.assertEqual(result, [port.port_id for port in self.connected_ports])

    def test_sort_ports_reverse(self):
        """Test the port sorting function. The order is reversed."""
        # arrange
        connected_ports = self.connected_ports[::-1]

        # act
        result = sort_ports(connected_ports)

        # assert
        self.assertEqual(result, [port.port_id for port in self.connected_ports])

    def test_sort_ports_4_ports(self):
        """Test the port sorting function with 4 ports, the order remains the same."""
        # arrange
        self.connected_ports.append(
            Port(port_id="port3", port_name="Sec port3", port_type=PortType.IN)
        )
        self.connected_ports.append(
            Port(port_id="port4", port_name="Sec port4", port_type=PortType.OUT)
        )
        # act
        result = sort_ports(self.connected_ports)

        # assert
        self.assertEqual(result, [port.port_id for port in self.connected_ports])

    def test_sort_ports_4_ports_reverse(self):
        """Test the port sorting function with 4 ports, the order is reversed."""
        # arrange
        self.connected_ports.append(
            Port(port_id="port3", port_name="Sec port3", port_type=PortType.IN)
        )
        self.connected_ports.append(
            Port(port_id="port4", port_name="Sec port4", port_type=PortType.OUT)
        )
        connected_ports = self.connected_ports[::-1]

        # act
        result = sort_ports(connected_ports)

        # assert
        self.assertEqual(result, [port.port_id for port in self.connected_ports])

    def test_sort_port_error_number_of_ports(self):
        """Test the port sorting function.

        This test has different number of in and out port resulting in error.
        """
        # arrange
        self.connected_ports.append(
            Port(port_id="port3", port_name="Sec port3", port_type=PortType.IN)
        )

        # act
        with self.assertRaises(ValueError) as cm:
            sort_ports(self.connected_ports)

        # assert
        self.assertEqual(str(cm.exception), "The number of in ports and out ports are not equal")

    def test_order_prim_sec_ports(self):
        """Test the order primary secondary ports function."""
        # arrange
        self.connected_ports.append(
            Port(port_id="port3", port_name="Sec port3", port_type=PortType.IN)
        )
        self.connected_ports.append(
            Port(port_id="port4", port_name="Sec port4", port_type=PortType.OUT)
        )

        # act
        result = order_prim_sec_ports(self.connected_ports)

        # assert
        self.assertEqual(result, self.connected_ports)

    def test_order_prim_sec_ports_error_prim(self):
        """Test the order primary secondary ports function.

        This test has different number of primary ports resulting in error.
        """
        # arrange
        self.connected_ports.append(
            Port(port_id="port3", port_name="Prim port3", port_type=PortType.IN)
        )
        self.connected_ports.append(
            Port(port_id="port4", port_name="Sec port4", port_type=PortType.OUT)
        )

        # act
        with self.assertRaises(ValueError) as cm:
            order_prim_sec_ports(self.connected_ports)

        # assert
        self.assertEqual(
            str(cm.exception), "The number of ports with prim in the name is not equal to 2"
        )

    def test_order_prim_sec_ports_error_sec(self):
        """Test the order primary secondary ports function.

        This test has different number of secondary ports resulting in error.
        """
        # arrange
        self.connected_ports.append(
            Port(port_id="port3", port_name="Sec port3", port_type=PortType.IN)
        )
        self.connected_ports.append(
            Port(port_id="port4", port_name="Sec port4", port_type=PortType.OUT)
        )
        self.connected_ports.append(
            Port(port_id="port5", port_name="Sec port5", port_type=PortType.OUT)
        )

        # act
        with self.assertRaises(ValueError) as cm:
            order_prim_sec_ports(self.connected_ports)

        # assert
        self.assertEqual(
            str(cm.exception), "The number of ports with sec in the name is not equal to 2"
        )

    def test_order_prim_sec_ports_reversed(self):
        """Test the order primary secondary ports function.

        This test has the order reversed.
        """
        # arrange
        self.connected_ports.insert(
            0, Port(port_id="port4", port_name="Sec port4", port_type=PortType.OUT)
        )
        self.connected_ports.insert(
            0, Port(port_id="port3", port_name="Sec port3", port_type=PortType.IN)
        )
        # act
        result = order_prim_sec_ports(self.connected_ports)

        # assert
        self.assertEqual(result[0], self.connected_ports[2])
        self.assertEqual(result[1], self.connected_ports[3])
        self.assertEqual(result[2], self.connected_ports[0])
        self.assertEqual(result[3], self.connected_ports[1])

    def test_reverse_dict(self):
        """Test the reverse dict function."""
        # arrange
        original_dict = {"key1": "value1", "key2": "value2", "key3": "value1"}

        # act
        result = reverse_dict(original_dict)

        # assert
        self.assertEqual(result, {"value1": ["key1", "key3"], "value2": ["key2"]})
