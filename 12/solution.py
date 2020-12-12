#!/usr/bin/env python3


MOVE_NORTH = "N"
MOVE_SOUTH = "S"
MOVE_EAST = "E"
MOVE_WEST = "W"
ROTATE_LEFT = "L"
ROTATE_RIGHT = "R"
MOVE_FORWARD = "F"


class Boat:

    def __init__(self, waypoint, move_refers_to_waypoint=False):
        self.x = 0  # > 0 means east
        self.y = 0  # > 0 means north
        self.waypoint = waypoint  # Boat waypoint/direction
        # True if move actions move the waypoint, False if they move the boat
        self.move_refers_to_waypoint = move_refers_to_waypoint

    def move(self, move_type, move_value):
        if move_type == ROTATE_LEFT:
            self.rotate_left(move_value)
        elif move_type == ROTATE_RIGHT:
            self.rotate_right(move_value)
        elif move_type == MOVE_FORWARD:
            dx, dy = self.waypoint
            self.x += dx * move_value
            self.y += dy * move_value
        else:
            self._move_action(move_type, move_value)

    def _move_action(self, move_type, move_value):
        if self.move_refers_to_waypoint:
            x, y = self.waypoint
        else:
            x, y = self.x, self.y

        if move_type == MOVE_NORTH:
            y += move_value
        elif move_type == MOVE_SOUTH:
            y -= move_value
        elif move_type == MOVE_EAST:
            x += move_value
        elif move_type == MOVE_WEST:
            x -= move_value
        else:
            raise RuntimeError("Invalid move %s" % move_type)

        if self.move_refers_to_waypoint:
            self.waypoint = (x, y)
        else:
            self.x, self.y = x, y

    def rotate_left(self, degrees):
        times = (degrees % 360) // 90
        dx, dy = self.waypoint
        for _ in range(times):
            dx, dy = -dy, dx
        self.waypoint = (dx, dy)

    def rotate_right(self, degrees):
        self.rotate_left(360 - degrees)


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


def read_moves():
    for line in read_input():
        move_type = line[0]
        move_value = int(line[1:])
        yield move_type, move_value


def solve1(moves):
    boat = Boat((1, 0))
    for move in moves:
        boat.move(*move)
    return abs(boat.x) + abs(boat.y)


def solve2(moves):
    boat = Boat((10, 1), move_refers_to_waypoint=True)
    for move in moves:
        boat.move(*move)
    return abs(boat.x) + abs(boat.y)


if __name__ == "__main__":
    moves = list(read_moves())
    solution1 = solve1(moves)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(moves)
    print("Solution 2: %d" % solution2)
