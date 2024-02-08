

class ControllerConsumer:
    """Class to store the consumer for the controller."""
    def __init__(self, name, identifier):
        """Constructor for the consumer."""
        self.name = name
        self.id = identifier
        self.temperature_return = 40 + 273.15
        self.temperature_supply = 80 + 273.15

    def get_heat_demand(self, time) -> float:
        """Method to get the heat demand of the consumer."""
        return 5000000 * time / 3600.0


class ControllerSource:
    """Class to store the source for the controller."""
    def __init__(self, name, identifier):
        """Constructor for the source."""
        self.name = name
        self.id = identifier
        self.temperature_return = 40 + 273.15
        self.temperature_supply = 80 + 273.15
        self.power = 5000000000

