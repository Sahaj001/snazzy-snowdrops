from __future__ import annotations

from typing import TYPE_CHECKING

from engine.event_bus import EventBus, EventType, GameEvent
from engine.interfaces import Behaviour, Interactable, Living
from game.entities.entity import Entity
from game.inventory import Inventory

if TYPE_CHECKING:
    from game.world import World
    from models.direction import Direction
    from models.position import Pos


class Player(Entity, Living, Interactable):
    """Player character in the game world."""

    def __init__(
        self,
        entity_id: str,
        pos: Pos,
        behaviour: Behaviour,
        hp: int = 100,
        max_hp: int = 100,
        intelligence: int = 0,
        max_intelligence: int = 100,
        fatigue: int = 0,
        max_fatigue: int = 100,
        speed: float = 1.0,
    ) -> None:
        super().__init__(entity_id, pos, behaviour)
        self.inventory = Inventory()
        self.speed = speed
        self.hp = hp
        self.max_hp = max_hp
        self.intelligence = intelligence
        self.max_intelligence = max_intelligence
        self.fatigue = fatigue
        self.max_fatigue = max_fatigue
        self.step_size = 1

    def move(self, direction: Direction, world: World) -> None:
        """Move the player by dx, dy if the target tile is passable."""
        dx, dy = direction.value
        new_x = self.pos.x + dx * self.step_size
        new_y = self.pos.y + dy * self.step_size
        if world.is_passable(new_x, new_y):
            self.pos.x = new_x
            self.pos.y = new_y

    def update(
        self,
        *args: int,
        **kwargs: int,
    ) -> None:
        """Update the player's state."""
        # Player-specific update logic can go here

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
