from pyodide.ffi import create_proxy

import js


class Sprite:
    """A sprite that can be drawn on the canvas."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: str = "red",
    ) -> None:
        """Initialize a sprite."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.visible = True

    def draw(self, ctx: js.CanvasRenderingContext2D) -> None:
        """Draw the sprite on the canvas."""
        if self.visible:
            ctx.fillStyle = self.color
            ctx.fillRect(self.x, self.y, self.width, self.height)


class ImageSprite(Sprite):
    """A sprite that uses an image."""

    def __init__(
        self,
        x: int,
        y: int,
        image_url: str,
        width: int | None = None,
        height: int | None = None,
    ) -> None:
        """Initialize an image sprite."""
        super().__init__(x, y, width or 32, height or 32)
        self.image_url = image_url
        self.image = None
        self.loaded = False
        self.load_image()

    def load_image(self) -> None:
        """Load the image from URL."""
        img = js.Image.new()

        def on_load(_event: js.Event) -> None:
            self.loaded = True
            if not self.width:
                self.width = img.width
            if not self.height:
                self.height = img.height
            print(f"Image loaded: {self.image_url}")

        def on_error(_event: js.Event) -> None:
            print(f"Failed to load image: {self.image_url}")
            # Fallback to colored rectangle
            self.loaded = True

        img.onload = create_proxy(on_load)
        img.onerror = create_proxy(on_error)
        img.src = self.image_url
        self.image = img

    def draw(self, ctx: js.CanvasRenderingContext2D) -> None:
        """Draw the image sprite on the canvas."""
        if self.visible and self.loaded:
            if self.image and hasattr(self.image, "complete") and self.image.complete:
                ctx.drawImage(self.image, self.x, self.y, self.width, self.height)
            else:
                # Fallback to colored rectangle
                ctx.fillStyle = self.color or "purple"
                ctx.fillRect(self.x, self.y, self.width, self.height)


class World:
    """A 2D world that contains sprites."""

    def __init__(self, width: int, height: int) -> None:
        """Initialize the world."""
        self.width = width
        self.height = height
        self.sprites = []
        self.background_color = "darkgreen"

        # Create some example sprites
        self.create_world()

    def create_world(self) -> None:
        """Create the initial world with sprites."""
        # Add some trees (green rectangles)
        for i in range(5):
            tree = Sprite(100 + i * 150, 300, 30, 80, "black")
            self.add_sprite(tree)

        # Add some rocks (gray circles - drawn as squares for now)
        for i in range(3):
            rock = Sprite(200 + i * 200, 400, 25, 25, "gray")
            self.add_sprite(rock)

        # Add a house (brown rectangle with red roof)
        house_base = Sprite(400, 250, 100, 60, "brown")
        house_roof = Sprite(380, 230, 140, 30, "red")
        self.add_sprite(house_base)
        self.add_sprite(house_roof)

    def add_sprite(self, sprite: Sprite) -> None:
        """Add a sprite to the world."""
        self.sprites.append(sprite)

    def remove_sprite(self, sprite: Sprite) -> None:
        """Remove a sprite from the world."""
        if sprite in self.sprites:
            self.sprites.remove(sprite)

    def update(self) -> None:
        """Update all sprites in the world."""
        # Add any world logic here (sprite animations, physics, etc.)

    def draw(self, ctx: js.CanvasRenderingContext2D) -> None:
        """Draw the world and all sprites."""
        # Draw background
        ctx.fillStyle = self.background_color
        ctx.fillRect(0, 0, self.width, self.height)

        # Draw all sprites
        for sprite in self.sprites:
            sprite.draw(ctx)

    def resize(self, new_width: int, new_height: int) -> None:
        """Handle world resize."""
        self.width = new_width
        self.height = new_height


class Player(Sprite):
    """A player sprite that can move around."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize the player."""
        super().__init__(x, y, 32, 32, "blue")
        self.speed = 3
        self.keys_pressed = set()

    def handle_input(self) -> None:
        """Handle player input for movement."""
        # This would be connected to keyboard events
        if "ArrowLeft" in self.keys_pressed or "a" in self.keys_pressed:
            self.x -= self.speed
        if "ArrowRight" in self.keys_pressed or "d" in self.keys_pressed:
            self.x += self.speed
        if "ArrowUp" in self.keys_pressed or "w" in self.keys_pressed:
            self.y -= self.speed
        if "ArrowDown" in self.keys_pressed or "s" in self.keys_pressed:
            self.y += self.speed

        # Keep player within world bounds
        self.x = max(0, min(self.x, world.width - self.width))
        self.y = max(0, min(self.y, world.height - self.height))

    def update(self) -> None:
        """Update player."""
        self.handle_input()


def setup_canvas() -> tuple:
    """Initialize canvas and fill with background."""
    canvas = js.canvas
    canvas.width = js.window.innerWidth
    canvas.height = js.window.innerHeight

    ctx = canvas.getContext("2d")
    print("Canvas setup complete")
    return ctx, canvas


def animate(_timestamp: float | None = None) -> None:
    """Animate the game loop."""
    canvas = js.canvas
    ctx = canvas.getContext("2d")

    # Update world and player
    world.update()
    player.update()

    # Clear canvas and draw world
    world.draw(ctx)

    # Draw player on top
    player.draw(ctx)

    # Request next frame
    js.window.requestAnimationFrame(create_proxy(animate))


def resize_canvas() -> None:
    """Handle canvas resize and update world boundaries."""
    canvas = js.canvas
    canvas.width = js.window.innerWidth
    canvas.height = js.window.innerHeight

    # Update world dimensions
    world.resize(canvas.width, canvas.height)

    print(f"World resized to: {canvas.width}x{canvas.height}")


def setup_input() -> None:
    """Set up keyboard input handling."""

    def on_keydown(event: js.KeyboardEvent) -> None:
        player.keys_pressed.add(event.key)
        event.preventDefault()

    def on_keyup(event: js.KeyboardEvent) -> None:
        player.keys_pressed.discard(event.key)
        event.preventDefault()

    js.document.addEventListener("keydown", create_proxy(on_keydown))
    js.document.addEventListener("keyup", create_proxy(on_keyup))


# Initialize when module is imported
ctx, canvas = setup_canvas()
world = World(canvas.width, canvas.height)
player = Player(100, 100)

# Setup input handling
setup_input()

# Start animation
animate()
