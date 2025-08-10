from __future__ import annotations

from typing import TYPE_CHECKING

from . import game
from .data import Tile
from .images import render_image

if TYPE_CHECKING:
    from .data import Sprite


def is_solid_tile(tile_x: int, tile_y: int) -> bool:
    if (
        tile_x < 0
        or tile_x >= game.LEVEL_WIDTH
        or tile_y < 0
        or tile_y >= game.LEVEL_HEIGHT
    ):
        return True
    return game.tiles[tile_x + tile_y * game.LEVEL_WIDTH] != Tile.AIR


def move_x(sprite: Sprite, dx: int) -> None:
    new_x = sprite.x + dx
    tile_x = new_x // game.TILE_SIZE
    tile_y = sprite.y // game.TILE_SIZE
    if is_solid_tile(tile_x, tile_y):
        if dx > 0:
            sprite.x = tile_x * game.TILE_SIZE - game.TILE_SIZE
        elif dx < 0:
            sprite.x = (tile_x + 1) * game.TILE_SIZE
        sprite.dx = 0
    else:
        sprite.x = new_x


def move_y(sprite: Sprite, dy: int) -> None:
    new_y = sprite.y + dy
    tile_x = sprite.x // game.TILE_SIZE
    tile_y = new_y // game.TILE_SIZE
    if is_solid_tile(tile_x, tile_y):
        if dy > 0:
            sprite.y = tile_y * game.TILE_SIZE - game.TILE_SIZE
        elif dy < 0:
            sprite.y = (tile_y + 1) * game.TILE_SIZE
        sprite.dy = 0
    else:
        sprite.y = new_y


def update_sprite(sprite: Sprite) -> None:
    move_x(sprite, sprite.dx)
    move_y(sprite, sprite.dy)
    sprite.dy -= 1


def render_sprite(sprite: Sprite) -> None:
    render_image(sprite.image, sprite.x, sprite.y)
