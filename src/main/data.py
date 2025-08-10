from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, auto


class Tile(StrEnum):
    AIR = auto()


@dataclass(slots=True)
class Sprite:
    # bottom-left origin world space
    x: int = 0
    y: int = 0
    # velocity world space
    dx: int = 0
    dy: int = 0
    image: str = "missing"


@dataclass(slots=True)
class Player(Sprite):
    pass
