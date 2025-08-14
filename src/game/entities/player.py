from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from engine.event_bus import EventBus, EventType, GameEvent
from engine.interfaces import Behaviour, Interactable, Living
from game.entities.entity import Entity
from game.inventory import Inventory
from models.direction import Direction

if TYPE_CHECKING:
    from game.world import World
    from models.position import Pos
    from models.sprite import SpriteRegistry


class PlayerState(Enum):
    """Enum representing the player's state."""

    IDLE = "idle"
    WALKING_UP = "walking_up"
    WALKING_DOWN = "walking_down"
    WALKING_LEFT = "walking_left"
    WALKING_RIGHT = "walking_right"
    INTERACTING = "interacting"
    DEAD = "dead"


class Player(Entity, Living, Interactable):
    """Player character in the game world."""

    def __init__(
        self,
        entity_id: str,
        pos: Pos,
        behaviour: Behaviour,
        hp: int = 100,
        intelligence: int = 0,
        fatigue: int = 0,
        sprite_registry: SpriteRegistry | None = None,
    ) -> None:
        super().__init__(entity_id, pos, behaviour, sprite_registry)
        self.inventory = Inventory()
        self.hp = hp
        self.intelligence = intelligence

        self.max_hp = 100
        self.fatigue = fatigue
        self.max_intelligence = 100
        self.max_fatigue = 100
        self.step_size = 20  # in pixel
        self.state = PlayerState.IDLE

    def move(self, key: str, world: World) -> None:
        """Move the player by dx, dy if the target tile is passable."""
        direction = Direction.from_key(key)
        if not direction:
            self.state = PlayerState.IDLE
            return

        dx, dy = direction.value
        new_x = self.pos.x + dx * self.step_size
        new_y = self.pos.y + dy * self.step_size
        if world.is_passable(new_x, new_y):
            self.pos.x = new_x
            self.pos.y = new_y
            if direction.value == Direction.LEFT.value:
                self.state = PlayerState.WALKING_LEFT
            elif direction.value == Direction.RIGHT.value:
                self.state = PlayerState.WALKING_RIGHT
            elif direction.value == Direction.UP.value:
                self.state = PlayerState.WALKING_UP
            elif direction.value == Direction.DOWN.value:
                self.state = PlayerState.WALKING_DOWN
        else:
            self.state = PlayerState.IDLE

    def update(
        self,
        **kwargs: int,
    ) -> None:
        """Update the player's state."""
        # Player-specific update logic can go here
        events = kwargs.get("events", [])
        self.state = PlayerState.IDLE  # Reset state to idle by default
        for event in events:
            if event.event_type == EventType.PLAYER_MOVED:
                key = event.payload.get("key")
                if key:
                    self.move(key, kwargs.get("world"))
                event.consume()

        self.update_frame_idx()

    def update_frame_idx(self) -> None:
        """Update player sprite frame idx."""
        sprite = self.sprite_registry.get(self.state.value)
        if sprite and sprite.is_animated():
            self.frame_idx = (self.frame_idx + 1) % sprite.frame_count
        else:
            self.frame_idx = 0

    def is_alive(self) -> bool:
        """Check if the player is alive based on HP."""
        return self.hp > 0

    def take_damage(self, n: int) -> None:
        """Reduce player's HP by n, ensuring it doesn't go below 0."""
        self.hp = max(self.hp - n, 0)

    def interact(self, _actor: Entity, event_bus: EventBus) -> None:
        """Handle interaction with the player, e.g., opening inventory."""
        print(f"{self.id} interacts with player.")
        event_bus.post(
            GameEvent(
                event_type=EventType.UI_UPDATE,
                payload={
                    "overlay_id": "player_info",
                    "inventory": self.inventory.slots,
                    "hp": self.hp,
                },
            ),
        )

    def get_hud_info(self) -> str:
        """Get player HUD information."""
        hud_info = {
            "id": self.id,
            "hp": self.hp,
            "inventory": self.inventory.slots,
            "pos": self.pos,
            "state": self.state,
        }
        return str(hud_info)

    def get_status_info(self) -> dict[str, int]:
        """Get player status information."""
        return {
            "hp": self.hp,
            "max_hp": self.max_hp,
            "intelligence": self.intelligence,
            "max_intelligence": self.max_intelligence,
            "fatigue": self.fatigue,
            "max_fatigue": self.max_fatigue,
        }
