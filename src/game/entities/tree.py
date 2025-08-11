from __future__ import annotations

from typing import TYPE_CHECKING

from engine.interfaces import Behaviour, Interactable
from game.entities.entity import Entity

if TYPE_CHECKING:
    from engine.interfaces import Pos


class Tree(Entity, Interactable):
    """Represents a tree entity in the game world."""

    def __init__(self, tree_id: str, pos: Pos, behaviour: Behaviour) -> None:
        super().__init__(tree_id, pos, behaviour)

    def interact(self, actor: Entity) -> None:
        """Allow an actor to interact with the tree, e.g., chop it down or gather resources."""
        print(f"{actor.id} interacts with tree {self.id}")

    def update(
        self,
        *args: int,
        **kwargs: int,
    ) -> None:
        """Update the tree's state."""
        # Trees may have seasonal changes or drop fruits

    def __str__(self) -> str:
        return f"Tree(id={self.id}, pos={self.pos})"


class TreeBehaviour(Behaviour):
    """Defines the behaviour of a tree entity."""

    @property
    def passable(self) -> bool:
        """Trees are not passable."""
        return False

    @property
    def interactable(self) -> bool:
        """Trees can be interacted with."""
        return False
