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
        if key == "ArrowUp" or key.lower() == "w":
            return cls.UP
        if key == "ArrowDown" or key.lower() == "s":
            return cls.DOWN
        if key == "ArrowLeft" or key.lower() == "a":
            return cls.LEFT
        if key == "ArrowRight" or key.lower() == "d":
            return cls.RIGHT
        return None

    @classmethod
    def random(cls) -> "Direction":
        """Return a random direction."""
        return random.choice(list(cls))
