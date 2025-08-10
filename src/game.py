from js import console

from engine.canvas import Canvas


def start(js_canvas, js_ctx) -> None:
    console.log("Game started")

    canvas = Canvas(js_canvas, js_ctx)

    # Example tilemap (numbers are tile indexes)
    tilemap_data = [
        [0, 1, 2, 1, 0],
        [1, 2, 3, 2, 1],
        [2, 3, 0, 3, 2],
        [1, 2, 3, 2, 1],
        [0, 1, 2, 1, 0],
    ]

    # Provide your tileset image path here
    tileset_src = "/assets/sprites/test-tile.png"
    tile_width = 32
    tile_height = 32

    tilemap = TileMap(canvas, tileset_src, tile_width, tile_height, tilemap_data)

    # Clear canvas and draw tilemap
    canvas.clear("#222")
    tilemap.draw()

    # Draw some shapes on top
    canvas.draw_rect(100, 100, 200, 150, "red")
    canvas.draw_circle(400, 300, 50, "blue")
    canvas.draw_text("Hello from Canvas class", 200, 500, "white", "24px Arial")
