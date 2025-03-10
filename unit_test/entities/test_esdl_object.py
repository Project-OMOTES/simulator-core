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

"""Test esdl object class."""
import unittest
from pathlib import Path

import esdl

from omotes_simulator_core.adapter.transforms.esdl_asset_mapper import EsdlAssetMapper
from omotes_simulator_core.adapter.transforms.string_to_esdl import (
    StringEsdlAssetMapper,
)
from omotes_simulator_core.entities.assets.demand_cluster import DemandCluster
from omotes_simulator_core.entities.assets.pipe import Pipe
from omotes_simulator_core.entities.assets.production_cluster import ProductionCluster
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file


class EsdlObjectTest(unittest.TestCase):
    """Test class for ESDL objects class."""

    def setUp(self):
        """Arranging standard objects for the other test."""
        esdl_file_path = Path(__file__).parent / ".." / ".." / "testdata" / "test1.esdl"
        esdl_file_path = str(esdl_file_path)
        self.esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))

    def test_get_all_assets_of_type(self):
        """Test to get a list of all assets of a certain type."""
        # Arrange
        producer = "producer"
        consumer = "consumer"
        pipe = "pipe"

        # Act
        producers = self.esdl_object.get_all_assets_of_type(producer)
        consumers = self.esdl_object.get_all_assets_of_type(consumer)

        pipes = self.esdl_object.get_all_assets_of_type(pipe)  # act

        # Assert
        self.assertEqual(len(producers), 1)
        self.assertEqual(len(consumers), 1)
        self.assertEqual(len(pipes), 2)

    def test_creation_of_esdl_asset_objects(self):
        """Test for creation of objects."""
        # Arrange
        producer = "producer"
        consumer = "consumer"
        pipe = "pipe"
        producers = self.esdl_object.get_all_assets_of_type(producer)
        consumers = self.esdl_object.get_all_assets_of_type(consumer)
        pipes = self.esdl_object.get_all_assets_of_type(pipe)

        # Act
        asset_producer = EsdlAssetMapper.to_entity(producers[0])
        asset_consumer = EsdlAssetMapper.to_entity(consumers[0])

        asset_pipe = EsdlAssetMapper.to_entity(pipes[0])  # act

        # Assert
        self.assertTrue(isinstance(asset_producer, ProductionCluster))
        self.assertTrue(isinstance(asset_consumer, DemandCluster))
        self.assertTrue(isinstance(asset_pipe, Pipe))

    def test_get_connected_assets(self):
        """Test for connection of two assets."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("producer")[0].esdl_asset
        pipes = self.esdl_object.get_all_assets_of_type("pipe")
        test_list1 = [(pipes[1].get_id(), pipes[1].get_port_ids()[1])]
        test_list2 = [(pipes[0].get_id(), pipes[0].get_port_ids()[0])]

        # Act
        connected_assets1 = self.esdl_object.get_connected_assets(asset.id, asset.port[1].id)

        connected_assets2 = self.esdl_object.get_connected_assets(asset.id, asset.port[0].id)  # act

        # Assert
        self.assertEqual(connected_assets1, test_list2)
        self.assertEqual(connected_assets2, test_list1)

    def test_get_property(self):
        """Test get_property method."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("pipe")[0]

        # Act
        length = asset.get_property("length", 0.0)  # act

        # Assert
        self.assertEqual(length, asset.esdl_asset.length)

    def test_get_property_not_found(self):
        """Test get_property when the property is not found."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("pipe")[0]

        # Act
        length = asset.get_property("length_not_found", 0.0)  # act

        # Assert
        self.assertEqual(length, 0.0)

    def test_get_port_ids(self):
        """Test get_port_ids method."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("pipe")[0]

        port_ids = asset.get_port_ids()  # act

        # Assert
        self.assertEqual(
            port_ids,
            ["a9793a5e-df4f-4795-8079-015dfaf57f82", "3f2dc09a-0cee-44bd-a337-cea55461a334"],
        )
        self.assertEqual(len(port_ids), 2)

    def test_get_supply_temperature_in(self):
        """Test get_supply_temperature method."""
        asset = self.esdl_object.get_all_assets_of_type("pipe")[0]
        # Act
        supply_temperature = asset.get_supply_temperature("In")

        # Assert
        self.assertEqual(supply_temperature, 353.15)

    def test_get_supply_temperature_out(self):
        """Test get_supply_temperature method."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("pipe")[0]

        # Act
        supply_temperature = asset.get_supply_temperature("Out")

        # Assert
        self.assertEqual(supply_temperature, 353.15)

    def test_get_return_temperature_in(self):
        """Test get_return_temperature method."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("pipe")[1]

        # Act
        return_temperature = asset.get_return_temperature("In")

        # Assert
        self.assertEqual(return_temperature, 313.15)

    def test_get_return_temperature_out(self):
        """Test get_return_temperature method."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("pipe")[1]

        # Act
        return_temperature = asset.get_return_temperature("Out")

        # Assert
        self.assertEqual(return_temperature, 313.15)

    def test_get_supply_temperature_consumer(self):
        """Test get_supply_temperature method."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("consumer")[0]

        # Act
        supply_temperature = asset.get_return_temperature("Out")

        # Assert
        self.assertEqual(supply_temperature, 313.15)

    def test_get_return_temperature_consumer(self):
        """Test get_supply_temperature method."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("consumer")[0]

        # Act
        supply_temperature = asset.get_supply_temperature("In")

        # Assert
        self.assertEqual(supply_temperature, 353.15)

    def test_get_supply_temperature_producer(self):
        """Test get_supply_temperature method."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("producer")[0]

        # Act
        supply_temperature = asset.get_supply_temperature("Out")

        # Assert
        self.assertEqual(supply_temperature, 353.15)

    def test_get_return_temperature_producer(self):
        """Test get_supply_temperature method."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("producer")[0]

        # Act
        supply_temperature = asset.get_return_temperature("In")

        # Assert
        self.assertEqual(supply_temperature, 313.15)

    def test_get_port_type_in(self):
        """Test get_port_type method."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("pipe")[0]

        # Act
        port_type = asset.get_port_type("In")

        # Assert
        self.assertEqual(port_type, esdl.InPort)

    def test_get_port_type_out(self):
        """Test get_port_type method."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("pipe")[0]

        # Act
        port_type = asset.get_port_type("Out")

        # Assert
        self.assertEqual(port_type, esdl.OutPort)

    def test_get_port_type_error(self):
        """Test get_port_type method."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("pipe")[0]

        # Act
        with self.assertRaises(ValueError) as cm:
            asset.get_port_type("Error")

        # assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            str(cm.exception),
            "Port type not recognized: Error",
        )

    def test_multiple_connection(self):
        """Test for multiple connections to one asset."""
        # Arrange
        esdl_file_path = (
            Path(__file__).parent / ".." / ".." / "testdata" / "test_multiple_connection.esdl"
        )
        esdl_file_path = str(esdl_file_path)
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        pipe = esdl_object.get_all_assets_of_type("pipe")[0]
        assets = esdl_object.get_all_assets_of_type("producer")
        test_list = [(asset.get_id(), asset.get_port_ids()[1]) for asset in assets]

        # Act
        connected_assets = esdl_object.get_connected_assets(pipe.get_id(), pipe.get_port_ids()[0])

        # Assert
        self.assertEqual(connected_assets, test_list)

    def test_no_connected_assets_error(self):
        """Test for error when no connected assets are found."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("producer")[0]
        pipe = self.esdl_object.get_all_assets_of_type("pipe")[0]

        # Act
        with self.assertRaises(ValueError) as cm:
            self.esdl_object.get_connected_assets(asset.get_id(), pipe.get_port_ids()[0])

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            str(cm.exception),
            f"No connected assets found for asset: {asset.get_id()} and "
            f"port: {pipe.get_port_ids()[0]}",
        )

    def test_get_asset_by_id(self):
        # Arrange
        producers = self.esdl_object.get_all_assets_of_type("producer")
        producer = producers[0]

        # Act
        asset = self.esdl_object.get_asset_by_id(producer.get_id())

        # Assert
        self.assertEqual(asset.esdl_asset, producer.esdl_asset)


class StringEsdlAssetMapperTest(unittest.TestCase):
    """Class to test conversion from esdl asset to string and back."""

    def setUp(self) -> None:
        """Arranging of the data for the tests."""
        self.asset = esdl.Asset
        self.producer = esdl.Producer
        self.consumer = esdl.GenericConsumer
        self.geothermal_source = esdl.GeothermalSource
        self.conversion = esdl.Conversion
        self.pipe = esdl.Pipe
        self.transport = esdl.Transport
        self.joint = esdl.Joint
        self.heat_pump = esdl.HeatPump
        self.heat_exchange = esdl.HeatExchange
        self.asset_str = "asset"
        self.producer_str = "producer"
        self.consumer_str = "consumer"
        self.geothermal_source_str = "geothermal"
        self.conversion_str = "conversion"
        self.pipe_str = "pipe"
        self.transport_str = "transport"
        self.joint_str = "joint"
        self.heat_tranfer_str = "heat_transfer"

    def test_to_string(self):
        """Test for conversion from esdl asset to string."""
        # Arrange

        # Act
        asset_str = StringEsdlAssetMapper().to_entity(self.asset)
        producer_str = StringEsdlAssetMapper().to_entity(self.producer)
        consumer_str = StringEsdlAssetMapper().to_entity(self.consumer)
        geothermal_source_str = StringEsdlAssetMapper().to_entity(self.geothermal_source)
        conversion_str = StringEsdlAssetMapper().to_entity(self.conversion)
        pipe_str = StringEsdlAssetMapper().to_entity(self.pipe)
        transport_str = StringEsdlAssetMapper().to_entity(self.transport)
        heat_tranfer_str = StringEsdlAssetMapper().to_entity(self.heat_pump)
        heat_tranfer_str2 = StringEsdlAssetMapper().to_entity(self.heat_exchange)

        joint_str = StringEsdlAssetMapper().to_entity(self.joint)  # act

        # Assert
        self.assertTrue(asset_str == self.asset_str)
        self.assertTrue(producer_str == self.producer_str)
        self.assertTrue(consumer_str == self.consumer_str)
        self.assertTrue(geothermal_source_str == self.geothermal_source_str)
        self.assertTrue(conversion_str == self.conversion_str)
        self.assertTrue(pipe_str == self.pipe_str)
        self.assertTrue(transport_str == self.transport_str)
        self.assertTrue(joint_str == self.joint_str)
        self.assertTrue(heat_tranfer_str == self.heat_tranfer_str)
        self.assertTrue(heat_tranfer_str2 == self.heat_tranfer_str)

    def test_to_esdl(self):
        """Test for mapping back to esdl assets."""
        # Arrange

        # Act
        asset = StringEsdlAssetMapper().to_esdl(self.asset_str)[0]
        producer = StringEsdlAssetMapper().to_esdl(self.producer_str)[0]
        consumer = StringEsdlAssetMapper().to_esdl(self.consumer_str)[0]
        conversion = StringEsdlAssetMapper().to_esdl(self.conversion_str)[0]
        pipe = StringEsdlAssetMapper().to_esdl(self.pipe_str)[0]
        transport = StringEsdlAssetMapper().to_esdl(self.transport_str)[0]
        joint = StringEsdlAssetMapper().to_esdl(self.joint_str)[0]
        heat_transfer = StringEsdlAssetMapper().to_esdl(self.heat_tranfer_str)[0]
        heat_transfer2 = StringEsdlAssetMapper().to_esdl(self.heat_tranfer_str)[1]

        geothermal = StringEsdlAssetMapper().to_esdl(self.geothermal_source_str)[0]  # act

        # Assert
        self.assertTrue(asset == self.asset)
        self.assertTrue(producer == self.producer)
        self.assertTrue(consumer == self.consumer)
        self.assertTrue(conversion == self.conversion)
        self.assertTrue(pipe == self.pipe)
        self.assertTrue(transport == self.transport)
        self.assertTrue(joint == self.joint)
        self.assertTrue(geothermal == self.geothermal_source)
        self.assertTrue(heat_transfer == self.heat_pump)
        self.assertTrue(heat_transfer2 == self.heat_exchange)

    def test_raise_error(self):
        """Test to test if an error is raised for unknown component in ESDL."""
        # Arrange
        test_string = "nothing"
        test_esdl_asset = esdl.WindTurbine
        # Act

        # Assert
        with self.assertRaises(NotImplementedError):
            StringEsdlAssetMapper().to_esdl(test_string)  # act

        with self.assertRaises(NotImplementedError):
            StringEsdlAssetMapper().to_entity(test_esdl_asset)  # act
