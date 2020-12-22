import sys
from itertools import product


ACTIVE_CUBE = '#'
INACTIVE_CUBE = '.'


def read_dimension(instream):
    dim = dict()
    z = 0
    w = 0
    for y, line in enumerate(instream):
        line = line.strip()
        for x, cube in enumerate(line):
            dim[(x, y, z, w)] = cube

    return dim


def gen_neigbors(c):
    x, y, z, w = c
    deltas = [-1, 0, 1]
    return [(x + dx, y + dy, z + dz, w + dw)
            for (dx, dy, dz, dw)
            in product(deltas, deltas, deltas, deltas)
            if (dx, dy, dz, dw) != (0, 0, 0, 0)]


def is_active(cube):
    return cube == ACTIVE_CUBE


def determine_cube_state(dimension, c):
    neighbor_cubes = [dimension[n] for n in gen_neigbors(c) if n in dimension]
    if c in dimension and is_active(dimension[c]):
        return ACTIVE_CUBE if 2 <= neighbor_cubes.count(ACTIVE_CUBE) <= 3 else INACTIVE_CUBE
    else:
        return ACTIVE_CUBE if neighbor_cubes.count(ACTIVE_CUBE) == 3 else INACTIVE_CUBE
        

def expand_dimension(dimension):
    new_dimension = dict()

    for c in dimension:
        for n in gen_neigbors(c):
            if n not in new_dimension:
                new_dimension[n] = determine_cube_state(dimension, n)
    
    return new_dimension


def main():
    dimension = read_dimension(sys.stdin)
    for i in range(6):
        dimension = expand_dimension(dimension)
    print(list(dimension.values()).count(ACTIVE_CUBE))
        
    

if __name__ == '__main__':
    main()
