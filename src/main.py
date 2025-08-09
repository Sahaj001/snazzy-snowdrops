from js import console, document, window
from pyodide.ffi import create_proxy

console.log("Python script started ✅")

canvas = document.getElementById("gameCanvas")
ctx = canvas.getContext("2d")

if ctx is None:
    console.error("Canvas context is None ❌")
else:
    console.log("Canvas context acquired ✅")


class BouncingSquare:
    """A simple bouncing square game object."""

    def __init__(self, x: int, y: int, vx: float, vy: float, size: int = 30) -> None:
        """Initialize the bouncing square."""
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.color = "red"

    def update(self) -> None:
        """Update the square's position and handle bouncing."""
        # Update position
        self.x += self.vx
        self.y += self.vy

        # Bounce off walls
        if self.x < 0 or self.x > canvas.width - self.size:
            self.vx = -self.vx
        if self.y < 0 or self.y > canvas.height - self.size:
            self.vy = -self.vy

    def draw(self) -> None:
        """Draw the square on the canvas."""
        ctx.fillStyle = self.color
        ctx.fillRect(self.x, self.y, self.size, self.size)


# Create bouncing square instance
bouncing_square = BouncingSquare(50, 50, 2, 1.5)


def game_loop(_timestamp: float) -> None:
    """Run the main game loop animation."""
    # Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    # Update and draw bouncing square
    bouncing_square.update()
    bouncing_square.draw()

    # Schedule next frame
    window.requestAnimationFrame(game_loop_proxy)


# Create a persistent proxy for the loop function
game_loop_proxy = create_proxy(game_loop)

# Start the loop
window.requestAnimationFrame(game_loop_proxy)
