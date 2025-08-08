import js


def setup_canvas() -> js.JSObject:
    """Initialize canvas and fill with red background."""
    # Get canvas and set size to fill window
    canvas = js.canvas
    canvas.width = js.window.innerWidth
    canvas.height = js.window.innerHeight

    # Get 2D context and fill with red
    ctx = canvas.getContext("2d")
    ctx.fillStyle = "green"
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    print("Canvas setup complete - red background applied")
    return ctx


def resize_canvas() -> None:
    """Handle canvas resize and maintain green background."""
    canvas = js.canvas
    canvas.width = js.window.innerWidth
    canvas.height = js.window.innerHeight
    ctx = canvas.getContext("2d")
    ctx.fillStyle = "red"
    ctx.fillRect(0, 0, canvas.width, canvas.height)


# Initialize when module is imported
ctx = setup_canvas()
