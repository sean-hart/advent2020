#!/usr/bin/python3
# aoc 2020 day 1 part 1

def solution(integers):
    """
    Finds the two entries that sum to 2020 and returns their product.
    Raises `ValueError` if there is no solution.
    """
    inverse = set()

    for n in integers:
        if 2020 - n in inverse:
            return n * (2020 - n)
        inverse.add(n)

    raise ValueError('no solution found')


if __name__ == '__main__':
    with open('input.txt') as f:
        integers = map(int, f.read().split('\n'))
    print(solution(integers))

