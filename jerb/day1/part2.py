#!/usr/bin/python3
# aoc 2020 day 1 part 2
import itertools

def solution(integers):
    """
    Finds the integers that sum to 2020 and returns their product.
    Raises `ValueError` if there is no solution.
    """
    inverse = {}
    for (a, b) in itertools.combinations(integers, 2):
        inverse[2020 - a - b] = a * b

    for n in integers:
        if n in inverse:
            return n * inverse[n]

    raise ValueError('no solution found')


if __name__ == '__main__':
    with open('input.txt') as f:
        integers = map(int, f.read().split('\n'))
    print(solution(integers))

