#!/usr/local/bin/python3
from collections import namedtuple

#INPUT_FILE = 'test.txt'
INPUT_FILE = 'input.txt'
ADVANCE_TOKENS = {'B', 'R'}
BoardingPass = namedtuple('BoardingPass', ('row', 'column', 'seat'))


def derive_position(encoding):
    power = len(encoding) - 1
    total = 0
    position = 0
    for c in encoding:
        if c in ADVANCE_TOKENS:
           total += 2 ** power
        power -= 1

    return total


def parse_boarding_passes(input_file):
    with open(input_file) as f:
        for boarding_pass in f:
            row = derive_position(boarding_pass[:7])
            column = derive_position(boarding_pass[7:10])
            yield BoardingPass(row, column, row * 8 + column)

if __name__ == '__main__':
    highest_seat = max(parse_boarding_passes(INPUT_FILE), key=lambda e: e.seat)
    print(highest_seat)

