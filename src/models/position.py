from dataclasses import dataclass


@dataclass
class Pos:
    """Represents a position in the world with x and y coordinates."""

    x: int
    y: int
    z: int = 0  # Optional z-coordinate for 3D space

    def tile_position(self, tile_size: int) -> tuple[int, int]:
        """Convert pixel position to tile coordinates."""
        return self.x // tile_size, self.y // tile_size
