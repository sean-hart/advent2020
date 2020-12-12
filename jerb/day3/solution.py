#!/usr/local/bin/python3
from math import prod

MAP_FILE = 'input.txt'
FOREST = '#'


def load_forest(input_filename):
    forest = []
    with open(input_filename) as f:
        for line in f:
            forest.append(list(line.rstrip()))
    return forest


def count_trees(forest_map, direction):
    """
    given a forest map, count the number of trees along the path made by traversing
    in `direction` increments. the map's columns repeat unbounded.
    """
    rows, cols = len(forest_map), len(forest_map[0])
    x, y = direction # the problem states that the starting square is empty
    trees = 0
    while x < rows and y < cols:
        if forest_map[x][y] == FOREST:
            trees += 1
        x, y = x + direction[0], (y + direction[1]) % cols

    return trees


if __name__ == '__main__':
    forest = load_forest(MAP_FILE)

    part1_directions = (1, 3),
    part2_directions = (1, 1), (1, 3), (1, 5), (1, 7), (2, 1)

    print(prod([count_trees(forest, d) for d in part1_directions]))

