from random import randint, shuffle
from typing import Any

from engine.event_bus import GameEvent


class SlidingTilesPuzzle:
    def __init__(self, event: GameEvent) -> None:
        self.size = 3
        self.tile_size = 16
        self.event = event
        self.tiles: list[int] = list(range(self.size**2))
        # this is why we need a 1d array
        self.tiles[randint(0, len(self.tiles) - 1)] = -1
        shuffle(self.tiles)

    def draw(self, canvas: Any) -> None:
        self.canvas = canvas
        # Background
        gap = 2
        total_gap = max(0, self.size - 1) * gap
        width, height = total_gap + self.size * self.tile_size, total_gap + self.size * self.tile_size
        ix, iy = (canvas.width - width) // 2, (canvas.height - height) // 2

        ctx = canvas.getContext("2d", alpha=True)

        # Background
        ctx.fillStyle = "rgba(0, 0, 0, 0.7)"
        ctx.fillRect(ix, iy, width, height)

        for y in range(self.size):
            for x in range(self.size):
                cell = self.tiles[x + y * self.size]
                if cell == -1:
                    continue
                w = gap + self.tile_size
                ctx.fillStyle = "white"
                ctx.fillRect(ix + x * w, iy + y * w, self.tile_size, self.tile_size)
                ctx.fillStyle = "black"
                ctx.font = "12px monospace"
                ctx.fillText(cell, ix + x * w, iy + y * w + 12)

    def handle_input(self, input: Any) -> None:
        i = self.tiles.index(-1)
        x = i % self.size
        y = i // self.size
        if input["key"] == "ArrowRight" and x != 0:
            t = self.tiles[i - 1]
            self.tiles[i] = t
            self.tiles[i - 1] = -1
        if input["key"] == "ArrowLeft" and x != self.size - 1:
            t = self.tiles[i + 1]
            self.tiles[i] = t
            self.tiles[i + 1] = -1
        if input["key"] == "ArrowUp" and y != self.size - 1:
            t = self.tiles[i + self.size]
            self.tiles[i] = t
            self.tiles[i + self.size] = -1
        if input["key"] == "ArrowDown" and y != 0:
            t = self.tiles[i - self.size]
            self.tiles[i] = t
            self.tiles[i - self.size] = -1
