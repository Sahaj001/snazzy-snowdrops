from __future__ import annotations

from typing import TYPE_CHECKING

from engine.interfaces import Behaviour, Living
from game.entities.entity import Entity
from game.inventory import Inventory

if TYPE_CHECKING:
    from game.world import World
    from models.position import Pos


class Player(Entity, Living):
    """Player character in the game world."""

    def __init__(
        self,
        entity_id: str,
        pos: Pos,
        behaviour: Behaviour,
        speed: float = 1.0,
    ) -> None:
        super().__init__(entity_id, pos, behaviour)
        self.inventory = Inventory()
        self.speed = speed
        self.hp = 100

    def move(self, dx: int, dy: int, world: World) -> None:
        """Move the player by dx, dy if the target tile is passable."""
        new_x = self.pos.x + dx
        new_y = self.pos.y + dy
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
