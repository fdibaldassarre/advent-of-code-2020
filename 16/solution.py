#!/usr/bin/env python3


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


def parse_ranges(value):
    ranges_raw = value.split(" or ")
    ranges = list()
    for range_raw in ranges_raw:
        left, right = range_raw.split("-")
        ranges.append((int(left), int(right)))
    return ranges


def read_notes():
    ranges = dict()
    my_ticket = None
    nearby_tickets = list()
    read_ranges = True
    read_my_ticket = False
    for line in read_input():
        if line == "":
            continue
        if line.startswith("your ticket"):
            read_ranges = False
            read_my_ticket = True
            continue
        elif line.startswith("nearby ticket"):
            read_my_ticket = False
            continue

        if read_ranges:
            name, values = line.split(": ")
            name_ranges = parse_ranges(values)
            ranges[name] = name_ranges
        elif read_my_ticket:
            my_ticket = list(map(int, line.split(",")))
        else:
            ticket = list(map(int, line.split(",")))
            nearby_tickets.append(ticket)
    return ranges, my_ticket, nearby_tickets


def find_invalid_value(ticket, ranges):
    invalid_value = None
    for value in ticket:
        is_valid = False
        for name, name_ranges in ranges.items():
            is_valid_for_name = False
            for left, right in name_ranges:
                if left <= value <= right:
                    is_valid_for_name = True
                    break
            if is_valid_for_name:
                is_valid = True
                break
        if not is_valid:
            invalid_value = value
    return invalid_value


def solve1(ranges, my_ticket, nearby_tickets):
    invalid_values = list()
    for ticket in nearby_tickets:
        invalid_value = find_invalid_value(ticket, ranges)
        if invalid_value is not None:
            invalid_values.append(invalid_value)
    return sum(invalid_values)


def find_valid_fields(value, ranges):
    valid_fields = set()
    for name, name_ranges in ranges.items():
        for left, right in name_ranges:
            if left <= value <= right:
                valid_fields.add(name)
                break
    return valid_fields


def create_position_to_field_map(my_ticket, valid_tickets, ranges):
    """
    Create a map from a position to the fields valid for that position on all the tickets.
    """
    position_to_valid_fields = list()
    for position in range(len(my_ticket)):
        valid_fields = find_valid_fields(my_ticket[position], ranges)
        for ticket in valid_tickets:
            ticket_valid_fields = find_valid_fields(ticket[position], ranges)
            valid_fields = valid_fields.intersection(ticket_valid_fields)
        position_to_valid_fields.append((position, valid_fields))
    return position_to_valid_fields


def solve2(ranges, my_ticket, nearby_tickets):
    # Find the valid tickets
    valid_tickets = list(filter(lambda ticket: find_invalid_value(ticket, ranges) is None, nearby_tickets))

    # Find the valid fields for each position
    position_to_valid_fields = create_position_to_field_map(my_ticket, valid_tickets, ranges)
    # Sort by valid field size
    position_to_valid_fields.sort(key=lambda el: len(el[1]))

    # Create map position to field
    position_to_field_map = [None for _ in range(len(ranges))]
    assigned_fields = set()
    for position, valid_fields in position_to_valid_fields:
        target_field = None
        for valid_field in valid_fields:
            if valid_field not in assigned_fields:
                target_field = valid_field
        position_to_field_map[position] = target_field
        assigned_fields.add(target_field)

    # Find solution
    solution = 1
    for position, value in enumerate(my_ticket):
        field = position_to_field_map[position]
        if field.startswith("departure"):
            solution *= value
    return solution


if __name__ == "__main__":
    notes = read_notes()
    solution1 = solve1(*notes)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(*notes)
    print("Solution 2: %d" % solution2)
