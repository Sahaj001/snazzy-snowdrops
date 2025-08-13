from js import window, canvas
from config import WIDNOW_RATIO

def resize_canvas():
    """Resize canvas based on window size and fixed game ratio."""
    window_ratio = window.innerWidth / window.innerHeight
    if window_ratio > WIDNOW_RATIO:
        canvas.height = window.innerHeight
        canvas.width = window.innerHeight * WIDNOW_RATIO
    else:
        canvas.width = window.innerWidth
        canvas.height = window.innerWidth / WIDNOW_RATIO
    
    # Center the canvas
    canvas.style.position = "absolute"
    canvas.style.left = f"{(window.innerWidth - canvas.width) / 2}px"
    canvas.style.top = f"{(window.innerHeight - canvas.height) / 2}px"
    
    return canvas.width, canvas.height
