#!/usr/bin/env python3

def parse_int(value):
    try:
        result = int(value)
    except Exception:
        result = -1
    return result

REQUIRED_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

VALID_EYE_COLORS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

class Passport:

    def __init__(self):
        self.values = dict()
        self.n_required = 0
        self.valid_strict = True

    def add(self, pkey, pvalue):
        self.values[pkey] = pvalue
        if pkey in REQUIRED_FIELDS:
            self.n_required += 1
            if self.valid_strict and not self._valid(pkey, pvalue):
                self.valid_strict = False

    def isValid(self):
        return self.n_required == 7

    def isValidStrict(self):
        return self.isValid() and self.valid_strict

    def _valid(self, pkey, pvalue):
        if pkey == "byr":
            return 1920 <= parse_int(pvalue) <= 2002
        elif pkey == "iyr":
            return 2010 <= parse_int(pvalue) <= 2020
        elif pkey == "eyr":
            return 2020 <= parse_int(pvalue) <= 2030
        elif pkey == "hgt":
            return self._validHeight(pvalue)
        elif pkey == "hcl":
            return self._validColor(pvalue)
        elif pkey == "ecl":
            return pvalue in VALID_EYE_COLORS
        elif pkey == "pid":
            return len(pvalue) == 9 and parse_int(pvalue) != -1

    def _validHeight(self, pvalue):
        height = parse_int(pvalue[:-2])
        if pvalue.endswith("cm"):
            return 150 <= height <= 193
        elif pvalue.endswith("in"):
            return 59 <= height <= 76
        else:
            return False

    def _validColor(self, value):
        if not value.startswith("#") or len(value) != 7:
            return False
        valid = True
        for i in range(1, 7):
            v = ord(value[i])
            if 48 <= v <= 57 or 97 <= v <= 122:
                pass
            else:
                valid = False
                break
        return valid


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()

def read_passports():
    passports = list()
    passport = None
    for line in read_input():
        if line == "":
            if passport is not None:
                passports.append(passport)
                passport = None
        else:
            if passport is None:
                passport = Passport()
            values = line.split(" ")
            for value in values:
                pkey, pvalue = value.split(":", maxsplit=2)
                passport.add(pkey, pvalue)
    if passport is not None:
        passports.append(passport)
    return passports


def solve1(passports):
    n_valid = 0
    for passport in passports:
        if passport.isValid():
            n_valid += 1
    return n_valid

def solve2(passports):
    n_valid = 0
    for passport in passports:
        if passport.isValidStrict():
            n_valid += 1
    return n_valid


if __name__ == "__main__":
    passports = read_passports()
    solution1 = solve1(passports)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(passports)
    print("Solution 2: %d" % solution2)


