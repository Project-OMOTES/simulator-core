import pandas as pd


class ControllerConsumer:
    """Class to store the consumer for the controller."""
    def __init__(self, name: str, identifier: str):
        """Constructor for the consumer."""
        self.name = name
        self.id = identifier
        self.temperature_return = 40 + 273.15
        self.temperature_supply = 80 + 273.15
        self.profile: pd.DataFrame | None = None

    def get_heat_demand(self, time: int) -> float:
        """Method to get the heat demand of the consumer."""
        return self.profile.loc[time, "values"]

    def add_profile(self, profile: pd.DataFrame) -> None:
        """Method to add a profile to the consumer."""
        self.profile = profile


class ControllerSource:
    """Class to store the source for the controller."""
    def __init__(self, name: str, identifier: str):
        """Constructor for the source."""
        self.name = name
        self.id = identifier
        self.temperature_return: float = 40 + 273.15
        self.temperature_supply: float = 80 + 273.15
        self.power: float = 5000000000

