from simulator_core.entities import HeatNetwork, NetworkController, SimulationConfiguration


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
        self.config = config# we do we store this here?

        # time loop
        
