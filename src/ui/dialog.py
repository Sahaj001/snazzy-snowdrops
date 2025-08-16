from collections.abc import Callable
from dataclasses import dataclass

from js import HTMLCanvasElement

from engine.interfaces import Drawable


@dataclass
class DialogBox(Drawable):
    """Represents a dialog box with text and options."""

    text: str
    options: list[str]  # ["Yes", "No"]
    selected_index: int = 0
    callback: Callable[[str], None] = None

    def draw(
        self,
        canvas: HTMLCanvasElement,
    ) -> None:
        """Draw a dialog box on the canvas."""
        # Background
        width, height = 450, 150
        x, y = (canvas.width - width) // 2, (canvas.height - height) // 2

        ctx = canvas.getContext("2d", alpha=True)

        # Background
        ctx.fillStyle = "rgba(0, 0, 0, 0.7)"
        ctx.fillRect(x, y, width, height)

        # Text
        ctx.fillStyle = "white"
        ctx.font = "18px Arial"
        ctx.fillText(self.text, x + 20, y + 40)

        # Options
        for i, option in enumerate(self.options):
            color = "yellow" if i == self.selected_index else "white"
            ctx.fillStyle = color
            ctx.fillText(option, x + 20 + i * 100, y + 100)
