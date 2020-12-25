#!/usr/bin/env python3


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


def read_public_keys():
    for line in read_input():
        yield int(line)


def perform_loop(value, subject_number=7):
    value *= subject_number
    value %= 20201227
    return value


def solve1(card_public_key, door_public_key):
    # Find the loop sizes
    loop_size = 0
    value = 1
    card_loop_size, door_loop_size = None, None
    while card_loop_size is None and door_loop_size is None:
        value = perform_loop(value, subject_number=7)
        loop_size += 1
        if value == card_public_key:
            card_loop_size = loop_size
        if value == door_public_key:
            door_loop_size = loop_size
    # Find the encryption key
    if door_loop_size is not None:
        loop_size = door_loop_size
        subject_number = card_public_key
    else:
        loop_size = card_loop_size
        subject_number = door_public_key
    encryption_key = 1
    for _ in range(loop_size):
        encryption_key = perform_loop(encryption_key, subject_number=subject_number)
    return encryption_key


if __name__ == "__main__":
    public_keys = list(read_public_keys())
    solution1 = solve1(*public_keys)
    print("Solution 1: %d" % solution1)
