class HeatNetwork:
    def __init__(self):
        pass

    def run_timestep(self, time: float, controller_input: dict):
        """Method to simulate a time step

        :param float time: Timestep for which to simulate the model
        :param dict controller_input: Dict specifying the heat demand for the different assets.
        :return: None
        """
        pass

    def store_output(self):
        """Method to store the output data

        This method takes the data from the pandapipes dataframe and stores it into our own dataframe. This is needed
        since we have the possibility to redo a timestep when results are not converged for the input of the controller.
        :return: None
        """
