from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Entity = TypeVar("Entity")
EsdlAsset = TypeVar("EsdlAsset")


class EsdlMapperAbstract(ABC, Generic[Entity, EsdlAsset]):
    @abstractmethod
    def to_esdl(self, entity: Entity) -> EsdlAsset:
        """Map an Entity to a EsdlAsset"""

    @abstractmethod
    def to_entity(self, model: EsdlAsset) -> Entity:
        """Map am esdl asset  to an Entity"""
