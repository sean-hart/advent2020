import sys
from itertools import tee, islice, combinations, groupby, product
from functools import reduce
import operator



def ints_from(ss):
    for s in ss:
        yield int(s.strip())

def sum_range(ints, r, cache):
    if r in cache:
        return cache[r]
    elif r[0] >= r[1] - 1:
        return ints[r[0]]
    else:
        val = ints[r[0]] + sum_range(ints, (r[0] + 1, r[1]), cache)
        cache[r] = val
        return val

        
def sum_to_target(ints, r, target, cache):
    return sum_range(ints, r, cache) == target


def range_size(r):
    return r[1] - r[0]

        
def main():
    target = 27911108
    ints = list(ints_from(sys.stdin))
    ranges = [p for p in product(range(len(ints)), range(1, len(ints) + 1)) if p[0] <= p[1]]
    ranges.sort(key=range_size)
    cache = dict()
    candidates = [r for r in ranges if sum_to_target(ints, r, target, cache)]
    widest_range = candidates[-1]
    contig = ints[widest_range[0]:widest_range[1]]
    print(max(contig) + min(contig))

                 


if __name__ == '__main__':
    main()
