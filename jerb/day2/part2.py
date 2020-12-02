#!/usr/bin/python3
from collections import namedtuple
import re

PasswordTest = namedtuple('PasswordTest', ('pos1', 'pos2', 'char', 'password'))


def parse_test(test):
    match = re.match(r'(\d+)-(\d+)\s+([a-zA-Z]): ([a-zA-Z]+)', test)
    if not match:
        raise ValueError('failed to parse test: ' + test)
    pos1, pos2, char, password = match.groups()
    return PasswordTest(int(pos1) - 1, int(pos2) - 1, char, password)


def is_valid_password(test):
    return test.password[test.pos1] == test.char) ^ (test.password[test.pos2] == test.char


if __name__ == '__main__':
    valid_count = 0
    with open('input.txt') as f:
        for line in f.readlines():
            test = parse_test(line.rstrip())
            if is_valid_password(test):
                valid_count += 1

    print(valid_count)
