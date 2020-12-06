#!/usr/local/bin/python3
from collections import namedtuple


INPUT_FILE = 'input.txt'
ADVANCE_TOKENS = {'B', 'R'}
BoardingPass = namedtuple('BoardingPass', ('row', 'column', 'seat'))


def derive_position(encoding):
    if not encoding:
        return 0
    elif encoding[0] not in ADVANCE_TOKENS:
        return derive_position(encoding[1:])
    else:
        return 2**(len(encoding) - 1) + derive_position(encoding[1:])


def parse_boarding_passes(input_file):
    with open(input_file) as f:
        for boarding_pass in f:
            row = derive_position(boarding_pass[:7])
            column = derive_position(boarding_pass[7:10])
            yield BoardingPass(row, column, row * 8 + column)


if __name__ == '__main__':
    occupied = reduce(lambda accum, e: accum | 2 ** e.seat,
                      parse_boarding_passes(INPUT_FILE), key=lambda e: e.seat)
    print(occupied)

