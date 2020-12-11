#!/usr/bin/env python3

POSITION_FLOOR = "."
POSITION_EMPTY = "L"
POSITION_OCCUPIED = "#"

DELTA = [(-1, -1), (0, -1), (1, -1),
         (-1, 0),           (1, 0),
         (-1, 1),  (0, 1),  (1, 1)]


class Layout:

    def __init__(self):
        self.layout = dict()
        self.max_x = 0
        self.max_y = 0
        self.occupied = 0
        self.seat_to_neighbours = dict()
        self.tolerance = 0

    def set(self, x, y, status):
        self.layout[(x, y)] = status
        self.max_x = max(self.max_x, x)
        self.max_y = max(self.max_y, y)

    def reset(self):
        self.occupied = 0
        for position in self.layout:
            if self.layout[position] != POSITION_FLOOR:
                self.layout[position] = POSITION_EMPTY

    def setup(self, max_distance=None, tolerance=5):
        self.tolerance = tolerance
        for position in self.layout:
            if self.layout[position] == POSITION_FLOOR:
                continue
            self.seat_to_neighbours[position] = self.get_visible_neighbours(position, max_distance)

    def get_visible_neighbours(self, position, max_distance=None):
        x, y = position
        neibours = list()
        for dx, dy in DELTA:
            n = 0
            neibour = None
            while max_distance is None or n < max_distance:
                n += 1
                nx = x + n * dx
                ny = y + n * dy
                if 0 <= nx <= self.max_x and 0 <= ny <= self.max_y:
                    if self.layout[(nx, ny)] != POSITION_FLOOR:
                        neibour = (nx, ny)
                        break
                else:
                    neibour = None
                    break
            if neibour is not None:
                neibours.append(neibour)
        return neibours

    def get_occupied_neighbour(self, position):
        occupied = 0
        for neibour in self.seat_to_neighbours[position]:
            if self.layout[neibour] == POSITION_OCCUPIED:
                occupied += 1
        return occupied

    def update(self):
        new_positions = dict()
        delta = 0  # Delta of occupied positions
        for position in self.layout:
            if self.layout[position] == POSITION_FLOOR:
                continue
            occupied_near = self.get_occupied_neighbour(position)
            if self.layout[position] == POSITION_EMPTY and occupied_near == 0:
                new_positions[position] = POSITION_OCCUPIED
                delta += 1
            elif self.layout[position] == POSITION_OCCUPIED and occupied_near >= self.tolerance:
                new_positions[position] = POSITION_EMPTY
                delta -= 1
        self.layout.update(new_positions)
        self.occupied += delta
        return len(new_positions) > 0


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


def parse_layout(layout_raw):
    layout = Layout()
    for y, line in enumerate(layout_raw):
        for x, ch in enumerate(line):
            layout.set(x, y, ch)
    return layout


def solve1(layout):
    layout.setup(max_distance=1, tolerance=4)
    changed = True
    while changed:
        changed = layout.update()
    return layout.occupied


def solve2(layout):
    layout.setup(max_distance=None, tolerance=5)
    changed = True
    while changed:
        changed = layout.update()
    return layout.occupied


if __name__ == "__main__":
    layout = parse_layout(read_input())
    solution1 = solve1(layout)
    print("Solution 1: %d" % solution1)
    layout.reset()
    solution2 = solve2(layout)
    print("Solution 2: %d" % solution2)
