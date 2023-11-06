import esdl

from simulator_core.entities.esdl_object import EsdlObject, EsdlAssetObject
from simulator_core.adapter.transforms.mappers import StringEsdlAssetMapper
from simulator_core.infrastructure.utils import pyesdl_from_file
import unittest
from simulator_core.entities.assets import AssetAbstract, DemandCluster, ProductionCluster, Pipe


class EsdlObjectTest(unittest.TestCase):

    def setUp(self):
        esdl_file_path = r'.\..\..\testdata\test1.esdl'
        self.esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))

    def test_get_all_assets_of_type(self):
        # Arrange
        producer = 'producer'
        consumer = 'consumer'
        pipe = 'pipe'
        # Act
        producers = self.esdl_object.get_all_assets_of_type(producer)
        consumers = self.esdl_object.get_all_assets_of_type(consumer)
        pipes = self.esdl_object.get_all_assets_of_type(pipe)

        # Assert
        self.assertEqual(len(producers), 1)
        self.assertEqual(len(consumers), 1)
        self.assertEqual(len(pipes), 2)

    def test_EsdlAssetObject(self):
        # Arrange
        producer = 'producer'
        consumer = 'consumer'
        pipe = 'pipe'
        producers = self.esdl_object.get_all_assets_of_type(producer)
        consumers = self.esdl_object.get_all_assets_of_type(consumer)
        pipes = self.esdl_object.get_all_assets_of_type(pipe)
        # Act
        asset_producer = producers[0].convert_esdl()
        asset_consumer = consumers[0].convert_esdl()
        asset_pipe = pipes[0].convert_esdl()
        # Assert
        self.assertTrue(isinstance(asset_producer, ProductionCluster))
        self.assertTrue(isinstance(asset_consumer, DemandCluster))
        self.assertTrue(isinstance(asset_pipe, Pipe))


class StringEsdlAssetMapperTest(unittest.TestCase):

    def setUp(self) -> None:
        self.asset = esdl.Asset
        self.producer = esdl.Producer
        self.consumer = esdl.Consumer
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
        # Arrange
        # Act
        asset_str = StringEsdlAssetMapper().to_entity(self.asset)
        producer_str = StringEsdlAssetMapper().to_entity(self.producer)
        consumer_str = StringEsdlAssetMapper().to_entity(self.consumer)
        geothermal_source_str = StringEsdlAssetMapper().to_entity(self.geothermal_source)
        conversion_str = StringEsdlAssetMapper().to_entity(self.conversion)
        pipe_str = StringEsdlAssetMapper().to_entity(self.pipe)
        transport_str = StringEsdlAssetMapper().to_entity(self.transport)
        joint_str = StringEsdlAssetMapper().to_entity(self.joint)
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
        # Arrange
        # Act
        asset = StringEsdlAssetMapper().to_esdl(self.asset_str)
        producer = StringEsdlAssetMapper().to_esdl(self.producer_str)
        consumer = StringEsdlAssetMapper().to_esdl(self.consumer_str)
        conversion = StringEsdlAssetMapper().to_esdl(self.conversion_str)
        pipe = StringEsdlAssetMapper().to_esdl(self.pipe_str)
        transport = StringEsdlAssetMapper().to_esdl(self.transport_str)
        joint = StringEsdlAssetMapper().to_esdl(self.joint_str)
        geothermal = StringEsdlAssetMapper().to_esdl(self.geothermal_source_str)
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
        # Arrange
        test_string = "nothing"
        test_esdl_asset = esdl.WindTurbine
        # Act
        # Assert
        with self.assertRaises(NotImplementedError):
            StringEsdlAssetMapper().to_esdl(test_string)
        with self.assertRaises(NotImplementedError):
            StringEsdlAssetMapper().to_entity(test_esdl_asset)
