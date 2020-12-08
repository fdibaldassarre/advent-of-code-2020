#!/usr/bin/env python3


def read_input():
    data = list()
    with open("input") as hand:
        for line in hand:
            data.append(int(line.strip()))
    return data


def solve1(data, target=2020):
    # Find two entries that add up to 2020
    processed = set()
    solution = None
    for n in data:
        if n in processed:
            # Found
            solution = n * (target-n)
            break
        else:
            processed.add(target-n)
    return solution


def solve2(data):
    # Find three entries that map to 2020
    target = 2020
    for i in data:
        partial = solve1(data, target-i)
        if partial is not None:
            solution = partial * i
            break
    return solution


if __name__ == "__main__":
    data = read_input()
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)

    solution2 = solve2(data)
    print("Solution 2: %d" % solution2)
