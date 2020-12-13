#!/usr/bin/env python3


from functools import reduce


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


def parse_bus_info():
    bus_data = list(read_input())
    depart, bus_ids_raw = bus_data
    bus_ids = list()
    for bus_id in bus_ids_raw.split(","):
        if bus_id == "x":
            continue
        bus_ids.append(int(bus_id))
    return int(depart), bus_ids


def parse_bus_pattern():
    bus_data = list(read_input())
    _, bus_ids_raw = bus_data
    bus_pattern = list()
    for bus_id in bus_ids_raw.split(","):
        if bus_id == "x":
            bus_pattern.append(None)
        else:
            bus_pattern.append(int(bus_id))
    return bus_pattern


def solve1():
    depart, bus_ids = parse_bus_info()
    min_wait_time = None
    min_bus_id = None
    for bus_id in bus_ids:
        wait_time = bus_id - (depart % bus_id)
        if min_wait_time is None or wait_time < min_wait_time:
            min_wait_time = wait_time
            min_bus_id = bus_id
    return min_bus_id * min_wait_time


def solve2():
    pattern = parse_bus_pattern()
    """
        Need to solve
        x = a_1 (b_1)
        x = a_2 (b_2)
        ...
    """
    linear_sistem = list()
    for n, bus_id in enumerate(pattern):
        if bus_id is not None:
            linear_sistem.append((-1 * n, bus_id))
    """
        For a two equation system
        x = a_1 (b_1)
        x = a_2 (b_2)
        
        Given m_1, m_2 such that m_1 * b_1 + m_2 * b_2 = 1
        the solution is
        x = a_1 * m_2 * b_2 + a_2 * m_1 * b_1
    """
    x, b = reduce(solve_system, linear_sistem)
    return x


def solve_system(s1, s2):
    a_1, b_1 = s1
    a_2, b_2 = s2
    m_1, m_2 = resolve_bezout_identity(b_1, b_2)
    x = a_1 * m_2 * b_2 + a_2 * m_1 * b_1
    b = b_1 * b_2
    return (x % b), b


def resolve_bezout_identity(b_1, b_2):
    """
        m_1 * b_1 + m_2 * b_2 = 1
        m_1 * b_1 == 1 (b_2)
    """
    for m in range(b_2):
        if (m * b_1) % b_2 == 1:
            m_1 = m
            break
    m_2 = (1 - (m_1 * b_1)) // b_2
    return m_1, m_2


if __name__ == "__main__":
    solution1 = solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solve2()
    print("Solution 2: %d" % solution2)
