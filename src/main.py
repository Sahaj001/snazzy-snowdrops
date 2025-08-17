# Import necessary JS bindings
import random

from js import Event, document, performance, window
from pyodide.ffi import create_proxy
from pyodide.http import pyfetch

from engine import (
    Camera,
    EventBus,
    GameEngine,
    InputSystem,
    RenderSystem,
    SoundSystem,
)
from engine.settings import Settings
from engine.state import DelayState
from game import Fruit, Player, World, Zombie
from models import Pos, SpriteRegistry, TileMap, TilesRegistry
from view import ViewBridge

# ==== INITIAL SETUP ====

PLAYER_Z = 2  # Player's z-index for rendering
FRUIT_Z = 1


async def create_player(tile_map: TileMap) -> Player:
    """Add a player to the world at the center position."""
    player_sprite_registry_json = await load_json("assets/db/player.json")
    player_sprite_registry = SpriteRegistry.load_from_json(player_sprite_registry_json)
    player_x, player_y = tile_map.player_spawn

    return Player(
        entity_id="player1",
        pos=Pos(player_x, player_y, PLAYER_Z),
        behaviour=None,
        hp=5,
        fatigue=20,
        sprite_registry=player_sprite_registry,
    )


async def create_zombies(tile_map: TileMap) -> list[Zombie]:
    """Add a zombie to the world at the center position."""
    zombie_sprite_registry_json = await load_json("assets/db/zombie.json")
    zombie_sprite_registry = SpriteRegistry.load_from_json(zombie_sprite_registry_json)
    zombies = []
    zombie_spawn_positions = set(tile_map.zombie_spawns)
    for i, spawn in enumerate(zombie_spawn_positions):
        tile_x, tile_y = spawn
        # Ensure the zombie spawns at the tile center
        zombie_x = tile_x + tile_map.tile_size // 2
        zombie_y = tile_y + tile_map.tile_size // 2

        zombie = Zombie(
            zombie_id=f"zombie_{i}",
            pos=Pos(x=zombie_x, y=zombie_y, z=PLAYER_Z),
            behaviour=None,
            sprite_registry=zombie_sprite_registry,
        )
        zombies.append(zombie)

    return zombies


async def create_fruits(tile_map: TileMap, num_fruits: int = 5) -> list[Fruit]:
    """Add a specified number of fruits to the world at random positions."""
    fruit_registry_json = await load_json("assets/db/fruit.json")
    fruit_registry = SpriteRegistry.load_from_json(fruit_registry_json)
    fruits = []
    fruit_positions = set(tile_map.fruit_spawns)
    for i in range(num_fruits):
        fruit_spawn = random.choice(list(fruit_positions))
        tile_x, tile_y = fruit_spawn
        # Ensure the fruit spawns at the tile center
        fruit_x = tile_x + tile_map.tile_size // 2
        fruit_y = tile_y + tile_map.tile_size // 2
        fruit_positions.remove(fruit_spawn)  # Avoid duplicate spawns

        fruit = Fruit(
            fruit_id=f"fruit_{i}",
            pos=Pos(
                x=fruit_x,
                y=fruit_y,
                z=FRUIT_Z,
            ),
            behaviour=None,
            sprite_registry=fruit_registry,
        )
        fruits.append(fruit)

    return fruits


async def create_engine(sound_sys: SoundSystem) -> GameEngine:
    """Create and return the game engine."""
    # Ensure all systems are initialized
    await load_json("assets/audio/bgm.json")
    await load_json("assets/audio/sfx.json")

    canvas = document.getElementById("gameCanvas")
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
    input_system = InputSystem()

    tiled = await load_json("assets/tilemap/cj.tmj")

    tile_registry = TilesRegistry.load_from_tiled(
        directory="assets/tilemap/",
        tiled=tiled,
    )

    tile_map = TileMap.load_from_tiled(tiled)

    world_width_pixels = tile_map.width * tile_map.tile_size
    world_height_pixels = tile_map.height * tile_map.tile_size

    player = await create_player(tile_map)
    fruits = await create_fruits(tile_map, num_fruits=5)
    zombies = await create_zombies(tile_map)
    world = World(player, fruits, zombies, tile_map=tile_map)

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
        view_bridge=view_bridge,
        camera=camera,
    )
    event_bus = EventBus()

    settings = Settings(
        event_bus=event_bus,
        sound_system=sound_sys,
    )

    return GameEngine(
        world=world,
        renderer=render_system,
        input_sys=input_system,
        event_bus=event_bus,
        sound_sys=sound_sys,
        settings=settings,
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
def tick_frame(engine: GameEngine, timestamp: float, lf_timestamp: float = 0) -> None:
    """Update and render the game in the main loop."""
    dt = 1 / 60  # fixed timestep for now

    engine.tick(dt)

    # Handle Camera
    player = engine.world.get_current_player()
    engine.renderer.camera.center_on(player.pos)

    # Render
    engine.render(timestamp - DelayState.get_delay())

    # Clear the event bus after processing
    engine.event_bus.clear()

    if engine.settings.game_state.is_paused():
        DelayState.accum_delay(timestamp - lf_timestamp)

    # Schedule next frame
    window.requestAnimationFrame(
        create_proxy(
            lambda _: tick_frame(
                engine=engine,
                timestamp=performance.now(),
                lf_timestamp=timestamp,
            ),
        ),
    )


async def start() -> None:
    """Initialize the game engine and start the game loop."""
    sound_sys = SoundSystem(
        bgm_map=await load_json("assets/audio/bgm.json"),
        sfx_map=await load_json("assets/audio/sfx.json"),
    )

    engine = await create_engine(sound_sys)

    engine.settings.main_menu.make_visible()

    def handle_resize(_event: Event) -> None:
        """Handle window resize events."""
        on_resize(engine)

    window.addEventListener("resize", create_proxy(handle_resize))

    tick_frame(engine=engine, timestamp=0)


async def load_json(path: str) -> dict:
    res = await pyfetch(path)
    return await res.json()
