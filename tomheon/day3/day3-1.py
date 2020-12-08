import sys

X = 0
Y = 1


def main():
    grid = [line.strip() for line in sys.stdin if line.strip()]
    start_pos = (0, 0)
    pos_hit = [((start_pos[X] + (3 * i)) % len(grid[i]), start_pos[Y] + i) for i in range(len(grid))]
    squares = [grid[pos[Y]][pos[X]] for pos in pos_hit]
    print(squares.count('#'))


if __name__ == '__main__':
    main()
