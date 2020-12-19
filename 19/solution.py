#!/usr/bin/env python3


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


class Rule:

    def __init__(self, value=None, or_conditions=None):
        self.value = value
        self.or_conditions = or_conditions

    def verify(self, message, rules):
        verified, cursor = self.verify_iter(message, rules, cursor=0)
        return verified and cursor == len(message)

    def verify_iter(self, message, rules, cursor):
        if cursor >= len(message):
            return False, -1
        if self.value is not None:
            return message[cursor] == self.value, cursor+1
        else:
            for and_conditions in self.or_conditions:
                verified = True
                rule_cursor = cursor
                for and_condition in and_conditions:
                    and_rule = rules[and_condition]
                    rule_verified, rule_cursor = and_rule.verify_iter(message, rules, cursor=rule_cursor)
                    if not rule_verified:
                        verified = False
                        break
                if verified:
                    return True, rule_cursor
            return False, -1


"""
Verify the pattern
0: 8 11
8: 42 | 42 8
11: 42 31 | 42 11 31
"""
class RuleZero:

    def _verify(self, rule, message, rules, cursor):
        cursors = list()
        verified = True
        while verified and cursor < len(message):
            verified, cursor = rule.verify_iter(message, rules, cursor=cursor)
            if verified:
                cursors.append(cursor)
        return cursors

    def verify(self, message, rules):
        possible_head_cursors = self._verify(rules[42], message, rules, cursor=0)
        for start_cursor in possible_head_cursors:
            first_section_cursors = self._verify(rules[42], message, rules, cursor=start_cursor)
            for n, section_cursor in enumerate(first_section_cursors):
                n_matched = n + 1
                conditions = [[31] * n_matched]
                tmp_rule = Rule(or_conditions=conditions)
                end_cursors = tmp_rule.verify_iter(message, rules, cursor=section_cursor)
                for end_cursor in end_cursors:
                    if end_cursor == len(message):
                        return True
        return False


def parse_rule(line):
    if line.startswith("\""):
        value = line[1:-1]
        return Rule(value=value)
    else:
        or_conditions_raw = line.split(" | ")
        or_conditions = list()
        for condition_raw in or_conditions_raw:
            rules = list(map(int, condition_raw.split(" ")))
            or_conditions.append(rules)
        return Rule(or_conditions=or_conditions)


def parse():
    rules = dict()
    messages = list()
    read_messages = False
    for line in read_input():
        if line == "":
            read_messages = True
        if read_messages:
            messages.append(line)
        else:
            n, rule = line.split(": ", maxsplit=2)
            rules[int(n)] = parse_rule(rule)
    return rules, messages


def find_zero_rule_matches(rules, messages):
    n_matches = 0
    rule = rules[0]
    for message in messages:
        if rule.verify(message, rules):
            n_matches += 1
    return n_matches


def solve1(rules, messages):
    return find_zero_rule_matches(rules, messages)


def solve2(rules, messages):
    del rules[8]
    del rules[11]
    rules[0] = RuleZero()
    return find_zero_rule_matches(rules, messages)


if __name__ == "__main__":
    rules, messages = parse()
    solution1 = solve1(rules, messages)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(rules, messages)
    print("Solution 2: %d" % solution2)