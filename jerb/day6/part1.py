#!/usr/local/bin/python3

INPUT_FILE = 'input.txt'

def parse_group(group):
    return set(group.strip().replace('\n', ''))

if __name__ == '__main__':
    with open(INPUT_FILE) as f:
        groups = f.read().split('\n\n')

    print(sum(len(parse_group(group)) for group in groups))

