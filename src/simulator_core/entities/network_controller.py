class NetworkController:
    def __init__(self):
        pass

    def run_time_step(self, time: float) -> dict:
        """ Method to get the controller inputs for the network

        :param float time: Time step for which to run the controller.
        :return: dict with the key the asset id and the heat demand for that asset.
        """
        # TODO add also the possibility to return mass flow rate instead of heat demand.
        pass
