def map_to_ring_array(m):
    return m.strip().splitlines()

def char_at(m, x, y):
    m = map_to_ring_array(m)
    W = len(m[0])
    H = len(m)

    x = x%W
    if y >= H:
        return None

    return m[y][x]

def tree_count(m, slope_x, slope_y):
    i = j = 0
    count = 0
    while True:
        char = char_at(m, i, j)
        if char is None:
            break
        if char == '#':
            count += 1
        i += slope_x
        j += slope_y

    return count


if __name__ == '__main__':
    import fileinput

    data = ''.join(line for line in fileinput.input())
    print('Part 1:', tree_count(data, 3, 1))

    slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]
    counts = []
    for slope in slopes:
        counts.append(tree_count(data, *slope))

    product = 1
    for x in counts:
        product *= x

    print('Part 2:', product)
