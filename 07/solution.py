#!/usr/bin/env python3


class Rule:

    def __init__(self, source, contain=None):
        self.source = source
        self.contain = contain if contain is not None else dict()


def rule_from_string(line):
    line = line[:-1]  # Remove the final .
    source, contain_raw = line.split("bags contain", maxsplit=1)
    source = source.strip()
    contain_raw = contain_raw.strip()
    if contain_raw == "no other bags":
        return Rule(source)
    contain_raw = contain_raw.split(",")
    contain = dict()
    for contain_line in contain_raw:
        # contain_line == ' 1 bright white bag'
        contain_line = contain_line.strip()
        if contain_line.endswith("bag"):
            contain_line = contain_line[:-4]
        elif contain_line.endswith("bags"):
            contain_line = contain_line[:-5]
        n, color = contain_line.split(" ", maxsplit=1)
        contain[color] = int(n)
    return Rule(source, contain)


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()

def read_rules():
    data = read_input()
    rules = dict()
    for line in data:
        rule = rule_from_string(line)
        rules[rule.source] = rule
    return rules


def build_reverse_index(rules):
    """
        color -> bags containing the color
    :param rules:
    :return:
    """
    reverse_index = dict()
    for color in rules.keys():
        reverse_index[color] = set()
    for rule in rules.values():
        color = rule.source
        for contains in rule.contain:
            reverse_index[contains].add(color)
    return reverse_index


def solve1(rules):
    reverse_index = build_reverse_index(rules)
    target = "shiny gold"
    current_level = set()
    current_level.add(target)
    bags_with_shiny = set()
    while len(current_level) > 0:
        new_level = set()
        for color in current_level:
            if color in bags_with_shiny:
                continue
            bags_with_shiny.add(color)
            for contained in reverse_index[color]:
                new_level.add(contained)
        current_level = new_level
    return len(bags_with_shiny) - 1

def solve2(rules):
    total = 0
    bags = rules["shiny gold"].contain
    while len(bags) > 0:
        # Expand one
        bag = list(bags.keys())[0]
        multiplier = bags[bag]
        total += multiplier
        contained = rules[bag].contain
        for new_bag, quantity in contained.items():
            if new_bag not in bags:
                bags[new_bag] = 0
            bags[new_bag] += multiplier * quantity
        del bags[bag]
    return total


if __name__ == "__main__":
    groups = read_rules()
    solution1 = solve1(groups)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(groups)
    print("Solution 2: %d" % solution2)


