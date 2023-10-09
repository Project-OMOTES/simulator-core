from abc import ABC, abstractmethod


class AssetAbstract(ABC):

    @abstractmethod
    def register_pp(self):
        pass

    @abstractmethod
    def get_timeseries(self):
        pass
