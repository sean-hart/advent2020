#!/usr/local/bin/python3
import chinese_remainder
from itertools import count


def cascade(t, buses):
    for bus, offset in buses:
        if (t + offset) % bus != 0:
            return False

    return True


def solve_brute(buses):
    """unfortunately this worked in testing but was too slow for the large-sized input"""
    start = buses[0][0]
    for t in count(start, start):
        if cascade(t, buses[1:]):
            return t


def solve_fancy(buses):
    """i needed help to remember how to solve linear congruences..."""
    a = [b[0] for b in buses]
    n = [0] + [b[0] - b[1] for b in buses[1:]]
    return chinese_remainder.chinese_remainder(a, n)


if __name__ == '__main__':
    with open('input.txt') as f:
        depart = int(f.readline())
        buses = [(int(b), o) for (o, b) in enumerate(f.readline().rstrip().split(',')) if b != 'x']

    print(solve_fancy(buses))

