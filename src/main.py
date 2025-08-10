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
from game import Fruit, Player, Tile, TileMap, Tree, TreeBehaviour, World
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
    tile_size = 10  # Pixels per tile
    width, height = (
        canvas.width // tile_size,
        canvas.height // tile_size,
    )  # Map size in tiles

    game_tile_map = TileMap(width, height, tile_size)

    for y in range(height):
        for x in range(width):
            if (
                x == 0
                or x == width - 1
                or y == 0
                or y == height - 1
                or (x == VERTICAL_WALL_X and VERTICAL_WALL_Y_START <= y <= VERTICAL_WALL_Y_END)
                or (y == HORIZONTAL_WALL_Y and HORIZONTAL_WALL_X_START <= x <= HORIZONTAL_WALL_X_END)
            ):
                tile = Tile("wall", passable=False, z=1)
            else:
                tile = Tile("grass", passable=True, z=0)

            game_tile_map.set(x, y, tile)

    print("Tile map generated with dimensions:", width, "x", height)
    print("Tile map data:", game_tile_map.tiles)

    return game_tile_map


def get_world(game_tile_map: TileMap) -> World:
    """Create a new world with the given tile map."""
    game_world = World(tiles=game_tile_map)
    # Example player
    player = Player(entity_id="player1", pos=Pos(1, 1, 0), behaviour=None)
    game_world.add_player(player)

    # Entities like tree and fruit
    fruit = Fruit("fruit1", pos=Pos(12, 2, 0), behaviour=None)
    game_world.add_entity(fruit)

    for idx, tree_pos in enumerate([(3, 3), (4, 4), (5, 5)]):
        tree = Tree(f"tree_{idx}", pos=Pos(*tree_pos, 0), behaviour=TreeBehaviour())
        game_world.add_entity(tree)

    game_world.players.append(player)
    game_world.entities.append(player)

    return game_world


world = get_world(generate_tile_map())


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
