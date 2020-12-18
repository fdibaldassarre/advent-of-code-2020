#!/usr/bin/env python3


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


def to_tuple(size, *elements):
    result = [0] * size
    for n, el in enumerate(elements):
        result[n] = el
    return tuple(result)


def get_neighbours_iter(n, idx=0):
    if idx == n - 1:
        yield -1,
        yield 0,
        yield 1,
    else:
        for neighbour in get_neighbours_iter(n, idx+1):
            for dx in range(-1, 2):
                yield neighbour + (dx,)


class Space:

    def __init__(self, dimensions=3):
        self.dimensions = dimensions
        self.active_cubes = set()
        self.zero_neighbours = self._get_zero_neighbours()

    def _get_zero_neighbours(self):
        zero = (0,) * self.dimensions
        zero_neighbours = list()
        for delta in get_neighbours_iter(self.dimensions):
            if delta == zero:
                continue
            else:
                zero_neighbours.append(delta)
        return zero_neighbours

    def add_cube(self, cube):
        point = to_tuple(self.dimensions, *cube)
        self.active_cubes.add(point)

    def get_neighbours(self, point):
        for delta in self.zero_neighbours:
            yield tuple(n + delta[idx] for idx, n in enumerate(point))

    def get_visible_space(self):
        visible_space = set()
        for cube in self.active_cubes:
            visible_space.add(cube)
            for reachable in self.get_neighbours(cube):
                visible_space.add(reachable)
        return visible_space

    def update_active_cubes(self, active_cubes):
        self.active_cubes = active_cubes


def read_cubes():
    cubes = set()
    for y, line in enumerate(read_input()):
        for x, value in enumerate(line):
            if value == "#":
                cubes.add((x, y))
    return cubes


def solve(cubes, dimension=3):
    space = Space(dimension)
    for cube in cubes:
        space.add_cube(cube)
    for _ in range(6):
        # Get visible space
        visible_space = space.get_visible_space()
        # Update
        new_active_cubes = set()
        for cube in visible_space:
            n_active = 0
            for neighbour in space.get_neighbours(cube):
                if neighbour in space.active_cubes:
                    n_active += 1
            if cube in space.active_cubes:
                # Check if remains active
                if n_active == 2 or n_active == 3:
                    new_active_cubes.add(cube)
            else:
                # Check if becomes active
                if n_active == 3:
                    new_active_cubes.add(cube)
        space.update_active_cubes(new_active_cubes)
    return len(space.active_cubes)


def solve1(cubes):
    return solve(cubes, dimension=3)


def solve2(cubes):
    return solve(cubes, dimension=4)


if __name__ == "__main__":
    cubes = list(read_cubes())
    solution1 = solve1(cubes)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(cubes)
    print("Solution 2: %d" % solution2)
