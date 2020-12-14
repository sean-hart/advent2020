import sys
from itertools import groupby


def find_within_three(a, c, adapters):
    return [(n, c) for n in adapters if 0 < (n - a) <= 3]


def count_finished(working, highest):
    return sum([c for (a, c) in working if a == highest])


def find_next_working(adapters, working, highest):
    next_working = []

    for (a, c) in working:
        next_working.extend(find_within_three(a, c, adapters))
        
    next_working.sort()
    next_working = [(a, sum([c for (n, c) in g])) for a, g in groupby(next_working, key=lambda x: x[0])]
    
    return next_working, count_finished(working, highest) 


def main():
    adapters = [0] + [int(line.strip()) for line in sys.stdin if line.strip()]

    adapters.sort()
    highest = adapters[-1]

    score = 0
    
    working = [(adapters[0], 1)]
    
    while working:
        next_working, finished = find_next_working(adapters, working, highest)
        score += finished
        working = next_working

    print(score)
        
    

    
if __name__ == '__main__':
    main()
