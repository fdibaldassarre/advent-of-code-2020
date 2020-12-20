#!/usr/bin/env python3


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


def print_tile(tile):
    for row in tile.rows:
        print(row)


DIRECTION_TOP = 0
DIRECTION_BOTTOM = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3


def get_opposite(direction):
    if direction == DIRECTION_TOP:
        return DIRECTION_BOTTOM
    elif direction == DIRECTION_BOTTOM:
        return DIRECTION_TOP
    elif direction == DIRECTION_LEFT:
        return DIRECTION_RIGHT
    elif direction == DIRECTION_RIGHT:
        return DIRECTION_LEFT
    else:
        raise RuntimeError("Invalid direction %s" % direction)


class Tile:

    def __init__(self, tile_id=None):
        self.tile_id = tile_id
        self.rows = list()
        self.borders = dict()
        self.size = None

    def get_id(self):
        return self.tile_id

    def append_row(self, line):
        if self.size is None:
            self.size = len(line)
        self.rows.append(line)
        if len(self.rows) == self.size:
            # Finalize
            self._compute_borders()

    def get_border(self, direction):
        return self.borders[direction]

    def rotate(self):
        matrix = dict()
        for y, line in enumerate(self.rows):
            for x, ch in enumerate(line):
                # Rotate
                rx, ry = y, self.size - 1 - x
                matrix[(rx, ry)] = ch
        self._re_build(matrix)

    def flip(self):
        matrix = dict()
        for y, line in enumerate(self.rows):
            for x, ch in enumerate(line):
                fx, fy = self.size - 1 - x, y
                matrix[(fx, fy)] = ch
        self._re_build(matrix)

    def _re_build(self, matrix):
        # Re-build
        n = len(self.rows)
        self.rows = list()
        for y in range(n):
            line = list()
            for x in range(n):
                line.append(matrix[(x, y)])
            self.rows.append("".join(line))
        # Re-compute
        self._compute_borders()

    def align(self, border, direction):
        aligned = False
        for flip in range(2):
            if aligned:
                break
            if flip == 1:
                self.flip()
            for _ in range(4):
                self.rotate()
                current_border = self.get_border(direction)
                if current_border == border:
                    aligned = True
                    break

    def get_actual_image(self):
        for row in self.rows[1:-1]:
            yield row[1:-1]

    def _compute_borders(self):
        self.borders[DIRECTION_TOP] = self.rows[0]
        self.borders[DIRECTION_BOTTOM] = self.rows[-1]
        left_border = list()
        right_border = list()
        for line in self.rows:
            left_border.append(line[0])
            right_border.append(line[-1])
        self.borders[DIRECTION_LEFT] = "".join(left_border)
        self.borders[DIRECTION_RIGHT] = "".join(right_border)

    def get_possible_borders(self):
        for border in self.borders.values():
            yield border
            yield border[::-1]


class Puzzle:

    def __init__(self, tiles):
        self.tiles = tiles
        self.border_to_tiles = self._build_border_map()

    def _build_border_map(self):
        border_to_tiles = dict()
        for tile_id, tile in tiles.items():
            for border in tile.get_possible_borders():
                if border not in border_to_tiles:
                    border_to_tiles[border] = set()
                border_to_tiles[border].add(tile_id)
        return border_to_tiles

    def go_to_direction(self, current_tile, direction):
        tiles_row = list()
        while True:
            tiles_row.append(current_tile)
            border = current_tile.get_border(direction)
            valid_tiles = self.border_to_tiles[border].copy()
            valid_tiles.remove(current_tile.get_id())
            if len(valid_tiles) > 1:
                raise RuntimeError("Too many tiles")
            elif len(valid_tiles) == 1:
                tile_id = list(valid_tiles)[0]
                current_tile = self.tiles[tile_id]
                # Align the tile
                current_tile.align(border, get_opposite(direction))
            else:
                # Done
                break
        return tiles_row

    def solve(self):
        _, current_tile = list(tiles.items())[0]
        # Go to the border
        left_border_tile = self.go_to_direction(current_tile, DIRECTION_LEFT)[-1]
        # Go along the image borders
        top_left_corner = self.go_to_direction(left_border_tile, DIRECTION_TOP)[-1]
        solution = dict()
        max_y = 0
        max_x = 0
        for y, left_tile in enumerate(self.go_to_direction(top_left_corner, DIRECTION_BOTTOM)):
            max_y = max(max_y, y)
            for x, tile in enumerate(self.go_to_direction(left_tile, DIRECTION_RIGHT)):
                max_x = max(max_x, x)
                solution[(x, y)] = tile
        return (max_x, max_y), solution


def read_tiles():
    tiles = dict()
    current_tile = None
    for line in read_input():
        if line == "":
            continue
        if line.startswith("Tile"):
            tile_number = int(line[5:-1])
            current_tile = Tile(tile_number)
            tiles[tile_number] = current_tile
        else:
            current_tile.append_row(line)
    return tiles


def check_monster_at(image, x, y):
    size = image.size
    if x+19 >= size:
        return False
    if y+3 >= size:
        return False
    rows = image.rows
    if rows[y][x + 18] == "#" and \
       rows[y+1][x] == "#" and rows[y+1][x+5] == "#" and rows[y+1][x+6] == "#" and \
       rows[y+1][x+11] == "#" and rows[y+1][x+12] == "#" and \
       rows[y+1][x+17] == "#" and rows[y+1][x+18] == "#" and rows[y+1][x+19] == "#" and \
       rows[y+2][x+1] == "#" and rows[y+2][x+4] == "#" and rows[y+2][x+7] == "#" and \
       rows[y+2][x+10] == "#" and rows[y+2][x+13] == "#" and rows[y+2][x+16] == "#":
        return True
    else:
        return False


def find_sea_monsters(image):
    sea_monsters = 0
    for y in range(image.size):
        for x in range(image.size):
            monster_here = check_monster_at(image, x, y)
            if monster_here:
                sea_monsters += 1
    return sea_monsters


def solve1(image_size, solution):
    max_x, max_y = image_size
    # Find the corners
    top_left_corner = solution[(0, 0)].get_id()
    top_right_corner = solution[(0, max_x)].get_id()
    bottom_left_corner = solution[(max_y, 0)].get_id()
    bottom_right_corner = solution[(max_y, max_x)].get_id()
    return top_left_corner * top_right_corner * \
           bottom_left_corner * bottom_right_corner


def solve2(image_size, solution):
    # Re-build the whole image
    max_x, max_y = image_size
    rows = list()
    for y in range(max_y + 1):
        # Add thw rows for the tiles on this line
        new_row_elements = list()
        # Add entire row
        for x in range(max_x + 1):
            tile = solution[(x, y)]
            for n, row in enumerate(tile.get_actual_image()):
                if n >= len(new_row_elements):
                    new_row_elements.append(list())
                new_row_elements[n].append(row)
        new_rows = list()
        for chunks in new_row_elements:
            new_rows.append("".join(chunks))
        rows.extend(new_rows)
    # Compose the image
    image = Tile(0)
    for row in rows:
        image.append_row(row)
    # Find the sea monsters
    sea_monsters = 0
    for flip in range(2):
        if sea_monsters > 0:
            break
        for _ in range(4):
            image.rotate()
            sea_monsters = find_sea_monsters(image)
            if sea_monsters > 0:
                break
    if sea_monsters == 0:
        raise RuntimeError("Error, no monsters found")
    # Count the '#' in the image
    n_hashes = 0
    for row in image.rows:
        for ch in row:
            if ch == "#":
                n_hashes += 1
    return n_hashes - sea_monsters * 15


if __name__ == "__main__":
    tiles = read_tiles()
    puzzle = Puzzle(tiles)
    image_size, solution = puzzle.solve()
    solution1 = solve1(image_size, solution)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(image_size, solution)
    print("Solution 2: %d" % solution2)
