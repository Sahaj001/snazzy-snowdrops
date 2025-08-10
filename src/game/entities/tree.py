from __future__ import annotations

from typing import TYPE_CHECKING

from engine.interfaces import Interactable
from game.entities.entity import Entity

if TYPE_CHECKING:
    from engine.interfaces import Behaviour, Pos


class Tree(Entity, Interactable):
    """Represents a tree entity in the game world."""

    def __init__(self, entity_id: str, pos: Pos, behaviour: Behaviour) -> None:
        super().__init__(entity_id, pos, behaviour)

    def interact(self, actor: Entity) -> None:
        """Allow an actor to interact with the tree, e.g., chop it down or gather resources."""
        print(f"{actor.id} interacts with tree {self.id}")

    def update(
        self,
    ) -> None:
        """UUpdate the tree's state."""
        # Trees may have seasonal changes or drop fruits
