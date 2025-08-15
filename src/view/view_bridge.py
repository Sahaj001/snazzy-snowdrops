from __future__ import annotations

from typing import TYPE_CHECKING

import js
from js import Image, document
from pyodide.ffi import create_proxy

from engine.input_system import InputEvent, InputSystem, InputType
from models.draw_cmd import DrawCmdType

if TYPE_CHECKING:
    from js import HTMLCanvasElement

    from models.draw_cmd import DrawCmd
    from models.position import Pos
    from models.tile import TilesRegistry

ALLOWED_INPUTS = [
    "ArrowUp",
    "ArrowDown",
    "ArrowLeft",
    "ArrowRight",
    "W",
    "A",
    "S",
    "D",
    "w",
    "a",
    "s",
    "d",
    "Enter",
    "Escape",
    "e",
    "E",
]


class ViewBridge:
    """Abstracts the JS ↔ Pyodide interface."""

    def __init__(
        self,
        canvas: HTMLCanvasElement,
        input_sys: InputSystem,
        tiles_registry: TilesRegistry = None,
    ) -> None:
        self.canvas = canvas
        self.ctx = canvas.getContext("2d", alpha=True)
        self._image_cache = {}
        self.tiles_registry = tiles_registry
        self.input_sys = input_sys
        self._setup_event_handler()

    def _setup_event_handler(self) -> None:
        def on_key_down(evt: js.KeyBoardEvent) -> None:
            if self.input_sys and evt.key in ALLOWED_INPUTS:
                self.input_sys.push_event(InputEvent(InputType.KEYDOWN, evt.key))
            evt.preventDefault()

        def on_click(evt: js.MouseEvent) -> None:
            if self.input_sys:
                # Convert click position to canvas coordinates
                rect = self.canvas.getBoundingClientRect()
                x = evt.clientX - rect.left
                y = evt.clientY - rect.top
                self.input_sys.push_event(InputEvent(InputType.CLICK, None, (x, y)))
            evt.preventDefault()

        self.key_down_proxy = create_proxy(on_key_down)
        self.click_proxy = create_proxy(on_click)

        document.addEventListener("keydown", self.key_down_proxy)
        document.addEventListener("click", self.click_proxy)

    def draw(self, cmds: list[DrawCmd]) -> None:
        """Send draw commands to the JS side for rendering."""
        # Clear canvas before drawing
        self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height)

        # Process each draw command
        for cmd in cmds:
            if cmd.type == DrawCmdType.SPRITE:
                cmd.sprite.draw(
                    self.canvas,
                    self._load_image(cmd.sprite.image_path),
                    cmd.position,
                    cmd.rotation,
                )
            elif cmd.type == DrawCmdType.TILE:
                self.tiles_registry.draw_tile(self.canvas, cmd.tile_gid, cmd.position)
            elif cmd.type == DrawCmdType.TEXT:
                self.draw_text(
                    cmd.text,
                    cmd.position,
                )
            elif cmd.type == DrawCmdType.DIALOG:
                cmd.dialog.draw(self.canvas)
            elif cmd.type == DrawCmdType.STATUS_BAR:
                cmd.status_bar.draw(self.canvas)
            elif cmd.type == DrawCmdType.INVENTORY_OVERLAY:
                cmd.inventory_overlay.draw(self.canvas)

        self.tiles_registry.static_count += 1

    def draw_text(
        self,
        text: str,
        position: Pos,
        font: str = "16px Arial",
        color: str = "white",
        background_color: str = "rgba(0,0,0,0.7)",
    ) -> None:
        """Draws text with a background like a HUD or popup."""
        self.ctx.font = font
        self.ctx.fillStyle = background_color

        padding: int = 6
        metrics = self.ctx.measureText(text)
        text_width = metrics.width
        text_height = int(font.split("px")[0])

        self.ctx.fillRect(
            position.x - padding,
            position.y - text_height,
            text_width + padding * 2,
            text_height + padding,
        )

        self.ctx.fillStyle = color
        self.ctx.fillText(text, position.x, position.y)

    def _load_image(self, path: str) -> Image:
        """Cache and return HTMLImageElement for a given path."""
        if path not in self._image_cache:
            img = Image.new()
            img.src = path
            self._image_cache[path] = img

        return self._image_cache[path]

    def load_assets(self, index_path: str) -> None:
        """Load assets from a given index path."""
        # This would load assets via JS
