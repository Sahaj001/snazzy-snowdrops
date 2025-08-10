from __future__ import annotations

from typing import TYPE_CHECKING

import js
from js import Image, document
from pyodide.ffi import create_proxy

from engine.input_system import InputEvent, InputSystem, InputType

if TYPE_CHECKING:
    from js import HTMLCanvasElement

    from models.draw_cmd import DrawCmd


class ViewBridge:
    """Abstracts the JS ↔ Pyodide interface."""

    def __init__(self, canvas: HTMLCanvasElement, input_sys: InputSystem) -> None:
        self.canvas = canvas
        self.ctx = canvas.getContext("2d")
        self._image_cache = {}
        self.input_sys = input_sys
        self._setup_event_handler()

    def _setup_event_handler(self) -> None:
        def on_key_down(evt: js.KeyBoardEvent) -> None:
            if self.input_sys:
                self.input_sys.push_event(InputEvent(InputType.KEYDOWN, evt.key))
            evt.preventDefault()

        def on_key_up(evt: js.KeyBoardEvent) -> None:
            if self.input_sys:
                self.input_sys.push_event(InputEvent(InputType.KEYUP, evt.key))
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
        self.key_up_proxy = create_proxy(on_key_up)
        self.click_proxy = create_proxy(on_click)

        document.addEventListener("keydown", self.key_down_proxy)
        document.addEventListener("keyup", self.key_up_proxy)
        document.addEventListener("click", self.click_proxy)

    def draw(self, cmds: list[DrawCmd]) -> None:
        """Send draw commands to the JS side for rendering."""
        # Clear canvas before drawing
        self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height)

        # Process each draw command
        for cmd in cmds:
            sprite = cmd.sprite
            img = self._load_image(sprite.image_path)  # helper

            x, y = cmd.position.x, cmd.position.y
            w, h = sprite.size
            self.ctx.drawImage(img, x, y, w, h)

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
