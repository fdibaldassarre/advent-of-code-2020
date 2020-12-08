#!/usr/bin/env python3


class Boarding:

    def __init__(self, code):
        self.code = code

    def initialize(self):
        self.row = self._getValue(self.code[:7], "B")
        self.column = self._getValue(self.code[7:10], "R")
        self.id = self.row * 8 + self.column

    def _getValue(self, code, up_value):
        value = 0
        N = len(code)
        for i in range(N):
            if code[N-i-1] == up_value:
                value += 2**i
        return value


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


def read_boarding_passes():
    passes = list()
    for line in read_input():
        boarding = Boarding(line)
        boarding.initialize()
        passes.append(boarding)
    return passes


def solve1(boarding_passes):
    max_id = 0
    for boarding_pass in boarding_passes:
        max_id = max(boarding_pass.id, max_id)
    return max_id

def solve2(boarding_passes):
    boarding_passes = sorted(boarding_passes, key=lambda boarding_pass: boarding_pass.id)
    prev_pass = None
    my_board_pass_id = -1
    for boarding_pass in boarding_passes:
        if prev_pass is not None:
            if boarding_pass.id > prev_pass.id + 1:
                assert boarding_pass.id == prev_pass.id + 2
                my_board_pass_id = prev_pass.id + 1
                break
        prev_pass = boarding_pass
    return my_board_pass_id


if __name__ == "__main__":
    boarding_passes = read_boarding_passes()
    solution1 = solve1(boarding_passes)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(boarding_passes)
    print("Solution 2: %d" % solution2)


