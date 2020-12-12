#!/usr/local/bin/python3
from collections import namedtuple

Instruction = namedtuple('Instruction', ('address', 'command', 'argument'))

commands = {
    'nop': lambda pos, acc, arg: (pos + 1, acc),
    'jmp': lambda pos, acc, arg: (pos + arg, acc),
    'acc': lambda pos, acc, arg: (pos + 1, acc + arg)
}


def load_instructions(input_file):
    with open(input_file) as f:
        for i, line in enumerate(f.readlines()):
            cmd, arg = line.rstrip().split()
            yield Instruction(i, cmd, int(arg))


def process_instructions(instructions, pos=0, accum=0):
    seen = set()
    while pos < len(instructions) and instructions[pos] not in seen:
        seen.add(instructions[pos])
        pos, accum = commands[instructions[pos].command](pos, accum, instructions[pos].argument)

    return pos, accum


def part1(input_file):
    _, accum = process_instructions(tuple(load_instructions(input_file)))
    return accum


def flip_corrupt_instruction(instructions, pos):
    if instructions[pos].command == 'jmp':
        instructions[pos] = Instruction(
            instructions[pos].address, 'nop', instructions[pos].argument)
    elif instructions[pos].command == 'nop':
        instructions[pos] = Instruction(
            instructions[pos].address, 'jmp', instructions[pos].argument)


def part2(input_file):
    instructions = list(load_instructions(input_file))
    pos = 0
    exit_accum = None

    while pos < len(instructions):
        exit_pos, exit_accum = process_instructions(instructions)
        if exit_pos >= len(instructions):
            break

        flip_corrupt_instruction(instructions, pos)
        exit_pos, exit_accum = process_instructions(instructions)
        if exit_pos >= len(instructions):
            break

        flip_corrupt_instruction(instructions, pos)
        pos += 1

    return exit_accum


if __name__ == '__main__':
    input_file = 'input.txt'
    print(f"part 1: {part1(input_file)}")
    print(f"part 2: {part2(input_file)}")


