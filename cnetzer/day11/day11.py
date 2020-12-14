from array import array
from collections import Counter
from copy import deepcopy
from itertools import product
from pprint import pprint


def directions():
    for off_x, off_y in product([-1, 0, 1], repeat=2):
        if (off_x, off_y) == (0,0):
            continue
        yield (off_x, off_y)

def neighbors_part1(grid, out_of_bounds, x, y):
    for off_x, off_y in directions():
        pos_x, pos_y = (x + off_x, y + off_y)
        if (pos_x, pos_y) in out_of_bounds:
            continue
        yield grid[pos_y][pos_x]

def neighbors_part2(grid, out_of_bounds, x, y):
    for off_x, off_y in directions():
        #print(f'off_x {off_x}  off_y {off_y}')
        pos_x = x
        pos_y = y
        assert (off_x, off_y) != (0,0), (off_x, off_y)
        while True:
            pos_x = pos_x + off_x
            pos_y = pos_y + off_y
            #print(pos_x, pos_y)
            if (pos_x, pos_y) in out_of_bounds:
                break
            if grid[pos_y][pos_x] != '.':
                yield grid[pos_y][pos_x]
                break

def gridterable(grid, out_of_bounds, neighbors_func, empty_threshold):
    W = len(grid[0])
    H = len(grid)

    while True:
        new_grid = deepcopy(grid)
        for i in range(W):
            for j in range(H):
                counts = Counter(neighbors_func(grid, out_of_bounds, i, j))
                if grid[j][i] == 'L':
                    if not counts.get('#', 0):
                        new_grid[j][i] = '#'
                elif grid[j][i] == '#':
                    if counts.get('#', 0) >= empty_threshold:
                        new_grid[j][i] = 'L'
        yield new_grid

        if grid_to_str(new_grid, W) == grid_to_str(grid, W):
            break

        grid = new_grid

def grid_to_str(grid, width):
    s = ''.join(a.tounicode() for a in grid)
    return '\n'.join([s[i:i+width] for i in range(0, len(s), width)])


if __name__ == '__main__':
    import fileinput

    lines = [line.strip() for line in fileinput.input()]
    W = len(lines[0])

    grid = [array('u', line) for line in lines]

    # Make a set of "out of bounds" co-ordinates (this was added for part2, as
    # my part1 solution for handling out of bounds co-ordinates wouldn't have
    # worked for part 2).  I then adapted the part 1 and part 2 solutions to
    # use common functions for both solutions.
    out_of_bounds = set()
    out_of_bounds.update((x,-1) for x in range(-1, W))  # top border
    H = len(lines)
    for y in range(-1, H):
        out_of_bounds.add((-1,y))
        out_of_bounds.add((W,y))
    out_of_bounds.update((x,H) for x in range(-1, W+1))  # bottom border


    #print(grid)
    #print()
    for g in gridterable(grid, out_of_bounds, neighbors_part1, 4):
        # We only care about the last grid, but it's fun to print
        #print(g)
        #print()
        pass
    print('Part 1:', grid_to_str(g, W).count('#'))

    #print(grid)
    #print()
    for g in gridterable(grid, out_of_bounds, neighbors_part2, 5):
        # We only care about the last grid, but it's fun to print
        #print(g)
        #print()
        pass
    print('Part 2:', grid_to_str(g, W).count('#'))
