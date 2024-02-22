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

from simulator_core.adapter.transforms.esdl_asset_mapper import EsdlAssetMapper
from simulator_core.adapter.transforms.string_to_esdl import StringEsdlAssetMapper
from simulator_core.entities.assets.demand_cluster import DemandCluster
from simulator_core.entities.assets.pipe import Pipe
from simulator_core.entities.assets.production_cluster import ProductionCluster
from simulator_core.entities.assets.utils import Port
from simulator_core.entities.esdl_object import EsdlObject
from simulator_core.infrastructure.utils import pyesdl_from_file


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
        asset_producer = EsdlAssetMapper().to_entity(producers[0])
        asset_consumer = EsdlAssetMapper().to_entity(consumers[0])

        asset_pipe = EsdlAssetMapper().to_entity(pipes[0])  # act

        # Assert
        self.assertTrue(isinstance(asset_producer, ProductionCluster))
        self.assertTrue(isinstance(asset_consumer, DemandCluster))
        self.assertTrue(isinstance(asset_pipe, Pipe))

    def test_get_connected_assets(self):
        """Test for connection of two assets."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("producer")[0].esdl_asset
        test_list1 = [("Pipe1_ret", Port.Out)]
        test_list2 = [("Pipe1", Port.In)]

        # Act
        connected_assets1 = self.esdl_object.get_connected_assets(asset.id, Port.In)

        connected_assets2 = self.esdl_object.get_connected_assets(asset.id, Port.Out)  # act

        # Assert
        self.assertEqual(connected_assets1, test_list1)
        self.assertEqual(connected_assets2, test_list2)

    def test_get_property(self):
        """Test get_property method."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("pipe")[0]

        # Act
        length, property_available = asset.get_property("length", 0.0)  # act

        # Assert
        assert length == asset.esdl_asset.length
        assert property_available

    def test_get_property_not_found(self):
        """Test get_property when the property is not found."""
        # Arrange
        asset = self.esdl_object.get_all_assets_of_type("pipe")[0]

        # Act
        length, property_available = asset.get_property("length_not_found", 0.0)  # act

        # Assert
        assert length == 0.0
        assert property_available is False


class StringEsdlAssetMapperTest(unittest.TestCase):
    """Class to test conversion from esdl asset to string and back."""

    def setUp(self) -> None:
        """Arranging of the data for the tests."""
        self.asset = esdl.Asset
        self.producer = esdl.GenericProducer
        self.consumer = esdl.GenericConsumer
        self.geothermal_source = esdl.GeothermalSource
        self.conversion = esdl.Conversion
        self.pipe = esdl.Pipe
        self.transport = esdl.Transport
        self.joint = esdl.Joint
        self.asset_str = "asset"
        self.producer_str = "producer"
        self.consumer_str = "consumer"
        self.geothermal_source_str = "geothermal"
        self.conversion_str = "conversion"
        self.pipe_str = "pipe"
        self.transport_str = "transport"
        self.joint_str = "junction"

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
