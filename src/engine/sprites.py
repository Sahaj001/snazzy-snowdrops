from js import Image, console


class TileMap:
    def __init__(self, canvas, tileset_src, tile_w, tile_h, map_data) -> None:
        self.canvas = canvas
        self.tile_width = tile_w
        self.tile_height = tile_h
        self.map_data = map_data
        self.tileset = Image.new()
        self.tileset.src = tileset_src
        self.loaded = False
        self.tileset.onload = self._on_load

    def _on_load(self, event) -> None:
        console.log("Tileset loaded")
        self.loaded = True

    def draw(self) -> None:
        if not self.loaded:
            return
        for row_idx, row in enumerate(self.map_data):
            for col_idx, tile_index in enumerate(row):
                # Calculate source tile position in tileset
                sx = (tile_index % (self.tileset.width // self.tile_width)) * self.tile_width
                sy = (tile_index // (self.tileset.width // self.tile_width)) * self.tile_height

                dx = col_idx * self.tile_width
                dy = row_idx * self.tile_height

                self.canvas.draw_sprite(
                    self.tileset, sx, sy, self.tile_width, self.tile_height, dx, dy, self.tile_width, self.tile_height,
                )
