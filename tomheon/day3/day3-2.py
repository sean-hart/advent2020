import sys
from functools import reduce

X = 0
Y = 1
TREE = '#'


def count_trees_hit_on_slope(x_slope, y_slope, grid):
    start_pos = (0, 0)
    pos_hit = [((start_pos[X] + (x_slope * i)) % len(grid[i]),
                start_pos[Y] + (y_slope * i)) for i in range(len(grid))
                if (y_slope * i) < len(grid)]
    squares = [grid[pos[Y]][pos[X]] for pos in pos_hit]
    return squares.count(TREE)


def main():
    grid = [line.strip() for line in sys.stdin if line.strip()]
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    trees_hit = [count_trees_hit_on_slope(s[X], s[Y], grid) for s in slopes]
    print(reduce(lambda x, y: x * y, trees_hit))

if __name__ == '__main__':
    main()
