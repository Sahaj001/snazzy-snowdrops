from typing import Any

is_mouse_down: bool = False
mouse_x: int = 0
mouse_y: int = 0
mouse_capture: str | None = None


def on_mouse_move(event: Any) -> None:
    global mouse_x, mouse_y
    mouse_x = event.clientX
    mouse_y = event.clientY


def on_mouse_down() -> None:
    global is_mouse_down
    is_mouse_down = True


def on_mouse_up() -> None:
    global is_mouse_down
    is_mouse_down = False


def update_mouse() -> None:
    global mouse_capture
    if not is_mouse_down:
        mouse_capture = None


def capture_mouse(id: str) -> bool:
    global mouse_capture
    if is_mouse_down and mouse_capture is None:
        mouse_capture = id
        return True
    return False
