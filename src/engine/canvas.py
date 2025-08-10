class Canvas:
    def __init__(self, canvas, ctx) -> None:
        self.canvas = canvas
        self.ctx = ctx
        self.width = canvas.width
        self.height = canvas.height

    def clear(self, color="#000") -> None:
        """Clear the entire canvas with a background color."""
        self.ctx.fillStyle = color
        self.ctx.fillRect(0, 0, self.width, self.height)

    def draw_rect(self, x, y, w, h, color="#FFF") -> None:
        """Draw a filled rectangle."""
        self.ctx.fillStyle = color
        self.ctx.fillRect(x, y, w, h)

    def draw_text(self, text, x, y, color="#FFF", font="20px Arial") -> None:
        """Draw text on the canvas."""
        self.ctx.fillStyle = color
        self.ctx.font = font
        self.ctx.fillText(text, x, y)

    def draw_circle(self, x, y, radius, color="#FFF") -> None:
        """Draw a filled circle."""
        self.ctx.beginPath()
        self.ctx.arc(x, y, radius, 0, 2 * 3.14159)
        self.ctx.fillStyle = color
        self.ctx.fill()

    def draw_sprite(self, image, sx, sy, sw, sh, dx, dy, dw, dh) -> None:
        self.ctx.drawImage(image, sx, sy, sw, sh, dx, dy, dw, dh)
