from js import Image, document, window

from engine.canvas import Canvas
from engine.sprites import SpriteSheet


class Game:
    def __init__(self) -> None:
        self.canvas_elem = document.getElementById("gameCanvas")
        self.ctx = self.canvas_elem.getContext("2d")
        self.canvas = Canvas(self.canvas_elem, self.ctx)

        self.tileset_image = Image.new()
        self.tileset_image.src = "/assets/tileset.png"  # make sure path is correct

        # Tile size in pixels
        self.tile_width = 32
        self.tile_height = 32

        self.tileset = None  # will init after image loads
        self.tilemap = [
            [0, 1, 2, 3, 0, 1, 2, 3, 0, 1],
            [1, 2, 3, 0, 1, 2, 3, 0, 1, 2],
            # Add more rows as needed to fill your canvas
        ]

    def on_tileset_loaded(self, _event) -> None:
        self.tileset = SpriteSheet(self.tileset_image, self.tile_width, self.tile_height)
        self.start_game_loop()

    def start_game_loop(self) -> None:
        def loop(timestamp=None) -> None:
            self.update()
            self.render()
            window.requestAnimationFrame(loop)

        window.requestAnimationFrame(loop)

    def update(self) -> None:
        # TODO: update game state here (animations, input, etc)
        pass

    def render(self) -> None:
        # Clear canvas each frame
        self.ctx.clearRect(0, 0, self.canvas_elem.width, self.canvas_elem.height)

        # Draw tiles covering whole canvas
        for row_idx, row in enumerate(self.tilemap):
            for col_idx, tile_index in enumerate(row):
                x = col_idx * self.tile_width
                y = row_idx * self.tile_height
                self.canvas.draw_sprite_tile(self.tileset, tile_index, x, y)

        # Draw a red rectangle on top (example)
        self.ctx.fillStyle = "red"
        self.ctx.fillRect(50, 50, 100, 100)


game_instance = None


def start() -> None:
    global game_instance
    game_instance = Game()
    game_instance.tileset_image.onload = game_instance.on_tileset_loaded
