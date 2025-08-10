from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from js import HTMLCanvasElement

    from engine.input_system import InputEvent
    from models.draw_cmd import DrawCmd


class ViewBridge:
    """Abstracts the JS ↔ Pyodide interface."""

    def __init__(self, canvas: HTMLCanvasElement) -> None:
        self.canvas = canvas

    def draw(self, cmds: list[DrawCmd]) -> None:
        """Send draw commands to the JS side for rendering."""
        # This would call into JS to render

    def get_input_events(self) -> list[InputEvent]:
        """Retrieve input events from the JS side."""
        # This would pull events from JS
        return []

    def load_assets(self, index_path: str) -> None:
        """Load assets from a given index path."""
        # This would load assets via JS
