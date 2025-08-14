from collections import defaultdict
from dataclasses import dataclass

from js import HTMLCanvasElement, Image

from models import DrawCmd


@dataclass
class Tileset:
    """Represents a tileset used in the game world."""

    name: str
    image: Image
    firstgid: int
    columns: int
    tilewidth: int
    tileheight: int
    tilecount: int


@dataclass
class TilesRegistry:
    """Registry for managing multiple tilesets."""

    tilesets: list[Tileset] = None

    @classmethod
    def load_from_tiled(cls, directory: str, tiled: dict) -> "TilesRegistry":
        """Load tilesets from a Tiled JSON object."""
        result = []
        for ts in tiled["tilesets"]:
            image = Image.new()
            image.src = f"{directory}{ts['image']}"
            tileset = Tileset(
                name=ts["name"],
                image=image,
                firstgid=ts["firstgid"],
                columns=ts["columns"],
                tilewidth=ts["tilewidth"],
                tileheight=ts["tileheight"],
                tilecount=ts["tilecount"],
            )
            result.append(tileset)

        return cls(tilesets=result)

    def draw_tile(
        self,
        canvas: HTMLCanvasElement,
        cmd: DrawCmd,
    ) -> None:
        """Draw a tile at the specified position."""
        gid = cmd.tile_gid
        position = cmd.position
        scale = cmd.scale
        for tileset in self.tilesets:
            if tileset.firstgid <= gid < tileset.firstgid + tileset.tilecount:
                tile_index = gid - tileset.firstgid
                x = (tile_index % tileset.columns) * tileset.tilewidth
                y = (tile_index // tileset.columns) * tileset.tileheight

                ctx = canvas.getContext("2d", alpha=True)
                ctx.drawImage(
                    tileset.image,
                    x,
                    y,
                    tileset.tilewidth,
                    tileset.tileheight,
                    position.x,
                    position.y,
                    tileset.tilewidth * scale,
                    tileset.tileheight * scale,
                )
                break


@dataclass
class Tile:
    """Represents a single tile in the world."""

    sprite_id: str = ""  # backward compatibility
    gid: int = 0  # Global ID of the tile
    z: int = 0
    passable: bool = False


@dataclass
class ObjectTile:
    """Represents an object tile in the world."""

    id: str
    x: int
    y: int
    width: int
    height: int
    passable: bool = False


class TileMap:
    """Grid of tiles that makes up the world terrain."""

    def __init__(self, width: int, height: int, tile_size: int) -> None:
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tiles: dict[tuple[int, int], list[Tile]] = defaultdict(list)
        self.collision_boxes: list[ObjectTile] = []

    def get(self, x: int, y: int) -> list[Tile] | None:
        """Get the tile at given coordinates."""
        return self.tiles.get((x, y), None)

    def set(self, x: int, y: int, tile: Tile) -> None:
        """Set the tile at given coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[(x, y)].append(tile)

    def is_passable(self, x: int, y: int) -> bool:
        """Check if a tile can be walked on."""
        tile = self.get(x, y)
        return tile is not None and all(t.passable for t in tile)

    def add_collision_box(self, obj: ObjectTile) -> None:
        """Add a collision box to the tile map."""
        self.collision_boxes.append(obj)

    @classmethod
    def load_from_tiled(cls, tiled: dict) -> "TileMap":
        """Load tile map data from a Tiled JSON object."""
        tile_map = cls(
            width=tiled["width"],
            height=tiled["height"],
            tile_size=tiled["tilewidth"],
        )

        for layer in tiled["layers"]:
            if layer["type"] == "tilelayer":
                for idx, gid in enumerate(layer["data"]):
                    if gid > 0:
                        x = idx % tile_map.width
                        y = idx // tile_map.width
                        tile = Tile(gid=gid, z=0, passable=True)
                        tile_map.set(x, y, tile)
            elif layer["type"] == "objectgroup":
                for obj in layer["objects"]:
                    tile_map.add_collision_box(
                        ObjectTile(
                            id=obj["id"],
                            x=obj["x"],
                            y=obj["y"],
                            width=obj["width"],
                            height=obj["height"],
                            passable=obj.get("properties", {}).get("passable", False),
                        ),
                    )
        return tile_map
