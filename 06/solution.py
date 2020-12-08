#!/usr/bin/env python3


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()

def read_groups():
    data = read_input()
    groups = list()
    current_group = list()
    for line in data:
        if line == "":
            groups.append(current_group)
            current_group = list()
        else:
            current_group.append(line)
    groups.append(current_group)
    return groups


def solve1(groups):
    total = 0
    for group in groups:
        collective = set()
        for anwers in group:
            for answer in anwers:
                collective.add(answer)
        total += len(collective)
    return total

def solve2(groups):
    total = 0
    for group in groups:
        common = None
        for anwers in group:
            current = set()
            for answer in anwers:
                current.add(answer)
            if common is None:
                common = current
            else:
                common = common.intersection(current)
        total += len(common)
    return total


if __name__ == "__main__":
    groups = read_groups()
    solution1 = solve1(groups)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(groups)
    print("Solution 2: %d" % solution2)


