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

"""Module containing the abstract class for the mappers."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Entity = TypeVar("Entity")
EsdlAssetObject = TypeVar("EsdlAssetObject")


class EsdlMapperAbstract(ABC, Generic[Entity, EsdlAssetObject]):
    """Abstract class to be used for deriving mapper classes from esdl to our own classes."""

    @abstractmethod
    def to_esdl(self, entity: Entity) -> EsdlAssetObject:
        """Map an Entity to a EsdlAsset."""

    @abstractmethod
    def to_entity(self, model: EsdlAssetObject) -> Entity:
        """Map an esdl asset  to an Entity."""
