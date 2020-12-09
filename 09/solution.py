#!/usr/bin/env python3


def read_input():
    with open("input") as hand:
        for line in hand:
            yield int(line.strip())


class Preamble:

    def __init__(self, preamble):
        self._containSet = set(preamble)
        self._collector = preamble
        self._idx = 0
        self.size = len(preamble)

    def add(self, n):
        old = self._collector[self._idx]
        self._containSet.remove(old)
        self._collector[self._idx] = n
        self._containSet.add(n)
        self._idx = (self._idx + 1) % len(self._collector)

    def contains(self, n):
        return n in self._containSet

    def values(self):
        return self._collector


def verify(n, preamble):
    valid = False
    for v in preamble.values():
        if n != 2*v and preamble.contains(n - v):
            valid = True
    return valid


def solve1(cypher):
    preamble_size = 25
    preamble = Preamble(cypher[:preamble_size])
    invalid = None
    for i, n in enumerate(cypher):
        if i < preamble.size:
            pass
        else:
            if not verify(n, preamble):
                invalid = n
                break
            preamble.add(n)
    return invalid


def solve2(cypher, target):
    start_idx = 0
    end_idx = 1
    current_sum = cypher[start_idx]
    while end_idx < len(cypher) and current_sum != target:
        if current_sum + cypher[end_idx] <= target:
            current_sum += cypher[end_idx]
            end_idx += 1
        elif start_idx < end_idx:
            current_sum -= cypher[start_idx]
            start_idx += 1
        else:
            start_idx += 1
            end_idx = start_idx + 1
            current_sum = cypher[start_idx]
    target_range = cypher[start_idx:end_idx]
    return max(target_range) + min(target_range)


if __name__ == "__main__":
    cypher = list(read_input())
    solution1 = solve1(cypher)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(cypher, solution1)
    print("Solution 2: %d" % solution2)
