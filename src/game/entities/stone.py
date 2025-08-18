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


class StoneState(Enum):
    IDLE = "idle"
    PUZZLE_ACTIVE = "puzzle_active"
    SOLVED = "solved"


class Stone(Entity, Interactable):
    """Represents a stone entity that can trigger a puzzle when clicked."""

    def __init__(
        self,
        stone_id: str,
        pos: Pos,
        behaviour: Behaviour,
        sprite_registry: SpriteRegistry | None = None,
    ) -> None:
        super().__init__(stone_id, pos, behaviour, sprite_registry)
        self.state = StoneState.IDLE

    def interact(self, actor: Entity, event_bus: EventBus) -> None:
        """When player interacts with the stone, trigger the puzzle."""
        if self.state == StoneState.SOLVED:
            return  # already solved, ignore

        # Post event to open the puzzle UI
        event_bus.post(
            GameEvent(
                event_type=EventType.START_PUZZLE,
                payload={
                    "puzzle_type": "sliding_tiles",
                    "image": "assets/images/puzzle/stone_puzzle.png",
                    "grid_size": 3,
                    "callback": lambda solved: self.on_puzzle_finished(event_bus, solved),
                },
            )
        )
        print(f"Stone {self.id} triggered puzzle by {actor.id}")
        self.state = StoneState.PUZZLE_ACTIVE

    def on_puzzle_finished(self, event_bus: EventBus, solved: bool) -> None:
        """Handle the result of the puzzle."""
        if solved:
            print(f"Puzzle solved for {self.id}!")
            self.state = StoneState.SOLVED

            event_bus.post(
                GameEvent(
                    event_type=EventType.PUZZLE_SOLVED,
                    payload={"stone_id": self.id},
                )
            )
        else:
            print(f"Puzzle failed or exited for {self.id}")
            self.state = StoneState.IDLE

    def update(self, **kwargs) -> None:
        """Update the stone's state based on events."""
        events = kwargs.get("events", [])
        for event in events:
            if event.event_type == EventType.PUZZLE_SOLVED:
                stone_id = event.payload.get("stone_id")
                if stone_id == self.id:
                    event.consume()

        self.update_frame_idx()

    def update_frame_idx(self) -> None:
        """Update sprite frame based on state."""
        sprite = self.sprite_registry.get(self.state.value)
        if sprite and sprite.is_animated():
            self.frame_idx = (self.frame_idx + 1) % sprite.frame_count
        else:
            self.frame_idx = 0


class StoneBehaviour(Behaviour):
    """Defines the behaviour of a stone entity."""

    @property
    def passable(self) -> bool:
        return False  # player can’t walk through stone

    @property
    def interactable(self) -> bool:
        return True  # player can click/interact
