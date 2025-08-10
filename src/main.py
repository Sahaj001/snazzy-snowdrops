# main.py — Entry point for running in Pyodide with HTML canvas

# Import necessary JS bindings
from js import document, requestAnimationFrame
from pyodide.ffi import create_proxy

from engine import (
    Camera,
    EventBus,
    GameEngine,
    InputSystem,
    RenderSystem,
    SpriteRegistry,
)
from game import Player, World
from models import Pos
from view import ViewBridge

# ==== INITIAL SETUP ====

# 1. Get the HTML canvas and pass to ViewBridge
canvas = document.getElementById("gameCanvas")
view_bridge = ViewBridge(canvas)

# 2. Load sprite assets
view_bridge.load_assets("assets/sprites.json")

# 3. Create sprite registry
sprite_registry = SpriteRegistry()
sprite_registry.load_from_json("assets/sprites.json")

# 4. Create systems
camera = Camera(x=0, y=0, screen_w=canvas.width, screen_h=canvas.height)
render_system = RenderSystem(
    sprites=sprite_registry,
    view_bridge=view_bridge,
    camera=camera,
)
input_system = InputSystem(view_bridge=view_bridge)
event_bus = EventBus()

# 5. Create world
# Provide an initial tiles argument (e.g., an empty list or your map data)
world = World(tiles=[])

# Example player
player = Player(entity_id="player1", pos=Pos(5, 5, 0), behaviour=None)
world.players.append(player)
world.entities.append(player)

# 6. Create game engine
engine = GameEngine(
    world=world,
    renderer=render_system,
    input_sys=input_system,
    event_bus=event_bus,
)

# ==== GAME LOOP ====


def tick_frame(_timestamp: float) -> None:
    """Update and render the game in the main loop."""
    dt = 1 / 60  # fixed timestep for now

    # Update
    engine.tick(dt)

    # Render
    engine.render()

    # Schedule next frame
    requestAnimationFrame(create_proxy(tick_frame))


# ==== START GAME ====
requestAnimationFrame(create_proxy(tick_frame))
