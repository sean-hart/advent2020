def count_trees(input_string, slope):
    right = 0
    down = 0
    trees = 0
    lines = input_string.splitlines()
    while down < len(lines):
        while len(lines[down]) <= right:
            lines[down] = lines[down] + lines[down]
        if lines[down][right] == '#':
            trees += 1
        right += slope['right']
        down += slope['down']
    return trees
