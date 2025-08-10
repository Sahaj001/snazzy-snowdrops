from abc import ABC, abstractmethod

from engine import mouse
from engine.interfaces import Behaviour, Object
from models.position import Pos


class Entity(Object, ABC):
    """Base class for all game entities."""

    def __init__(
        self,
        entity_id: str,
        pos: Pos,
        behaviour: Behaviour | None = None,
    ) -> None:
        """Initialize the entity with an ID and position."""
        self.id = entity_id
        self.pos = pos
        self.behaviour = behaviour

    @abstractmethod
    def update(self, *args: int, **kwargs: int) -> None:
        """Update the entity's state."""
        if mouse.capture_mouse(self.id):
            print(f"{self.__class__.__name__} {self.id} was clicked")

    def destroy(self) -> None:
        """Destroy the entity."""
