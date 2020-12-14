import sys
from itertools import tee, islice, combinations
from functools import reduce
import operator


def slide_over_preambles(ps, preamble_length):
    a, b = tee(ps)
    yield islice(a, preamble_length)
    while True:
        next(b)
        a, b = tee(b)
        yield islice(a, preamble_length)
    
def ints_from(ss):
    for s in ss:
        yield int(s.strip())

        
def main():
    preamble_length = 25
    a, b = tee(ints_from(sys.stdin))
    targets = islice(b, preamble_length, None)
    for (preamble, target) in zip(slide_over_preambles(a, preamble_length), targets):
        if not any([reduce(operator.add, c) == target for c in combinations(preamble, 2)]):
            print(target)


if __name__ == '__main__':
    main()
