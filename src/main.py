# Import necessary JS bindings
from js import document, window
from pyodide.ffi import create_proxy
from pyodide.http import pyfetch

from engine import (
    Camera,
    EventBus,
    GameEngine,
    InputSystem,
    RenderSystem,
    SoundSystem,
    SpriteRegistry,
)
from game import Fruit, Player, Tile, TileMap, Tree, TreeBehaviour, World
from models import Pos
from view import ViewBridge

# ==== INITIAL SETUP ====
VERTICAL_WALL_X = 5
VERTICAL_WALL_Y_START = 3
VERTICAL_WALL_Y_END = 8
HORIZONTAL_WALL_Y = 7
HORIZONTAL_WALL_X_START = 8
HORIZONTAL_WALL_X_END = 12

WORLD_WIDTH_PIXELS = 2000
WORLD_HEIGHT_PIXELS = 2000
TILE_SIZE_PIXELS = 50  # pixels

# 1. Get the HTML canvas and pass to ViewBridge
canvas = document.getElementById("gameCanvas")
canvas.width = window.innerWidth
canvas.height = window.innerHeight
input_system = InputSystem()
view_bridge = ViewBridge(canvas, input_system)

# 2. Create sprite registry
sprite_registry = SpriteRegistry()
sprite_registry.load_from_json("assets/sprites.json")

# 4. Create systems
camera = Camera(x=2, y=2, screen_w=canvas.width, screen_h=canvas.height)
render_system = RenderSystem(
    sprites=sprite_registry,
    view_bridge=view_bridge,
    camera=camera,
)
event_bus = EventBus()


# 4. Create world
# Provide an initial tiles argument (e.g., an empty list or your map data)
# Wall placement constants
def generate_tile_map() -> TileMap:
    """Generate a simple tile map for the world."""
    tile_size = TILE_SIZE_PIXELS  # Pixels per tile
    width, height = WORLD_WIDTH_PIXELS // tile_size, WORLD_HEIGHT_PIXELS // tile_size

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

    # print("Tile map generated with dimensions:", width, "x", height)
    # print("Tile map data:", game_tile_map.tiles)

    return game_tile_map


def generate_world(game_tile_map: TileMap) -> World:
    """Create a new world with the given tile map."""
    game_world = World(tiles=game_tile_map)
    # Example player
    player = Player(entity_id="player1", pos=Pos(10, 10, 0), behaviour=None)
    game_world.add_player(player)

    # Entities like tree and fruit
    for idx, fruit_pos in enumerate([(2, 2), (3, 10), (4, 3)]):
        fruit = Fruit(f"fruit_{idx}", pos=Pos(*fruit_pos, 0), behaviour=None)
        game_world.add_entity(fruit)

    for idx, tree_pos in enumerate([(3, 3), (4, 4), (5, 5)]):
        tree = Tree(f"tree_{idx}", pos=Pos(*tree_pos, 0), behaviour=TreeBehaviour())
        game_world.add_entity(tree)

    return game_world


world = generate_world(generate_tile_map())


# ==== GAME LOOP ====
def tick_frame(timestamp: float | None = None, *, engine) -> None:  # noqa: ANN001
    """Update and render the game in the main loop."""
    dt = 1 / 60  # fixed timestep for now

    # Update
    engine.tick(dt)

    # Render
    player = engine.world.get_current_player()
    engine.renderer.camera.center_on(player.pos)
    engine.render(timestamp)

    # Clear the event bus after processing
    engine.event_bus.clear()

    # Schedule next frame
    window.requestAnimationFrame(
        create_proxy(lambda timestamp: tick_frame(timestamp, engine=engine))
    )


async def start() -> None:
    sound_sys = SoundSystem(
        bgm_map=await load_json("assets/audio/bgm.json"),
        sfx_map=await load_json("assets/audio/sfx.json"),
    )
    engine = GameEngine(
        world=world,
        renderer=render_system,
        input_sys=input_system,
        event_bus=event_bus,
        sound_sys=sound_sys,
    )
    tick_frame(engine=engine)


async def load_json(path: str) -> dict:
    res = await pyfetch(path)
    return await res.json()
