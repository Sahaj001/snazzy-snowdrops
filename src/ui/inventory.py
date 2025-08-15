from dataclasses import dataclass

from js import HTMLCanvasElement


@dataclass
class InventoryOverlay:
    """Represents the inventory overlay displaying items and their quantities."""

    active: bool = False
    items: list[str] = None

    def __post_init__(self) -> None:
        if self.items is None:
            self.items = ["Fruit"]

    def draw(self, canvas: HTMLCanvasElement) -> None:
        """Draw the inventory overlay on the canvas."""

        ctx = canvas.getContext("2d", alpha=True)
        width = 300
        height = 200

        x = (canvas.width - width) // 2
        y = (canvas.height - height) // 2

        # Draw the overlay background
        ctx.fillStyle = "rgba(0, 0, 0, 0.8)"
        ctx.beginPath()
        ctx.moveTo(x + 15, y)
        ctx.lineTo(x + width - 15, y)
        ctx.quadraticCurveTo(x + width, y, x + width, y + 15)
        ctx.lineTo(x + width, y + height - 15)
        ctx.quadraticCurveTo(x + width, y + height, x + width - 15, y + height)
        ctx.lineTo(x + 15, y + height)
        ctx.quadraticCurveTo(x, y + height, x, y + height - 15)
        ctx.lineTo(x, y + 15)
        ctx.quadraticCurveTo(x, y, x + 15, y)
        ctx.closePath()
        ctx.fill()

        # Draw border
        ctx.strokeStyle = "white"
        ctx.lineWidth = 2
        ctx.stroke()