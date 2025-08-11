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
    from models.sprite import Sprite
    from ui.dialog import DialogBox

ALLOWED_INPUTS = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Enter", "Escape"]


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
                self.draw_sprite(cmd.sprite, cmd.position)
            elif cmd.type == DrawCmdType.TEXT:
                self.draw_text(
                    cmd.text,
                    cmd.position,
                )
            elif cmd.type == DrawCmdType.DIALOG:
                self.draw_dialog(cmd.dialog)

    def draw_dialog(self, dialog: DialogBox) -> None:
        """Draw a dialog box on the canvas."""
        # Background
        width, height = 300, 150
        x, y = (self.canvas.width - width) // 2, (self.canvas.height - height) // 2

        # Background
        self.ctx.fillStyle = "rgba(0, 0, 0, 0.7)"
        self.ctx.fillRect(x, y, width, height)

        # Text
        self.ctx.fillStyle = "white"
        self.ctx.font = "18px Arial"
        self.ctx.fillText(dialog.text, x + 20, y + 40)

        # Options
        for i, option in enumerate(dialog.options):
            color = "yellow" if i == dialog.selected_index else "white"
            self.ctx.fillStyle = color
            self.ctx.fillText(option, x + 20 + i * 100, y + 100)

    def draw_sprite(self, sprite: Sprite, position: Pos) -> None:
        """Draw a single sprite at a given position."""
        img = self._load_image(sprite.image_path)
        x, y = position.x, position.y
        w, h = sprite.size
        self.ctx.drawImage(img, x, y, w, h)

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
