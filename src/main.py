# Import necessary JS bindings
import random

import js
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
from game import Fruit, Player, World
from models import Pos, TileMap, TilesRegistry
from view import ViewBridge

# ==== INITIAL SETUP ====

PLAYER_Z = 1  # Player's z-index for rendering
FRUIT_Z = 2


def add_player_to_world(world: World) -> None:
    """Add a player to the world at the center position."""
    world_width_pixels = world.tile_map.width * world.tile_map.tile_size
    world_height_pixels = world.tile_map.height * world.tile_map.tile_size
    player = Player(
        entity_id="player1",
        pos=Pos(world_width_pixels // 2, world_height_pixels // 2, PLAYER_Z),
        behaviour=None,
        hp=40,
        fatigue=20,
    )
    world.add_player(player)


def add_fruits_to_world(world: World, num_fruits: int = 5) -> None:
    """Add a specified number of fruits to the world at random positions."""
    for i in range(num_fruits):
        tile_x = random.randint(0, world.tile_map.width - 1)
        tile_y = random.randint(0, world.tile_map.height - 1)
        fruit = Fruit(
            fruit_id=f"fruit_{i}",
            pos=Pos(
                tile_x * world.tile_map.tile_size,
                tile_y * world.tile_map.tile_size,
                FRUIT_Z,
            ),
            behaviour=None,
        )
        world.add_entity(fruit)


async def create_engine() -> GameEngine:
    """Create and return the game engine."""
    # Ensure all systems are initialized
    await load_json("assets/audio/bgm.json")
    await load_json("assets/audio/sfx.json")

    canvas = document.getElementById("gameCanvas")
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
    input_system = InputSystem()

    sprite_registry = SpriteRegistry()
    sprite_registry.load_from_json("assets/sprites.json")

    tiled = await load_json("assets/tilemap/cj.tmj")

    tile_registry = TilesRegistry.load_from_tiled(
        directory="assets/tilemap/",
        tiled=tiled,
    )

    tile_map = TileMap.load_from_tiled(tiled)

    world = World(tile_map=tile_map)
    world_width_pixels = tile_map.width * tile_map.tile_size
    world_height_pixels = tile_map.height * tile_map.tile_size

    add_player_to_world(world)
    add_fruits_to_world(world, num_fruits=5)

    camera = Camera(
        x=2,
        y=2,
        screen_w=canvas.width,
        screen_h=canvas.height,
        world_max_y=world_height_pixels,
        world_max_x=world_width_pixels,
        zoom=1.25,
    )

    view_bridge = ViewBridge(canvas, input_system, tile_registry)
    render_system = RenderSystem(
        sprites=sprite_registry,
        view_bridge=view_bridge,
        camera=camera,
    )
    event_bus = EventBus()

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
        create_proxy(lambda timestamp: tick_frame(timestamp, engine=engine)),
    )


async def start() -> None:
    """Initialize the game engine and start the game loop."""
    engine = await create_engine()

    def handle_resize(_event: js.Event) -> None:
        """Handle window resize events."""
        on_resize(engine)

    window.addEventListener("resize", create_proxy(handle_resize))

    tick_frame(timestamp=0, engine=engine)


async def load_json(path: str) -> dict:
    res = await pyfetch(path)
    return await res.json()
