#!/usr/bin/env python3

DIRECTION_EAST = "e"
DIRECTION_SOUTHEAST = "se"
DIRECTION_SOUTHWEST = "sw"
DIRECTION_WEST = "w"
DIRECTION_NORTHWEST = "nw"
DIRECTION_NORTHEAST = "ne"


def get_neighbours(x, y):
    neighbours = dict()
    neighbours[DIRECTION_EAST] = (x - 2, y)
    neighbours[DIRECTION_WEST] = (x + 2, y)
    neighbours[DIRECTION_SOUTHEAST] = (x - 1, y - 1)
    neighbours[DIRECTION_SOUTHWEST] = (x + 1, y - 1)
    neighbours[DIRECTION_NORTHEAST] = (x - 1, y + 1)
    neighbours[DIRECTION_NORTHWEST] = (x + 1, y + 1)
    return neighbours


class HexagonalGrid:

    def __init__(self):
        self.black_tiles = set()

    def flip(self, tile):
        if tile in self.black_tiles:
            self.black_tiles.remove(tile)
        else:
            self.black_tiles.add(tile)

    def count_black(self):
        return len(self.black_tiles)

    def flipall(self, tiles):
        for tile in tiles:
            self.flip(tile)


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


def parse_moves(line):
    moves = list()
    val = None
    for ch in line:
        if val is not None:
            moves.append(val + ch)
            val = None
            continue
        if ch == "n" or ch == "s":
            val = ch
        else:
            moves.append(ch)
    return moves


def read_move_list():
    move_list = list()
    for line in read_input():
        move_list.append(parse_moves(line))
    return move_list


def solve1(move_list):
    grid = HexagonalGrid()
    for moves in move_list:
        tile = (0, 0)
        for move in moves:
            tile = get_neighbours(*tile)[move]
        grid.flip(tile)
    return grid, grid.count_black()


def solve2(grid):
    for _ in range(100):
        # Find the visible space
        visibile_space = set()
        for tile in grid.black_tiles:
            visibile_space.add(tile)
            for visible in get_neighbours(*tile).values():
                visibile_space.add(visible)
        # Flip
        flip_set = set()
        for tile in visibile_space:
            n_blacks = 0
            for neighbour in get_neighbours(*tile).values():
                if neighbour in grid.black_tiles:
                    n_blacks += 1
            if tile in grid.black_tiles:
                if n_blacks == 0 or n_blacks > 2:
                    flip_set.add(tile)
            else:
                if n_blacks == 2:
                    flip_set.add(tile)
        # Update
        grid.flipall(flip_set)
    return grid.count_black()


if __name__ == "__main__":
    move_list = read_move_list()
    grid, solution1 = solve1(move_list)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(grid)
    print("Solution 2: %d" % solution2)
