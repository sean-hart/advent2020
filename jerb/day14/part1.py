#!/usr/local/bin/python3
from collections import namedtuple
import re
import sys


Mask = namedtuple('Mask', ('ignore', 'override'))
Assign = namedtuple('Instruction', ('address', 'argument'))


def parse_instructions(raw_instructions):
    for instruction in raw_instructions:
        if instruction.startswith('mask'):
            yield parse_mask(instruction)
        else:
            yield Assign(*map(int, re.search(r'(\d+)\D+(\d+)', instruction).groups()))


def parse_mask(raw_mask):
    raw_mask = raw_mask[raw_mask.rindex(' ') + 1:]
    ignore = int(''.join([str(int(b == 'X')) for b in raw_mask]), 2)
    override = int(raw_mask.replace('X', '0'), 2)
    return Mask(ignore, override)


def compute(instructions):
    registers = dict()
    mask = Mask(2 ** 36 - 1, 0) # no-op mask
    for instruction in instructions:
        if type(instruction) == Mask:
            mask = instruction
        elif type(instruction) == Assign:
            registers[instruction.address] = instruction.argument & mask.ignore | mask.override
        else:
            raise ValueError('Invalid instruction type')

    return sum(registers.values())


def main(filehandle):
    raw_instructions = filehandle.read().rstrip().split('\n')
    return compute(parse_instructions(raw_instructions))


if __name__ == '__main__':
    print(main(sys.stdin))

