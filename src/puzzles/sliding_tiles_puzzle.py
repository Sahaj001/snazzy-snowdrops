import numpy as np
from js import HTMLCanvasElement, Image, window


class SlidingTilesPuzzle:
    def __init__(self, image_path: str, grid_size: int, tile_size: int) -> None:
        self.image_path = image_path
        self.grid_size = grid_size
        self.tile_size = tile_size

        # Load image
        self.image = Image.new()
        self.image.src = image_path

        # Create a solved puzzle (last tile is the "empty" space)
        self.tiles = np.arange(grid_size * grid_size).reshape((grid_size, grid_size))
        self.empty_pos = (grid_size - 1, grid_size - 1)  # start bottom-right
        self.solved = False

    def shuffle(self):
        flat = np.arange(self.grid_size * self.grid_size)
        np.random.shuffle(flat)

        # Ensure solvability
        while not self._is_solvable(flat):
            np.random.shuffle(flat)

        self.tiles = flat.reshape((self.grid_size, self.grid_size))
        self.empty_pos = tuple(np.argwhere(self.tiles == self.grid_size**2 - 1)[0])

    def _is_solvable(self, flat) -> bool:
        """Check if a given tile arrangement is solvable"""
        inversions = 0
        size = self.grid_size
        empty_tile = size * size - 1

        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] != empty_tile and flat[j] != empty_tile and flat[i] > flat[j]:
                    inversions += 1

        if size % 2 == 1:
            # Odd grid: solvable if inversions even
            return inversions % 2 == 0
        else:
            # Even grid: row of empty from bottom matters
            empty_row = (np.where(flat == empty_tile)[0][0] // size)
            empty_row_from_bottom = size - empty_row
            return (inversions + empty_row_from_bottom) % 2 == 0


    def swap(self, pos1, pos2) -> None:
        """Swap two tiles given (row, col) positions."""
        r1, c1 = pos1
        r2, c2 = pos2
        self.tiles[r1, c1], self.tiles[r2, c2] = self.tiles[r2, c2], self.tiles[r1, c1]

    def handle_input(self, direction: str) -> None:
        """Move empty tile if possible: 'up', 'down', 'left', 'right'."""
        row, col = self.empty_pos
        target_pos = None
        print("my direction is", direction)

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

        # After each move, check if solved
        self._check_solved()

    def _swap(self, pos1, pos2):
        self.tiles[pos1], self.tiles[pos2] = self.tiles[pos2], self.tiles[pos1]

    def _check_solved(self):
        expected = np.arange(self.grid_size * self.grid_size).reshape((self.grid_size, self.grid_size))
        if np.array_equal(self.tiles, expected):
            if not self.solved:
                self.solved = True
                self.on_solved()

    def on_solved(self):
        """Called when puzzle is solved"""
        print("🎉 Puzzle solved! Game Finished.")

    def is_solved(self):
        """Check if puzzle is solved."""
        return np.array_equal(self.tiles, np.arange(self.grid_size**2).reshape(self.grid_size, self.grid_size))

    def draw2(self, canvas: "HTMLCanvasElement") -> None:
        """Draw all tiles centered with a nice border."""
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
        ctx.quadraticCurveTo(offset_x + puzzle_size, offset_y, offset_x + puzzle_size, offset_y + border_radius)
        ctx.lineTo(offset_x + puzzle_size, offset_y + puzzle_size - border_radius)
        ctx.quadraticCurveTo(
            offset_x + puzzle_size,
            offset_y + puzzle_size,
            offset_x + puzzle_size - border_radius,
            offset_y + puzzle_size,
        )
        ctx.lineTo(offset_x + border_radius, offset_y + puzzle_size)
        ctx.quadraticCurveTo(offset_x, offset_y + puzzle_size, offset_x, offset_y + puzzle_size - border_radius)
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
                    src_x,
                    src_y,
                    self.tile_size,
                    self.tile_size,  # source size from original image
                    dest_x,
                    dest_y,
                    scaled_tile_size,
                    scaled_tile_size,  # destination scaled size
                )

    def draw(self, canvas) -> None:
        ctx = canvas.getContext("2d")
        canvas_width = ctx.canvas.width
        canvas_height = ctx.canvas.height
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
                    src_x,
                    src_y,
                    self.tile_size,
                    self.tile_size,  # src rect
                    dest_x,
                    dest_y,
                    tile_draw_size,
                    tile_draw_size,  # dest rect
                )

                # Tile border
                ctx.strokeStyle = "#000"
                ctx.lineWidth = 2
                ctx.strokeRect(dest_x, dest_y, tile_draw_size, tile_draw_size)
        # If solved, overlay full screen
        if self.solved:
            self._draw_completion_screen(ctx, canvas_width, canvas_height)

    def _draw_completion_screen(self, ctx, w, h):

        """Draw a full screen overlay when the puzzle is solved"""
        ctx.save()

        # Semi-transparent dark overlay
        ctx.fillStyle = "rgba(0, 0, 0, 0.75)"
        ctx.fillRect(0, 0, w, h)

        # Celebration message
        ctx.fillStyle = "gold"
        ctx.font = "bold 36px Arial"
        ctx.textAlign = "center"
        ctx.fillText("🎉 Puzzle Completed! 🎉", w // 2, h // 2 - 40)

        ctx.font = "24px Arial"
        ctx.fillStyle = "white"
        ctx.fillText("You may now return to your world.", w // 2, h // 2 + 10)
        ctx.fillText("Press any key to continue...", w // 2, h // 2 + 50)

        ctx.restore()
