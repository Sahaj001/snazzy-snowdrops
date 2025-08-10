from __future__ import annotations

from engine import mouse
from engine.interfaces import Behaviour, Living, Pos
from game.entities.entity import Entity


class NPC(Entity, Living):
    """Non-Player Character (NPC) in the game world."""

    def __init__(
        self,
        entity_id: str,
        pos: Pos,
        behaviour: Behaviour,
        ai_state: str = "idle",
    ) -> None:
        super().__init__(entity_id, pos, behaviour)
        self.ai_state = ai_state
        self.hp = 50

    def update(
        self,
    ) -> None:
        """Update the NPC's AI state and behavior."""
        if mouse.capture_mouse(self.id):
            print(f"{self.__class__.__name__} {self.id} was clicked")

    def is_alive(self) -> bool:
        """Check if the NPC is alive based on HP."""
        return self.hp > 0

    def take_damage(self, n: int) -> None:
        """Reduce NPC's HP by n, ensuring it doesn't go below 0."""
        self.hp = max(self.hp - n, 0)
