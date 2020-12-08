#!/usr/bin/env python3


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


def load_interpreter():
    source_code = list(read_input())
    interpreter = Interpreter()
    interpreter.compile(source_code)
    return interpreter


class Interpreter:

    def __init__(self):
        self.acc = 0
        self.idx = 0
        self.code = None

    def compile(self, source):
        self.code = list()
        for line in source:
            operation, argument_raw = line.split(" ", maxsplit=1)
            argument = int(argument_raw)
            self.code.append((operation, argument))

    def reset(self):
        self.idx = 0
        self.acc = 0

    def _executeInstruction(self, operation, argument):
        if operation == "nop":
            self.idx += 1
        elif operation == "acc":
            self.acc += argument
            self.idx += 1
        elif operation == "jmp":
            self.idx += argument
        else:
            raise RuntimeError("Invalid operation %s" % operation)

    def runDebug(self):
        operation, argument = self.code[self.idx]
        self._executeInstruction(operation, argument)
        return self.idx

    def terminated(self):
        return self.idx >= len(self.code)


def run_interpreter(interpreter):
    interpreter.reset()
    executed_operations = set()
    while not interpreter.terminated() and interpreter.idx not in executed_operations:
        executed_operations.add(interpreter.idx)
        interpreter.runDebug()
    return interpreter.acc, interpreter.terminated()

def solve1(interpreter):
    acc, _ = run_interpreter(interpreter)
    return acc


def solve2(interpreter):
    value = None
    for idx, original_instruction in enumerate(interpreter.code):
        operation, argument = original_instruction
        if operation == "acc":
            continue
        # Switch
        if operation == "nop":
            new_operation = "jmp"
        else:
            new_operation = "nop"
        interpreter.code[idx] = (new_operation, argument)
        # Attempt to run
        acc, terminated = run_interpreter(interpreter)
        if terminated:
            value = acc
            break
        # Switch back
        interpreter.code[idx] = original_instruction
    return value


if __name__ == "__main__":
    interpreter = load_interpreter()
    solution1 = solve1(interpreter)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(interpreter)
    print("Solution 2: %d" % solution2)


