from simulator_core.entities import EsdlObject, SimulationConfiguration
from simulator_core.adapter.transforms import EsdlEnergySystemMapper, EsdlControllerMapper
from simulator_core.simulation import NetworkSimulation
import pandas as pd
import numpy as np


class SimulationManager:
    def __init__(self, esdl: EsdlObject, config: SimulationConfiguration):
        self.esdl = esdl
        self.config = config

    def execute(self):
        # convert ESDL to Heat Network, NetworkController

        network = EsdlEnergySystemMapper().to_entity(self.esdl.es)
        controller = EsdlControllerMapper().to_entity(self.esdl.es)

        worker = NetworkSimulation(network, controller)
        worker.run(self.config)

        # Run output presenter that iterates over het network (/controller?) and
        # gathers the output into a single data object

        # return dataframe.
        return pd.DataFrame(
            np.random.randn(10, 3),
            index=pd.date_range("1/1/2001", periods=10, freq="H"),
            columns=['DEMO flowrate', 'DEMO Pressure', 'DEMO Temperature'],
        )
