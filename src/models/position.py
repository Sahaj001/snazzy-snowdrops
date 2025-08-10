from dataclasses import dataclass


@dataclass
class Pos:
    """Represents a position in the world with x and y coordinates."""

    x: int
    y: int
    z: int = 0  # Optional z-coordinate for 3D space
