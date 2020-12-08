#!/usr/bin/env python3


class Policy:

    def __init__(self, character, value_min, value_max):
        self.character = character
        self.value_min = value_min
        self.value_max = value_max

    def check(self, password):
        instances = 0
        for ch in password:
            if ch == self.character:
                instances += 1
        return self.value_min <= instances <= self.value_max


class PolicyNew:

    def __init__(self, character, value_min, value_max):
        self.character = character
        self.position_1 = value_min - 1
        self.position_2 = value_max - 1

    def check(self, password):
        if len(password) > self.position_1 and password[self.position_1] == self.character:
            contains1 = True
        else:
            contains1 = False
        if len(password) > self.position_2 and password[self.position_2] == self.character:
            contains2 = True
        else:
            contains2 = False
        return contains1 ^ contains2


def read_input():
    data = list()
    with open("input") as hand:
        for line in hand:
            data.append(line.strip())
    return data


def parse_line(line, version=1):
    policy_str, password = line.split(": ")
    interval, expectation = policy_str.split(" ")
    interval_min, interval_max = interval.split("-")
    if version == 1:
        policy = Policy(expectation, int(interval_min), int(interval_max))
    else:
        policy = PolicyNew(expectation, int(interval_min), int(interval_max))
    return policy, password


def solve(data):
    valid = 0
    for policy, password, in data:
        if policy.check(password):
            valid += 1
    return valid


if __name__ == "__main__":
    data = read_input()
    data1 = map(lambda line: parse_line(line, version=1), data)
    solution1 = solve(data1)
    print("Solution 1: %d" % solution1)
    data2 = map(lambda line: parse_line(line, version=2), data)
    solution2 = solve(data2)
    print("Solution 2: %d" % solution2)