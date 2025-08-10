from __future__ import annotations

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

    def is_alive(self) -> bool:
        """Check if the NPC is alive based on HP."""
        return self.hp > 0

    def take_damage(self, n: int) -> None:
        """Reduce NPC's HP by n, ensuring it doesn't go below 0."""
        self.hp = max(self.hp - n, 0)
