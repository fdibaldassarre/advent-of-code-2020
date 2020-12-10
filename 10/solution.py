#!/usr/bin/env python3


def read_input():
    with open("input") as hand:
        for line in hand:
            yield int(line.strip())


def solve1(jolts):
    differences = [0, 0, 0, 0]
    previous = 0
    for jolt in jolts:
        delta = jolt - previous
        differences[delta] += 1
        previous = jolt
    differences[3] += 1
    return differences[1] * differences[3]


def solve2(jolts):
    combinations = [0 for _ in jolts]
    combinations[len(jolts) - 1] = 1
    for n in range(len(jolts) - 1, 0, -1):
        idx = n - 1
        current = jolts[idx]
        current_combinations = 0
        for i in range(idx + 1, len(jolts)):
            if jolts[i] - current > 3:
                break
            current_combinations += combinations[i]
        combinations[idx] = current_combinations
    final_combinations = 0
    for n, jolt in enumerate(jolts):
        if jolt > 3:
            break
        final_combinations += combinations[n]
    return final_combinations


if __name__ == "__main__":
    jolts = list(read_input())
    jolts.sort()
    solution1 = solve1(jolts)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(jolts)
    print("Solution 2: %d" % solution2)
