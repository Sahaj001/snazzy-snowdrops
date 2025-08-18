from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from engine.event_bus import EventType, GameEvent
from engine.interfaces import Behaviour, Interactable
from game.entities.entity import Entity

if TYPE_CHECKING:
    from engine.event_bus import EventBus
    from models import Pos
    from models.sprite import SpriteRegistry


class FruitState(Enum):
    FRESH = "fresh"
    PICKED = "picked"


class Fruit(Entity, Interactable):
    """Represents a fruit entity in the game world."""

    def __init__(
        self,
        fruit_id: str,
        pos: Pos,
        behaviour: Behaviour,
        sprite_registry: SpriteRegistry | None = None,
    ) -> None:
        super().__init__(fruit_id, pos, behaviour, sprite_registry)
        self.max_hp = 5
        self.state = FruitState.FRESH

    def interact(self, actor: Entity, event_bus: EventBus) -> None:
        """Allow an actor to interact with the fruit, e.g., pick it up."""
        if self.state == FruitState.PICKED:
            return
        event_bus.post(
            GameEvent(
                event_type=EventType.ASK_DIALOG,
                payload={
                    "dialog": f"Do you want to pick up the fruit with hp {self.max_hp}.",
                    "callback": lambda answer: self.pick_up(actor, event_bus, answer),
                    "options": ["Pick Up", "Eat", "Exit"],
                    "selected_index": 0,
                },
            ),
        )
        print(f"pushing interaction event for {self.id} by {actor.id}")

    def pick_up(self, actor: Entity, event_bus: EventBus, answer: str) -> None:
        """Handle the logic for picking up the fruit."""
        if answer == "Eat":
            if hasattr(actor, "hp") and actor.hp > 0:
                actor.hp = min(actor.hp + self.max_hp, actor.max_hp)
            print(f"{actor.id} has eaten {self.id}.")

            event_bus.post(
                GameEvent(
                    event_type=EventType.FRUIT_PICKED,
                    payload={"fruit_id": self.id, "actor_id": actor.id},
                ),
            )

        if answer == "Pick Up":
            event_bus.post(
                GameEvent(
                    event_type=EventType.INVENTORY_CHANGE,
                    payload={"object_name": "fruit", "action": "add", "item_id": self.id}
                )
            )

            event_bus.post(
                    GameEvent(
                        event_type=EventType.FRUIT_PICKED,
                        payload={"fruit_id": self.id, "actor_id": actor.id},
                    ),
                )


        event_bus.post(
            GameEvent(
                event_type=EventType.CLOSE_DIALOG,
                payload={"dialog_id": "fruit_pickup_dialog"},
            ),
        )

    def update(
        self,
        **kwargs: int,
    ) -> None:
        """Update the fruit's state."""
        events = kwargs.get("events", [])
        for event in events:
            if event.event_type == EventType.FRUIT_PICKED:
                fruit_id = event.payload.get("fruit_id")
                if fruit_id == self.id:
                    self.state = FruitState.PICKED
                    event.consume()

        self.update_frame_idx()

    def update_frame_idx(self) -> None:
        """Update player sprite frame idx."""
        sprite = self.sprite_registry.get(self.state.value)
        if sprite and sprite.is_animated():
            self.frame_idx = (self.frame_idx + 1) % sprite.frame_count
        else:
            self.frame_idx = 0


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
