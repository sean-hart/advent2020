#!/usr/local/bin/python3

INPUT_FILE = 'input.txt'


def parse_group(group):
    return [set(person) for person in group.strip().split('\n')]


if __name__ == '__main__':
    with open(INPUT_FILE) as f:
        groups = [parse_group(group) for group in f.read().split('\n\n')]

    print(sum(len(set.intersection(*group)) for group in groups))

