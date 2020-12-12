#!/usr/local/bin/python3
from collections import defaultdict
from functools import lru_cache
from itertools import takewhile


def part1(numbers, rating=3):
    diffs = defaultdict(int)
    adapter = 0
    while adapter < len(numbers) - 1:
        for i in range(1, min(4, len(numbers) - adapter)):
            if numbers[adapter + i] <= numbers[adapter] + rating:
                diffs[numbers[adapter + i] - numbers[adapter]] += 1
                adapter = adapter + i
                break
    diffs[3] += 1
    return diffs


@lru_cache(maxsize=None)
def count_paths(numbers):
    if not numbers:
        return 1

    paths = 0
    for i, adapter in takewhile(lambda x: x[1] <= numbers[0] + 3, enumerate(numbers[1:])):
        paths += count_paths(numbers[i + 1:])

    return max(1, paths)


if __name__ == '__main__':
    with open('input.txt') as f:
        nums = tuple(sorted([int(jolt) for jolt in f.readlines()]))

    path_diffs = part1((0,) + nums)
    print(f'part1: {path_diffs[1] * path_diffs[3]}')
    print(f'part2: {2 * count_paths(nums)}')


