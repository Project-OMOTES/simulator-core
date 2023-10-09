from abc import ABC, abstractmethod
from typing import Dict

from pandas import DataFrame


class AssetAbstract(ABC):
    """Abstract class for Asset"""

    @abstractmethod
    def set(self, **kwargs) -> None:
        """Placeholder to set attributes of an asset"""
        pass

    @abstractmethod
    def get(self, **kwargs) -> Dict:
        """Placeholder to get attributes of an asset"""
        pass

    @abstractmethod
    def register_pandapipes(self) -> None:
        """Placeholder to register asset in a pandapipes network"""
        pass

    @abstractmethod
    def get_timeseries(self) -> DataFrame:
        """Get timeseries as a dataframe from a pandapipes asset"""
        pass
