from typing import TYPE_CHECKING, Protocol

from models.position import Pos

if TYPE_CHECKING:
    from engine.event_bus import EventBus
    from game.entities.entity import Entity


class Object(Protocol):
    """Anything that has an ID and a position in the world."""

    id: str
    pos: Pos

    def destroy(self) -> None:
        """Destroy this object, removing it from the world."""


class Behaviour(Protocol):
    """Defines passability and interaction rules for entities."""

    @property
    def passable(self) -> bool:
        """Whether this entity can be passed through by players or NPCs."""

    @property
    def interactable(self) -> bool:
        """Whether this entity can be interacted with by players or NPCs."""


class Interactable(Protocol):
    """Marks an entity as interactable by players or NPCs."""

    def interact(self, actor: "Entity", event_bus: "EventBus") -> None:
        """Perform an interaction with the given actor."""


class Living(Protocol):
    """Marks an entity as living with HP and damage handling."""

    hp: int

    def is_alive(self) -> bool:
        """Check if the entity is still alive."""

    def take_damage(self, n: int) -> None:
        """Apply damage to the entity, reducing its HP."""


class Drawable(Protocol):
    """Marks an entity as drawable on the screen."""

    def draw(self, *args: int, **kwargs: int) -> None:
        """Draw this entity on the screen using the current view context."""
