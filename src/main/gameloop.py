from __future__ import annotations

from main import images, player, tiles

from . import game, sprites


def update() -> None:
    for sprite in game.sprites:
        sprites.update_sprite(sprite)
    player.update_player()


def render() -> None:
    images.render_image("grid-xy", -game.WIDTH // 2, -game.HEIGHT // 2)
    tiles.render_tiles()
    for sprite in game.sprites:
        sprites.render_sprite(sprite)
    player.render_player()
