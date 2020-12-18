#!/usr/bin/env python3


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


def evaluate(expression, cursor=0, advanced=False):
    elements = list()
    while cursor < len(expression):
        value = expression[cursor]
        if value == " ":
            cursor += 1
        elif value == "(":
            value, cursor = evaluate(expression, cursor+1, advanced=advanced)
            elements.append(value)
        elif value == ")":
            cursor += 1
            break
        elif value == "+":
            elements.append("+")
            cursor += 1
        elif value == "*":
            elements.append("*")
            cursor += 1
        else:
            value, cursor = parse_int(expression, cursor)
            elements.append(value)
    if advanced:
        current_value = compute_advanced(elements)
    else:
        current_value = compute(elements)
    return current_value, cursor


def parse_int(expression, cursor):
    start = cursor
    while cursor < len(expression) and 48 <= ord(expression[cursor]) <= 57:
        cursor += 1
    return int(expression[start:cursor]), cursor


def compute(elements):
    current_value = elements[0]
    idx = 1
    while idx < len(elements):
        if elements[idx] == "+":
            current_value = current_value + elements[idx + 1]
            idx += 2
        elif elements[idx] == "*":
            current_value = current_value * elements[idx + 1]
            idx += 2
        else:
            raise RuntimeError("Invalid operation %s", elements[idx])
    return current_value


def compute_advanced(elements):
    # Apply only the sums
    element_to_multiply = list()
    idx = 1
    current_value = None
    while idx < len(elements):
        if elements[idx] == "+":
            if current_value is None:
                current_value = elements[idx-1]
            current_value = current_value + elements[idx+1]
            idx += 2
        elif elements[idx] == "*":
            if current_value is not None:
                element_to_multiply.append(current_value)
                current_value = None
            else:
                element_to_multiply.append(elements[idx-1])
            idx += 2
        else:
            raise RuntimeError("Invalid operation %s", elements[idx])
    if current_value is not None:
        element_to_multiply.append(current_value)
    else:
        element_to_multiply.append(elements[-1])
    result = 1
    for element in element_to_multiply:
        result *= element
    return result


def solve1(expressions):
    total_sum = 0
    for expression in expressions:
        value, _ = evaluate(expression)
        total_sum += value
    return total_sum


def solve2(expressions):
    total_sum = 0
    for expression in expressions:
        value, _ = evaluate(expression, advanced=True)
        total_sum += value
    return total_sum


if __name__ == "__main__":
    expressions = list(read_input())
    solution1 = solve1(expressions)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(expressions)
    print("Solution 2: %d" % solution2)
