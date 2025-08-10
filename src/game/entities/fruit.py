from __future__ import annotations

from engine import mouse
from engine.interfaces import Behaviour, Interactable, Pos
from game.entities.entity import Entity


class Fruit(Entity, Interactable):
    """Represents a fruit entity in the game world."""

    def __init__(
        self,
        fruit_id: str,
        pos: Pos,
        behaviour: Behaviour,
        item_id: str,
    ) -> None:
        super().__init__(fruit_id, pos, behaviour)
        self.item_id = item_id

    def interact(self, actor: Entity) -> None:
        """Allow an actor to interact with the fruit, e.g., pick it up."""
        # Example: Add fruit to actor's inventory if available
        if hasattr(actor, "inventory"):
            actor.inventory.add(self.item_id, 1)
            print(f"{actor.id} picked up {self.item_id}")

    def update(
        self,
    ) -> None:
        """Update the fruit's state."""
        if mouse.capture_mouse(self.id):
            print(f"{self.__class__.__name__} {self.id} was clicked")
