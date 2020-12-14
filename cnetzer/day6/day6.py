if __name__ == '__main__':
    import fileinput

    data = [line.strip() for line in fileinput.input()]

    groups = [set()]
    for line in data:
        if not line:
            groups.append(set())
            continue
        groups[-1] |= set(line)

    count = sum(len(group) for group in groups)
    print('Part 1:', count)


    groups = [[]]
    for line in data:
        if not line:
            groups.append([])
            continue
        groups[-1].append(set(line))

    groups = [group for group in groups if group]
    count = sum(len(set.intersection(*g)) for g in groups)
    print('Part 2:', count)
