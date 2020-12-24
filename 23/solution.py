#!/usr/bin/env python3


class Cup:

    def __init__(self, value):
        self.value = value
        self.next = None


def read_input():
    data = input("Insert your input: ")
    return data.strip()


def read_cups(data):
    values = list(map(int, data))
    first = None
    prev = None
    for value in values:
        current = Cup(value)
        if first is None:
            first = current
        if prev is not None:
            prev.next = current
        prev = current
    prev.next = first
    return first, max(values)


def build_label_to_cup(first_cup):
    label_to_cup = dict()
    c = first_cup
    while True:
        label_to_cup[c.value] = c
        c = c.next
        if c == first_cup:
            break
    return label_to_cup


def add_cups(first_cup, max_value):
    label_to_cup = build_label_to_cup(first_cup)
    prev = first_cup
    while prev.next.value != first_cup.value:
        prev = prev.next
    for label in range(max_value + 1, 1000001):
        node = Cup(label)
        label_to_cup[label] = node
        prev.next = node
        prev = node
    prev.next = first_cup
    return first_cup, label_to_cup, 1000000


def iterate_once(cups, label_to_cup, max_value):
    cut = cups.next
    last_cut = cut
    for _ in range(2):
        last_cut = last_cut.next
    # Re-attach
    cups.next = last_cut.next
    last_cut.next = None
    # Find, if possible, the value with label=value-1
    current_value = cups.value
    values_cut = set()
    c = cut
    for _ in range(3):
        values_cut.add(c.value)
        c = c.next
    possible_values = set(filter(lambda el: el > 0, range(current_value - 4, current_value)))
    possible_values.difference_update(values_cut)
    if len(possible_values) == 0:
        # Find the maximum value in the list
        max_values = set(range(max_value-4, max_value+1))
        target_value = max(max_values.difference(values_cut))
    else:
        target_value = max(possible_values)
    # Find the target value
    start_section = label_to_cup[target_value]
    end_section = start_section.next
    # Attach
    start_section.next = cut
    last_cut.next = end_section
    return cups.next


def solve1(first_cup, label_to_cup, max_value):
    current_cup = first_cup
    for _ in range(100):
        current_cup = iterate_once(current_cup, label_to_cup, max_value)
    # Print the final order
    while current_cup.value != 1:
        current_cup = current_cup.next
    values = list()
    current_cup = current_cup.next
    while current_cup.value != 1:
        values.append(current_cup.value)
        current_cup = current_cup.next
    return "".join(map(str, values))


def solve2(first_cup, label_to_cup, max_value):
    current_cup = first_cup
    for _ in range(10000000):
        current_cup = iterate_once(current_cup, label_to_cup, max_value)
    # Print the final order
    while current_cup.value != 1:
        current_cup = current_cup.next
    # Print the final order
    while current_cup.value != 1:
        current_cup = current_cup.next
    l1 = current_cup.next.value
    l2 = current_cup.next.next.value
    return l1 * l2


if __name__ == "__main__":
    cups_str = read_input()
    first_cup, max_value = read_cups(cups_str)
    label_to_cup = build_label_to_cup(first_cup)
    solution1 = solve1(first_cup, label_to_cup, max_value)
    print("Solution 1: %s" % solution1)
    first_cup, max_value = read_cups(cups_str)
    first_cup, label_to_cup, max_value = add_cups(first_cup, max_value)
    solution2 = solve2(first_cup, label_to_cup, max_value)
    print("Solution 2: %d" % solution2)
