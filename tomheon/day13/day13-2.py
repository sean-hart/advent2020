import sys


def matches_offset(bus, offset, target):
    if offset == 0:
        return target % bus == 0
    else:
        return target % bus == bus - (offset % bus)


def solve_with_step(bus_with_offset, start, step):
    b, o = bus_with_offset
    while True:
        if matches_offset(b, o, start):
            return start
        start += step


def main():
    buses_with_offsets = [(int(b), o) for (o, b) in list(enumerate(sys.stdin.read().split(','))) if b != 'x']

    buses_with_offsets.sort()

    start = 1
    step = 1
    
    for i in range(len(buses_with_offsets)):
        start = solve_with_step(buses_with_offsets[i], start, step)
        # don't need to worry about lcm because these are all primes
        step *= buses_with_offsets[i][0]

    print(start)


if __name__ == '__main__':
    main()
