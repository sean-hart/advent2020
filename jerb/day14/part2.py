#!/usr/local/bin/python3
from collections import namedtuple
from functools import reduce
import operator
import re
import sys


Mask = namedtuple('Mask', ('enable', 'static', 'floating'))
Assign = namedtuple('Instruction', ('address', 'argument'))

ADDRESS_SIZE = 36


def parse_instructions(raw_instructions):
    for instruction in raw_instructions:
        if instruction.startswith('mask'):
            yield parse_mask(instruction)
        else:
            yield Assign(*map(int, re.search(r'(\d+)\D+(\d+)', instruction).groups()))


def parse_mask(raw_mask):
    raw_mask = raw_mask[raw_mask.rindex(' ') + 1:]
    static = (2 ** ADDRESS_SIZE - 1) & int(raw_mask.replace('0', '1').replace('X', '0'), 2)
    enable = int(raw_mask.replace('X', '0'), 2)
    floating = [2**i for (i, b) in enumerate(reversed(raw_mask)) if b == 'X']
    return Mask(enable, static, floating)


def derive_registers(mask, address):
    """returns a list of addresses that result from applying the given mask"""
    base = address & mask.static | mask.enable
    floating = tuple(enumerate(mask.floating))
    for permutation in range(2**len(floating)):
        factors = [f[1] for f in floating if (2**f[0]) & permutation]
        yield reduce(operator.ior, factors, base)


def compute(instructions):
    registers = dict()
    mask = Mask(0, 2 ** ADDRESS_SIZE - 1, []) # no-op mask
    for instruction in instructions:
        if type(instruction) == Mask:
            mask = instruction
        elif type(instruction) == Assign:
            for register in derive_registers(mask, instruction.address):
                registers[register] = instruction.argument
        else:
            raise ValueError('Invalid instruction type')

    return sum(registers.values())


def main(filehandle):
    raw_instructions = filehandle.read().rstrip().split('\n')
    return compute(parse_instructions(raw_instructions))


if __name__ == '__main__':
    print(main(sys.stdin))

