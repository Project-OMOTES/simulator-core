#  Copyright (c) 2025. Deltares & TNO
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
from pathlib import Path
from unittest.mock import Mock

from omotes_simulator_core.adapter.transforms.controller_mapper import EsdlControllerMapper
from omotes_simulator_core.adapter.transforms.mappers import EsdlEnergySystemMapper
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.entities.heat_network import HeatNetwork
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file


class ControllerNetworkCouplingTest(unittest.TestCase):
    """Test class for controller network coupling."""

    def setUp(self) -> None:
        # Path to ESDL file and loading ESDL object
        self.esdl_file_path = Path(__file__).parent / ".." / ".." / "testdata" / "test1.esdl"
        self.esdl_object = EsdlObject(pyesdl_from_file(str(self.esdl_file_path)))
        # Simulation network and controller
        self.network = HeatNetwork(EsdlEnergySystemMapper(self.esdl_object).to_entity)
        # - Replace all assets with mocks to be able to test the coupling
        for index, asset in enumerate(self.network.assets):
            mock_asset = Mock(wraps=asset)
            mock_asset.asset_id = asset.asset_id
            self.network.assets[index] = mock_asset

        self.controller = EsdlControllerMapper().to_entity(self.esdl_object)
        # - Replace all controllers in each network with mocks to be able to test the coupling
        for _, network in enumerate(self.controller.networks):
            for index_producer, producer in enumerate(network.producers):
                mock_producer = Mock(wraps=producer)
                mock_producer.id = producer.id
                network.producers[index_producer] = mock_producer
            for index_consumer, consumer in enumerate(network.consumers):
                mock_consumer = Mock(wraps=consumer)
                mock_consumer.id = consumer.id
                network.consumers[index_consumer] = mock_consumer
            for index_storage, storage in enumerate(network.storages):
                mock_storage = Mock(wraps=storage)
                mock_storage.id = storage.id
                network.storages[index_storage] = mock_storage

    def test_update_network_state(self):
        """Test whether update_network_state calls set_state on all assets in the controller."""
        # Arrange

        # Act
        self.controller.update_network_state(heat_network=self.network)

        # Assert
        set_state_calls = 0
        number_of_assets = 0
        for sub_network in self.controller.networks:
            for producer in sub_network.producers:
                set_state_calls += producer.set_state.call_count  # type: ignore
                number_of_assets += 1
            for consumer in sub_network.consumers:
                set_state_calls += consumer.set_state.call_count  # type: ignore
                number_of_assets += 1
            for storage in sub_network.storages:
                set_state_calls += storage.set_state.call_count  # type: ignore
                number_of_assets += 1

        self.assertEqual(set_state_calls, number_of_assets)
