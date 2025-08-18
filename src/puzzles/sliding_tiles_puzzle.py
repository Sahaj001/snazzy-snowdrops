import numpy as np
from js import Image, HTMLCanvasElement, window

class SlidingTilesPuzzle:
    def __init__(self, image_path: str, grid_size: int, tile_size: int):
        self.image_path = image_path
        self.grid_size = grid_size
        self.tile_size = tile_size

        # Load image
        self.image = Image.new()
        self.image.src = image_path

        # Create a solved puzzle (last tile is the "empty" space)
        self.tiles = np.arange(grid_size * grid_size).reshape((grid_size, grid_size))
        self.empty_pos = (grid_size - 1, grid_size - 1)  # start bottom-right

    def shuffle(self):
        """Randomly shuffle the tiles but keep solvable state (simple shuffle for now)."""
        flat_tiles = self.tiles.flatten()
        np.random.shuffle(flat_tiles)
        self.tiles = flat_tiles.reshape((self.grid_size, self.grid_size))

        # Find empty tile again
        empty_index = np.where(self.tiles == self.grid_size**2 - 1)
        self.empty_pos = (empty_index[0][0], empty_index[1][0])

    def swap(self, pos1, pos2):
        """Swap two tiles given (row, col) positions"""
        r1, c1 = pos1
        r2, c2 = pos2
        self.tiles[r1, c1], self.tiles[r2, c2] = self.tiles[r2, c2], self.tiles[r1, c1]

    def handle_input(self, direction: str):
        """Move empty tile if possible: 'up', 'down', 'left', 'right'"""
        row, col = self.empty_pos
        target_pos = None
        print('my direction is', direction)

        if direction == "up" and row < self.grid_size - 1:
            target_pos = (row + 1, col)
        elif direction == "down" and row > 0:
            target_pos = (row - 1, col)
        elif direction == "left" and col < self.grid_size - 1:
            target_pos = (row, col + 1)
        elif direction == "right" and col > 0:
            target_pos = (row, col - 1)

        if target_pos:
            self.swap(self.empty_pos, target_pos)
            self.empty_pos = target_pos

    def is_solved(self):
        """Check if puzzle is solved"""
        return np.array_equal(self.tiles, np.arange(self.grid_size**2).reshape(self.grid_size, self.grid_size))

    def draw2(self, canvas: "HTMLCanvasElement"):
        """Draw all tiles centered with a nice border"""
        ctx = canvas.getContext("2d")

        # Determine puzzle display size = half the viewport
        puzzle_size = min(window.innerWidth, window.innerHeight) // 2
        scaled_tile_size = puzzle_size // self.grid_size

        # Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height)

        # Compute offsets for centering
        offset_x = (canvas.width - puzzle_size) // 2
        offset_y = (canvas.height - puzzle_size) // 2

        # Draw background panel with rounded corners
        border_radius = 20
        ctx.fillStyle = "#333"  # dark background
        ctx.strokeStyle = "#fff"  # white border
        ctx.lineWidth = 4

        ctx.beginPath()
        ctx.moveTo(offset_x + border_radius, offset_y)
        ctx.lineTo(offset_x + puzzle_size - border_radius, offset_y)
        ctx.quadraticCurveTo(offset_x + puzzle_size, offset_y,
                            offset_x + puzzle_size, offset_y + border_radius)
        ctx.lineTo(offset_x + puzzle_size, offset_y + puzzle_size - border_radius)
        ctx.quadraticCurveTo(offset_x + puzzle_size, offset_y + puzzle_size,
                            offset_x + puzzle_size - border_radius, offset_y + puzzle_size)
        ctx.lineTo(offset_x + border_radius, offset_y + puzzle_size)
        ctx.quadraticCurveTo(offset_x, offset_y + puzzle_size,
                            offset_x, offset_y + puzzle_size - border_radius)
        ctx.lineTo(offset_x, offset_y + border_radius)
        ctx.quadraticCurveTo(offset_x, offset_y, offset_x + border_radius, offset_y)
        ctx.closePath()
        ctx.fill()
        ctx.stroke()

        # Draw tiles
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                tile_id = self.tiles[row, col]

                # Skip drawing the empty tile
                if tile_id == self.grid_size**2 - 1:
                    continue

                src_x = (tile_id % self.grid_size) * self.tile_size
                src_y = (tile_id // self.grid_size) * self.tile_size
                dest_x = offset_x + col * scaled_tile_size
                dest_y = offset_y + row * scaled_tile_size

                ctx.drawImage(
                    self.image,
                    src_x, src_y, self.tile_size, self.tile_size,  # source size from original image
                    dest_x, dest_y, scaled_tile_size, scaled_tile_size  # destination scaled size
                )
        
    def draw(self, canvas):
        ctx = canvas.getContext("2d")

        """Draw all tiles in a centered, beautiful grid"""
        # Calculate board size (half the smallest window dimension)
        board_size = min(window.innerWidth, window.innerHeight) // 2
        tile_draw_size = board_size // self.grid_size

        # Centering offsets
        offset_x = (window.innerWidth - board_size) // 2
        offset_y = (window.innerHeight - board_size) // 2

        # Style background board
        ctx.fillStyle = "#333"
        ctx.strokeStyle = "#fff"
        ctx.lineWidth = 4
        ctx.beginPath()
        ctx.roundRect(offset_x, offset_y, board_size, board_size, 20)  # Rounded corners
        ctx.fill()
        ctx.stroke()

        # Draw each tile
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                tile_id = self.tiles[row, col]
                if tile_id == self.grid_size**2 - 1:  # skip empty tile
                    continue

                # Source position in the original image
                src_x = (tile_id % self.grid_size) * self.tile_size
                src_y = (tile_id // self.grid_size) * self.tile_size

                # Destination position in canvas
                dest_x = offset_x + col * tile_draw_size
                dest_y = offset_y + row * tile_draw_size

                ctx.drawImage(
                    self.image,
                    src_x, src_y, self.tile_size, self.tile_size,  # src rect
                    dest_x, dest_y, tile_draw_size, tile_draw_size  # dest rect
                )

                # Tile border
                ctx.strokeStyle = "#000"
                ctx.lineWidth = 2
                ctx.strokeRect(dest_x, dest_y, tile_draw_size, tile_draw_size)