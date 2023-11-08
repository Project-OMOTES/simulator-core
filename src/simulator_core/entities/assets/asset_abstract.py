from abc import ABC, abstractmethod
from typing import Any

from pandas import DataFrame


class AssetAbstract(ABC):
    """Abstract class for Asset"""

    @abstractmethod
    def set(self, **kwargs) -> None:
        """Placeholder to set attributes of an asset"""
        pass

    @abstractmethod
    def get(self, **kwargs) -> Any:
        """Placeholder to get attributes of an asset"""
        pass

    @abstractmethod
    def register_pandapipes(self, **kwargs) -> None:
        """Placeholder to register asset in a pandapipes network"""
        pass

    @abstractmethod
    def get_timeseries(self, **kwargs) -> DataFrame:
        """Get timeseries as a dataframe from a pandapipes asset"""
        pass
