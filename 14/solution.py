#!/usr/bin/env python3


INSTRUCTION_MASK = 0
INSTRUCTION_MEMORY = 1


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


def load_program():
    source = read_input()
    instructions = list()
    for line in source:
        if line.startswith("mask"):
            _, bitmask = line.split(" = ")
            instructions.append((INSTRUCTION_MASK, bitmask))
        else:
            address_str, value_str = line.split("] = ")
            address = int(address_str[4:])
            value = int(value_str)
            instructions.append((INSTRUCTION_MEMORY, (address, value)))
    return instructions


def apply_bitmask(value, bitmask_str):
    result = 0
    for i in range(36):
        mask = bitmask_str[35-i]
        v = (value // 2**i) & 1
        if mask == "X":
            result += v * 2**i
        elif mask == "1":
            result += 2**i
    return result


def apply_bitmask_v2(value, bitmask_str):
    values = list()
    values.append(0)
    for i in range(36):
        mask = bitmask_str[35-i]
        v = (value // 2**i) & 1
        if mask == "X":
            new_values = list()
            for result in values:
                new_value = result + 2 ** i
                new_values.append(new_value)
            values.extend(new_values)
        elif mask == "1":
            for idx in range(len(values)):
                values[idx] += 2 ** i
        else:
            for idx in range(len(values)):
                values[idx] += v * 2 ** i
    return values


def solve1(program):
    bitmask = None
    memory = dict()
    for instruction in program:
        type, argument = instruction
        if type == INSTRUCTION_MASK:
            bitmask = argument
        else:
            address, value = argument
            if address not in memory:
                memory[address] = 0
            memory[address] = apply_bitmask(value, bitmask)
    return sum(memory.values())


def solve2(program):
    bitmask = None
    memory = dict()
    for instruction in program:
        type, argument = instruction
        if type == INSTRUCTION_MASK:
            bitmask = argument
        else:
            address, value = argument
            addresses = apply_bitmask_v2(address, bitmask)
            for address in addresses:
                if address not in memory:
                    memory[address] = 0
                memory[address] = value
    return sum(memory.values())


if __name__ == "__main__":
    program = load_program()
    solution1 = solve1(program)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(program)
    print("Solution 2: %d" % solution2)
