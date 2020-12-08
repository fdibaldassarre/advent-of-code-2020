#!/usr/bin/env python3

class Map:

    def __init__(self, data):
        self.data = data
        self._width = len(data[0])
        self.bottom = len(data)

    def checkTree(self, x, y):
        x = x % self._width
        return data[y][x] == "#"


def read_input():
    data = list()
    with open("input") as hand:
        for line in hand:
            data.append(line.strip())
    return data


def solve1(map, dx=3, dy=1):
    trees = 0
    n_steps = map.bottom // dy
    for step in range(n_steps):
        y = dy * step
        x = dx * step
        if map.checkTree(x, y):
            trees += 1
    return trees

def solve2(map):
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2)
    ]
    solution = 1
    for slope in slopes:
        dx, dy = slope
        trees = solve1(map, dx=dx, dy=dy)
        solution *= trees
    return solution


if __name__ == "__main__":
    data = read_input()
    map = Map(data)
    solution1 = solve1(map)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(map)
    print("Solution 2: %d" % solution2)


