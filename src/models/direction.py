import random
from enum import Enum
from typing import Optional


class Direction(Enum):
    """Enumeration for movement directions."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @classmethod
    def from_key(cls, key: str) -> Optional["Direction"]:
        """Convert a string to a Direction enum."""
        if key == "ArrowUp":
            return cls.UP
        if key == "ArrowDown":
            return cls.DOWN
        if key == "ArrowLeft":
            return cls.LEFT
        if key == "ArrowRight":
            return cls.RIGHT
        return None

    @classmethod
    def random(cls) -> "Direction":
        """Return a random direction."""
        return random.choice(list(cls))
