#!/usr/bin/env python3


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


class IRule:

    def verify(self, message, rules):
        raise NotImplementedError


class Rule(IRule):

    def __init__(self, value=None, or_conditions=None):
        self.value = value
        self.or_conditions = or_conditions

    def verify(self, message, rules):
        cursor = self.verify_iter(message, rules, cursor=0)
        return cursor == len(message)

    def verify_iter(self, message, rules, cursor):
        if cursor >= len(message):
            return -1
        if self.value is not None:
            if message[cursor] == self.value:
                return cursor + 1
            else:
                return -1
        else:
            for and_conditions in self.or_conditions:
                verified = True
                rule_cursor = cursor
                for and_condition in and_conditions:
                    and_rule = rules[and_condition]
                    rule_cursor = and_rule.verify_iter(message, rules, cursor=rule_cursor)
                    if rule_cursor == -1:
                        verified = False
                        break
                if verified:
                    return rule_cursor
            return -1




"""
Verify the pattern
0: 8 11
8: 42 | 42 8
11: 42 31 | 42 11 31
"""
class RuleZero(IRule):

    def verify_star(self, rule, message, rules, cursor):
        """
        Verify the pattern rule*
        """
        cursors = list()
        while -1 < cursor < len(message):
            cursor = rule.verify_iter(message, rules, cursor=cursor)
            if cursor > -1:
                cursors.append(cursor)
        return cursors

    def verify(self, message, rules):
        possible_head_cursors = self.verify_star(rules[42], message, rules, cursor=0)
        for head_matches, start_cursor in enumerate(possible_head_cursors):
            for n, section_cursor in enumerate(possible_head_cursors[head_matches+1:]):
                section_matched = n + 1  # Times 42 matched that should be mirrored by 31 matches
                conditions = [[31] * section_matched]
                tmp_rule = Rule(or_conditions=conditions)
                end_cursor = tmp_rule.verify_iter(message, rules, cursor=section_cursor)
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