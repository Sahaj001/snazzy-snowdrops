from __future__ import annotations

from js import window
from pyodide.ffi import create_proxy

from . import game, gameloop

last_time = 0.0
frame_interval = 1000 / game.FRAME_RATE


def _game_loop(timestamp: float) -> None:
    global last_time
    if timestamp - last_time >= frame_interval:
        last_time = timestamp
        gameloop.update()
        gameloop.render()
        game.time += 1
    window.requestAnimationFrame(game_loop)


game_loop = create_proxy(_game_loop)
window.requestAnimationFrame(game_loop)
