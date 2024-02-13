"""Module containing the classes for the controller."""
import datetime

import pandas as pd


class AssetControllerAbstract:
    """Abstract class for the asset controller."""

    def __init__(self, name: str, identifier: str):
        """Constructor for the asset controller.

        :param str name: Name of the controller object.
        :param str identifier: Unique identifier of the controller asset.
        """
        self.name = name
        self.id = identifier


class ControllerConsumer(AssetControllerAbstract):
    """Class to store the consumer for the controller asset."""

    def __init__(self, name: str, identifier: str):
        """Constructor for the consumer.

        :param str name: Name of the consumer.
        :param str identifier: Unique identifier of the consumer.
        """
        super().__init__(name, identifier)
        self.temperature_return = 40 + 273.15
        self.temperature_supply = 80 + 273.15
        self.profile: pd.DataFrame = pd.DataFrame()

    def get_heat_demand(self, time: datetime.datetime) -> float:
        """Method to get the heat demand of the consumer.

        :param datetime.datetime time: Time for which to get the heat demand.
        :return: float with the heat demand.
        """
        for index in range(len(self.profile)):
            if abs((self.profile["date"][index].to_pydatetime() - time).total_seconds()) < 3600:
                return float(self.profile["values"][index])
        return 0

    def add_profile(self, profile: pd.DataFrame) -> None:
        """Method to add a profile to the consumer."""
        self.profile = profile


class ControllerSource(AssetControllerAbstract):
    """Class to store the source for the controller."""

    def __init__(self, name: str, identifier: str):
        """Constructor for the source.

        :param str name: Name of the source.
        :param str identifier: Unique identifier of the source.
        """
        super().__init__(name, identifier)
        self.temperature_return: float = 40 + 273.15
        self.temperature_supply: float = 80 + 273.15
        self.power: float = 5000000000
