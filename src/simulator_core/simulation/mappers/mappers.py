from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# what is this?
Entity = TypeVar("Entity")
EsdlAsset = TypeVar("EsdlAsset")


class EsdlMapperAbstract(ABC, Generic[Entity, EsdlAsset]):
    #Abstract class to be used for deriving mapper classes from esdl to our own classes.
    @abstractmethod
    def to_esdl(self, entity: Entity) -> EsdlAsset:
        """Map an Entity to a EsdlAsset"""

    @abstractmethod
    def to_entity(self, model: EsdlAsset) -> Entity:
        """Map am esdl asset  to an Entity"""



