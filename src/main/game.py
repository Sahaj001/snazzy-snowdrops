from __future__ import annotations

from js import document

from .data import Player, Sprite, Tile

canvas = document.getElementById("canvas")
ctx = canvas.getContext("2d")  # pyright: ignore[reportAttributeAccessIssue]

TILE_SIZE = 32
LEVEL_WIDTH = 256
LEVEL_HEIGHT = 256
WIDTH: int = canvas.width  # pyright: ignore[reportAttributeAccessIssue]
HEIGHT: int = canvas.height  # pyright: ignore[reportAttributeAccessIssue]
FRAME_RATE: int = 60

time: int = 0
tiles: list[Tile] = [Tile.AIR] * LEVEL_WIDTH * LEVEL_HEIGHT
sprites: list[Sprite] = []
player: Player = Player()
# camera world space
camx: int = 0
camy: int = 0
