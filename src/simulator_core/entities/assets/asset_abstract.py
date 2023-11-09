#  Copyright (c) 2023. Deltares & TNO
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

""" Abstract class for asset. """

from abc import ABC, abstractmethod
from typing import Any

from pandas import DataFrame


class AssetAbstract(ABC):
    """Abstract class for Asset."""

    @abstractmethod
    def set(self, **kwargs) -> None:    
        """Placeholder to set attributes of an asset."""
        pass

    @abstractmethod
    def get(self, **kwargs) -> Any:
        """Placeholder to get attributes of an asset."""
        pass

    @abstractmethod
    def register_pandapipes(self, **kwargs) -> None:
        """Placeholder to register asset in a pandapipes network."""
        pass

    @abstractmethod
    def get_timeseries(self, **kwargs) -> DataFrame:
        """Get timeseries as a dataframe from a pandapipes asset."""
        pass
