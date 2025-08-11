from __future__ import annotations

from typing import TYPE_CHECKING

from engine.interfaces import Behaviour, Interactable, Pos
from game.entities.entity import Entity

if TYPE_CHECKING:
    from engine.event_bus import EventBus


class Fruit(Entity, Interactable):
    """Represents a fruit entity in the game world."""

    def __init__(
        self,
        fruit_id: str,
        pos: Pos,
        behaviour: Behaviour,
    ) -> None:
        super().__init__(fruit_id, pos, behaviour)

    def interact(self, actor: Entity, _event_bus: EventBus) -> None:
        """Allow an actor to interact with the fruit, e.g., pick it up."""
        # Example: Add fruit to actor's inventory if available
        if hasattr(actor, "inventory"):
            actor.inventory.add(self.id, 1)
            print(f"{actor.id} picked up {self.id}.")

    def update(
        self,
        *args: int,
        **kwargs: int,
    ) -> None:
        """Update the fruit's state."""


class FruitBehaviour(Behaviour):
    """Defines the behaviour of a fruit entity."""

    @property
    def passable(self) -> bool:
        """Fruits are passable."""
        return True

    @property
    def interactable(self) -> bool:
        """Fruits can be interacted with."""
        return True
