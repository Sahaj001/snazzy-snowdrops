from __future__ import annotations

from math import ceil, floor

from . import game
from .data import Tile
from .images import render_image


def render_tiles() -> None:
    h = ceil(game.HEIGHT / game.TILE_SIZE)
    w = ceil(game.WIDTH / game.TILE_SIZE)
    for y in range(h):
        for x in range(w):
            tx = x + floor(game.camx / game.TILE_SIZE) - floor(w / 2)
            ty = y + floor(game.camy / game.TILE_SIZE) - floor(h / 2)
            if 0 <= tx < game.LEVEL_WIDTH and 0 <= ty < game.LEVEL_HEIGHT:
                tile = game.tiles[tx + ty * game.LEVEL_WIDTH]
                if tile != Tile.AIR:
                    render_image(
                        str(tile),
                        tx * game.TILE_SIZE,
                        ty * game.TILE_SIZE,
                    )
