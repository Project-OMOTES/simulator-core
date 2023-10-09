from simulator_core.entities import HeatNetwork, NetworkController, SimulationConfiguration


class NetworkSimulation:
    def __init__(self, network: HeatNetwork, controller: NetworkController):
        self.config = None
        self.network = network
        self.controller = controller

    def run(self, config: SimulationConfiguration):
        self.config = config
