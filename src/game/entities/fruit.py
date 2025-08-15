from __future__ import annotations

from typing import TYPE_CHECKING

from engine.event_bus import EventType, GameEvent
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
        max_hp: int = 5,
    ) -> None:
        super().__init__(fruit_id, pos, behaviour)
        self.max_hp = max_hp

    def interact(self, actor: Entity, event_bus: EventBus) -> None:
        """Allow an actor to interact with the fruit, e.g., pick it up."""
        # ask the actor to pick up the fruit
        event_bus.post(
            GameEvent(
                event_type=EventType.ASK_DIALOG,
                payload={
                    "dialog": f"{actor.id} wants to pick up {self.id}.",
                    "callback": lambda answer: (
                        self.pick_up(actor, event_bus) if answer == "Yes" else None
                    ),
                    "options": ["Yes", "No"],
                    "selected_index": 0,
                },
            ),
        )
        print(f"pushing interaction event for {self.id} by {actor.id}")

    def pick_up(self, actor: Entity, event_bus: EventBus) -> None:
        """Handle the logic for picking up the fruit."""
        if hasattr(actor, "hp") and actor.hp > 0:
            actor.hp = min(actor.hp + self.max_hp, actor.max_hp)
            print(f"{actor.id} picked up {self.id}.")

            event_bus.post(
                GameEvent(
                    event_type=EventType.FRUIT_PICKED,
                    payload={"fruit_id": self.id, "actor_id": actor.id},
                ),
            )

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
