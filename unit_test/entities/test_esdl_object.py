from simulator_core.entities.esdl_object import EsdlObject
from simulator_core.infrastructure.utils import pyesdl_from_file
import unittest


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
        self.assertEqual(len(producers),1)
        self.assertEqual(len(consumers),1)
        self.assertEqual(len(pipes),2)
