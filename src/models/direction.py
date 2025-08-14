from enum import Enum


class Direction(Enum):
    """Enumeration for movement directions."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
