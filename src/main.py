# Import necessary JS bindings
import js
import random

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

PLAYER_Z = 1  # Player's z-index for rendering
FRUIT_Z = 2
TREE_Z = 3  # Tree's z-index for rendering
WALL_Z = 1  # Wall's z-index for rendering
GRASS_Z = 0  # Grass z-index for rendering


def generate_tile_map() -> TileMap:
    """Generate a larger tile map with perimeter walls and random internal walls."""
    tile_size = TILE_SIZE_PIXELS
    width, height = WORLD_WIDTH_PIXELS // tile_size, WORLD_HEIGHT_PIXELS // tile_size

    game_tile_map = TileMap(width, height, tile_size)

    # Set random seed for consistent world generation
    random.seed(42)

    for y in range(height):
        for x in range(width):
            # Perimeter walls
            if x == 0 or x == width - 1:
                tile = Tile("horizontal_wall", passable=False, z=WALL_Z)
            elif y == 0 or y == height - 1:
                tile = Tile("vertical_wall", passable=False, z=WALL_Z)
            # Random internal walls (sparse distribution)
            elif random.random() < 0.08:  # 8% chance of wall
                tile = Tile("horizontal_wall", passable=False, z=WALL_Z)
            else:
                tile = Tile("grass", passable=True, z=GRASS_Z)

            game_tile_map.set(x, y, tile)

    # Create some guaranteed pathways to prevent isolated areas
    # Horizontal pathways
    for pathway_y in range(10, height - 10, 15):
        for x in range(1, width - 1):
            game_tile_map.set(x, pathway_y, Tile("grass", passable=True, z=GRASS_Z))

    # Vertical pathways
    for pathway_x in range(10, width - 10, 15):
        for y in range(1, height - 1):
            game_tile_map.set(pathway_x, y, Tile("grass", passable=True, z=GRASS_Z))

    print(f"Large tile map generated with dimensions: {width} x {height}")
    return game_tile_map


def generate_world(game_tile_map: TileMap) -> World:
    """Create a new world with the given tile map and random entities."""
    game_world = World(tiles=game_tile_map)

    # Player in center of world
    center_x = WORLD_WIDTH_PIXELS // 2
    center_y = WORLD_HEIGHT_PIXELS // 2
    player = Player(
        entity_id="player1",
        pos=Pos(center_x, center_y, PLAYER_Z),
        behaviour=None,
    )
    game_world.add_player(player)

    random.seed(123)

    # Generate random fruits across the world
    num_fruits = 50
    for idx in range(num_fruits):
        # Avoid placing near edges
        x = (
            random.randint(3, (WORLD_WIDTH_PIXELS // TILE_SIZE_PIXELS) - 3)
            * TILE_SIZE_PIXELS
        )
        y = (
            random.randint(3, (WORLD_HEIGHT_PIXELS // TILE_SIZE_PIXELS) - 3)
            * TILE_SIZE_PIXELS
        )

        tile_x, tile_y = x // TILE_SIZE_PIXELS, y // TILE_SIZE_PIXELS
        if game_tile_map.get(tile_x, tile_y).passable:
            fruit = Fruit(f"fruit_{idx}", pos=Pos(x, y, FRUIT_Z), behaviour=None)
            game_world.add_entity(fruit)

    # Generate random trees
    num_trees = 30
    for idx in range(num_trees):
        x = (
            random.randint(5, (WORLD_WIDTH_PIXELS // TILE_SIZE_PIXELS) - 5)
            * TILE_SIZE_PIXELS
        )
        y = (
            random.randint(5, (WORLD_HEIGHT_PIXELS // TILE_SIZE_PIXELS) - 5)
            * TILE_SIZE_PIXELS
        )

        tile_x, tile_y = x // TILE_SIZE_PIXELS, y // TILE_SIZE_PIXELS
        if game_tile_map.get(tile_x, tile_y).passable:
            tree = Tree(
                f"tree_{idx}",
                pos=Pos(x, y, TREE_Z),
                behaviour=TreeBehaviour(),
            )
            game_world.add_entity(tree)

    print(f"World generated with {num_fruits} fruits and {num_trees} trees")
    return game_world


world = generate_world(generate_tile_map())


async def create_engine() -> GameEngine:
    """Create and return the game engine."""
    # Ensure all systems are initialized
    await load_json("assets/audio/bgm.json")
    await load_json("assets/audio/sfx.json")

    canvas = document.getElementById("gameCanvas")
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
    input_system = InputSystem()
    view_bridge = ViewBridge(canvas, input_system)

    sprite_registry = SpriteRegistry()
    sprite_registry.load_from_json("assets/sprites.json")

    # 4. Create systems
    camera = Camera(
        x=2,
        y=2,
        screen_w=canvas.width,
        screen_h=canvas.height,
        world_max_x=WORLD_HEIGHT_PIXELS,
        world_max_y=WORLD_WIDTH_PIXELS,
    )
    render_system = RenderSystem(
        sprites=sprite_registry,
        view_bridge=view_bridge,
        camera=camera,
    )
    event_bus = EventBus()
    world = generate_world(generate_tile_map())

    sound_sys = SoundSystem(
        bgm_map=await load_json("assets/audio/bgm.json"),
        sfx_map=await load_json("assets/audio/sfx.json"),
    )
    return GameEngine(
        world=world,
        renderer=render_system,
        input_sys=input_system,
        event_bus=event_bus,
        sound_sys=sound_sys,
    )


def on_resize(engine: GameEngine) -> None:
    """Handle window resize events to update canvas and camera."""
    # Update canvas size
    engine.renderer.view_bridge.canvas.width = document.documentElement.clientWidth
    engine.renderer.view_bridge.canvas.height = document.documentElement.clientHeight

    # Update camera viewport
    engine.renderer.camera.screen_w = engine.renderer.view_bridge.canvas.width
    engine.renderer.camera.screen_h = engine.renderer.view_bridge.canvas.height


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
    """Initialize the game engine and start the game loop."""
    engine = await create_engine()

    def handle_resize(event: js.Event) -> None:
        """Handle window resize events."""
        on_resize(engine)

    window.addEventListener("resize", create_proxy(handle_resize))

    tick_frame(engine=engine)


async def load_json(path: str) -> dict:
    res = await pyfetch(path)
    return await res.json()
