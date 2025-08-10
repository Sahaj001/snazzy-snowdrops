from __future__ import annotations

from typing import Any

from js import Image  # pyright: ignore[reportAttributeAccessIssue]

from . import game


class Images:
    def __init__(self) -> None:
        self._images: dict[str, object] = {}

    def __getitem__(self, key: str) -> Any:
        if key in self._images:
            return self._images[key]
        image = Image.new()
        image.src = f"/static/images/{key}.png"
        self._images[key] = image
        return image


images = Images()


def render_image(image: str, sx: int, sy: int) -> None:
    img = images[image]
    x = sx - game.camx + (game.WIDTH / 2)
    y = (game.HEIGHT / 2) - (sy - game.camy)
    game.ctx.drawImage(
        img,
        0,
        0,
        img.width,
        img.height,
        x,
        y - img.height,
        img.width,
        img.height,
    )
