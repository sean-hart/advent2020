#!/usr/local/bin/python3
from math import ceil


if __name__ == '__main__':
    with open('input.txt') as f:
        depart = int(f.readline())
        buses = [int(b) for b in f.readline().rstrip().split(',') if b != 'x']

    bus = min(zip(buses, [ceil(depart/b) * b - depart for b in buses]), key=lambda e: e[1])
    print(bus[0] * bus[1])
