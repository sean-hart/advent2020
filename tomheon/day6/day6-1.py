import sys
from itertools import takewhile
from functools import reduce
import operator


def parse_groups(instream):
    while True:
        lines = [line.strip() for line in takewhile(lambda x: x.strip(), instream)]
        if not lines:
            break
        yield [set(iter(l)) for l in lines]


def main():
    print(sum([len(reduce(operator.or_, g)) for g in parse_groups(sys.stdin)]))


if __name__ == '__main__':
    main()
