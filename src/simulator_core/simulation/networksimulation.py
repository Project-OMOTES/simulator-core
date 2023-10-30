import numpy as np
from simulator_core.entities import HeatNetwork, NetworkController, SimulationConfiguration
import logging

logger = logging.getLogger(__name__)

class NetworkSimulation:
    """Network simulation class

    Class which can be used to run a simulation. It holds a network object containing the information on the assets
    and an object with information on the controller. The simulation can be run with the run method passing a
    config object.
    """

    def __init__(self, network: HeatNetwork, controller: NetworkController):
        """Constructor of NetworkSimulation class

        Constructor of NetworkSimulation. This can be used to simulate a network for a certain period of time

        :param HeatNetwork network: Object containing all the info on the network
        :param controller: Object containing information on how the network should be controlled
        """
        self.config = None
        self.network = network
        self.controller = controller

    def run(self, config: SimulationConfiguration):
        """Method to run the simulation

        Runs the simulation based on the given config object, which contains info on the timestep and length.
        :param SimulationConfiguration config: SimulationConfig object containing info on a.o. the time step
        and duration
        :return: None
        """
        self.config = config # Why do we store it in here?

        # time loop
        for time in np.arange(self.config.start, self.config.stop, self.config.timestep):
            not_converged = True
            while not_converged:
                not_converged = False # for the moment we do not check on convergence, to get stuff running.
                # Also need to add break after 10 iteration.
                logger.debug("Simulating for timestep " + str(time))
                controller_input = self.controller.run_time_step(time)
                self.network.run_time_step(time, controller_input)
            self.network.store_output()




