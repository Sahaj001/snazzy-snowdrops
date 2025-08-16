from __future__ import annotations

from dataclasses import dataclass, field

from js import HTMLCanvasElement, document
Inventory: "Inventory"  # Forward reference for type hinting


@dataclass
class InventoryOverlay:
    """Represents the inventory overlay displaying items and their quantities."""

    active: bool = False
    overlay_canvas: "HTMLCanvasElement" = field(
        default_factory=lambda: document.getElementById("inventoryCanvas")
    )
    main_canvas: "HTMLCanvasElement" = field(
        default_factory=lambda: document.getElementById("gameCanvas")
    )

    def __init__(self, inventory: Inventory) -> None:
        self.inventory = inventory

    def __post_init__(self) -> None:
        if self.items is None:
            self.items = ["Fruit"]

        self.overlay_canvas.style.position = "absolute"
        self.overlay_canvas.style.top = "0px"
        self.overlay_canvas.style.left = "0px"
        self.overlay_canvas.style.zIndex = "100"
        self.overlay_canvas.style.pointerEvents = "none"
        self.overlay_canvas.width = self.main_canvas.width
        self.overlay_canvas.height = self.main_canvas.height

    def draw(self, canvas: HTMLCanvasElement) -> None:
        """Draw the inventory overlay on the canvas."""

        if not self.active:
            self.overlay_canvas.style.display = "none"
            return
        else:
            self.overlay_canvas.style.display = "block"

        ctx = self.overlay_canvas.getContext("2d", alpha=True)
        width = 310
        height = 200

        x = (self.overlay_canvas.width - width) // 2
        y = (self.overlay_canvas.height - height) // 2

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

        # Draw title text
        ctx.fillStyle = "white"
        ctx.font = "20px Arial"
        ctx.textAlign = "center"
        ctx.fillText("Inventory", x + width // 2, y + 30)


        test_items = [
        {"color": "red", "quantity": 1},
        {"color": "green", "quantity": 2},
        {"color": "blue", "quantity": 1},
        {"color": "yellow", "quantity": 3},
        {"color": "purple", "quantity": 1},
        {"color": "orange", "quantity": 5},
        {"color": "pink", "quantity": 2},
        {"color": "cyan", "quantity": 1},
        {"color": "brown", "quantity": 4},
        {"color": "gray", "quantity": 1},
        {"color": "black", "quantity": 2},
        {"color": "white", "quantity": 3},
        {"color": "gold", "quantity": 1},
        {"color": "silver", "quantity": 2},
        {"color": "teal", "quantity": 1},
        {"color": "lime", "quantity": 3},
        {"color": "navy", "quantity": 1},
        {"color": "maroon", "quantity": 2},
        ]

        cols = 6
        item_size = 40
        padding = 10
        start_x = x + padding
        start_y = y + 50

        for idx, item in enumerate(test_items):
            col = idx % cols
            row = idx // cols
            item_x = start_x + col * (item_size + padding)
            item_y = start_y + row * (item_size + padding)

            # Draw item box
            ctx.fillStyle = item["color"]
            ctx.fillRect(item_x, item_y, item_size, item_size)

            # Draw quantity if more than 1
            if item["quantity"] > 1:
                ctx.fillStyle = "white"
                ctx.font = "12px Arial"
                ctx.fillText(str(item["quantity"]), item_x + item_size - 10, item_y + item_size - 5)
