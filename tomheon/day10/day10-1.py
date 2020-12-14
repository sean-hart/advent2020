import sys
from itertools import tee


def main():
    adapters = [0] + [int(line.strip()) for line in sys.stdin if line.strip()]
    adapters.sort()
    adapters.append(adapters[-1] + 3)
    a, b = tee(adapters)
    next(b)
    diffs = [a2 - a1 for (a1, a2) in zip(a, b)]
    print(diffs.count(1))
    print(diffs.count(3))
    print(diffs.count(1) * diffs.count(3))
    
if __name__ == '__main__':
    main()
