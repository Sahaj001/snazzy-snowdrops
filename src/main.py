# Import necessary JS bindings
from js import document, window
from pyodide.ffi import create_proxy

from engine import (
    Camera,
    EventBus,
    GameEngine,
    InputSystem,
    RenderSystem,
    SpriteRegistry,
)
from game import Player, Tile, TileMap, World
from models import Pos
from view import ViewBridge

# ==== INITIAL SETUP ====

# 1. Get the HTML canvas and pass to ViewBridge
canvas = document.getElementById("gameCanvas")
input_system = InputSystem()
view_bridge = ViewBridge(canvas, input_system)

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
event_bus = EventBus()


# 5. Create world
# Provide an initial tiles argument (e.g., an empty list or your map data)
# Wall placement constants
VERTICAL_WALL_X = 5
VERTICAL_WALL_Y_START = 3
VERTICAL_WALL_Y_END = 8
HORIZONTAL_WALL_Y = 7
HORIZONTAL_WALL_X_START = 8
HORIZONTAL_WALL_X_END = 12


def generate_tile_map() -> TileMap:
    """Generate a simple tile map for the world."""
    width, height = 20, 15  # Map size in tiles
    tile_size = 32  # Pixels per tile

    tile_map = TileMap(width, height, tile_size)

    for y in range(height):
        for x in range(width):
            # Create different tile types based on position
            if y == 0 or y == height - 1 or x == 0 or x == width - 1:
                # Border walls
                tile = Tile("wall", passable=False, z=1)
            elif x == VERTICAL_WALL_X and VERTICAL_WALL_Y_START <= y <= VERTICAL_WALL_Y_END:
                # Vertical wall
                tile = Tile("wall", passable=False, z=1)
            elif y == HORIZONTAL_WALL_Y and HORIZONTAL_WALL_X_START <= x <= HORIZONTAL_WALL_X_END:
                # Horizontal wall
                tile = Tile("wall", passable=False, z=1)
            elif (x + y) % 3 == 0:
                # Some decorative stones
                tile = Tile("stone", passable=True, z=0)
            elif x % 4 == 0 and y % 3 == 0:
                # Trees
                tile = Tile("tree", passable=False, z=1)
            else:
                # Default grass tiles
                tile = Tile("grass", passable=True, z=0)

            tile_map.set(x, y, tile)

    return tile_map


# Generate the tile map
tile_map = generate_tile_map()

world = World(tiles=tile_map)

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


def tick_frame(_timestamp: float | None = None) -> None:
    """Update and render the game in the main loop."""
    dt = 1 / 60  # fixed timestep for now

    # Update
    engine.tick(dt)

    # Render
    engine.render()

    # Schedule next frame
    window.requestAnimationFrame(create_proxy(tick_frame))


# ==== START GAME ====
tick_frame()
