#!/usr/bin/env python3


def read_staring_numbers():
    numbers_raw = input("Insert your input numbers: ")
    return list(map(lambda n: int(n.strip()), numbers_raw.split(",")))


def solve1(starting_numbers, target=2020):
    last_spoken = dict()
    prev_number = None
    for round in range(target):
        if round < len(starting_numbers):
            spoken = starting_numbers[round]
        else:
            if prev_number not in last_spoken:
                spoken = 0
            else:
                spoken = round - 1 - last_spoken[prev_number]
        if prev_number is not None:
            last_spoken[prev_number] = round - 1
        prev_number = spoken
    return prev_number


def solve2(starting_numbers):
    return solve1(starting_numbers, target=30000000)


if __name__ == "__main__":
    numbers = read_staring_numbers()
    solution1 = solve1(numbers)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(numbers)
    print("Solution 2: %d" % solution2)
