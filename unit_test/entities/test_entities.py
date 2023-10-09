import simulator_core.entities.heat_network
from simulator_core.entities import HeatNetwork
import unittest


class HeatNetworkTest(unittest.TestCase):
    def test_heat_network(self) -> None:
        # Arrange

        # Act
        result = HeatNetwork()

        # Assert
        assert isinstance(result, simulator_core.entities.heat_network.HeatNetwork)
