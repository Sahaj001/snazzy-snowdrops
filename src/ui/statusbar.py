from dataclasses import dataclass

from js import HTMLCanvasElement


@dataclass
class StatusBar:
    """Represents the player's status bar displaying health, intelligence, and fatigue."""

    hp: int = 100
    max_hp: int = 100
    intelligence: int = 0
    max_intelligence: int = 100
    fatigue: int = 0
    max_fatigue: int = 100
    ticks: int = 0  # in-game ticks

    def draw(self, canvas: HTMLCanvasElement, corner: str = "top_left") -> None:
        """Draw the status bar on the given canvas."""
        ctx = canvas.getContext("2d", alpha=True)
        left_padding = 15
        top_padding = 25
        font_size = 25
        time_text = format_game_time(self.ticks)
        box_width = left_padding + len(time_text) * font_size
        box_height = 4 * (font_size + 15) + top_padding

        # Calculate position of status bar based on the corner
        x, y = self._get_position(ctx, corner, left_padding)

        # Draw the overlay background
        self._draw_overlay(ctx, x, y, box_width, box_height)

        # Draw the status text and icons for health, intelligence, fatigue, and game time
        self._draw_status(
            ctx,
            x + left_padding,
            y + top_padding,
            "❤️",
            f"{self.hp}/{self.max_hp}",
            font_size,
        )
        self._draw_status(
            ctx,
            x + left_padding,
            y + top_padding + font_size + 15,
            "💡",
            f"{self.intelligence}/{self.max_intelligence}",
            font_size,
        )
        self._draw_status(
            ctx,
            x + left_padding,
            y + top_padding + 2 * (font_size + 15),
            "🔋",
            f"{self.fatigue}/{self.max_fatigue}",
            font_size,
        )
        self._draw_status(
            ctx,
            x + left_padding,
            y + top_padding + 3 * (font_size + 15),
            "⏰",
            format_game_time(self.ticks),
            font_size,
        )

    def _get_position(
        self,
        ctx: HTMLCanvasElement,
        corner: str,
        padding: int,
    ) -> tuple[int, int]:
        """Calculate the x, y position based on the corner."""
        if corner == "top_left":
            return (padding, padding)
        return (ctx.canvas.width - 220 - padding, padding)

    def _draw_overlay(
        self,
        ctx: HTMLCanvasElement,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        """Draw a subtle, rounded, semi-transparent background."""
        ctx.fillStyle = "rgba(0, 0, 0, 0.5)"  # Light transparent background
        ctx.beginPath()
        ctx.moveTo(x + 15, y)  # Rounded top-left corner
        ctx.lineTo(x + width - 15, y)
        ctx.quadraticCurveTo(
            x + width,
            y,
            x + width,
            y + 15,
        )  # Rounded top-right corner
        ctx.lineTo(x + width, y + height - 15)
        ctx.quadraticCurveTo(
            x + width,
            y + height,
            x + width - 15,
            y + height,
        )  # Rounded bottom-right corner
        ctx.lineTo(x + 15, y + height)
        ctx.quadraticCurveTo(
            x,
            y + height,
            x,
            y + height - 15,
        )  # Rounded bottom-left corner
        ctx.lineTo(x, y + 15)
        ctx.quadraticCurveTo(x, y, x + 15, y)  # Rounded top-left corner closure
        ctx.closePath()
        ctx.fill()

    def _draw_status(
        self,
        ctx: HTMLCanvasElement,
        x: int,
        y: int,
        icon: str,
        text: str,
        font_size: int,
    ) -> None:
        """Draw a simple status label with an icon and the corresponding value."""
        ctx.fillStyle = "white"
        ctx.font = f"{font_size}px Arial"
        ctx.fillText(icon, x, y)  # Draw icon
        ctx.fillText(text, x + 50, y)  # Draw text next to the icon


def format_game_time(ticks: float) -> str:
    """Convert game ticks to a formatted time string (HH:MM:SS)."""
    seconds = ticks // 1000
    minutes = seconds // 60
    hours = minutes // 60
    seconds = seconds % 60
    minutes = minutes % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
