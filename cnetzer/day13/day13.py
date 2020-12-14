import math
import sys

assert sys.version_info >= (3,8), "Needed for math.prod() and inverse modular pow()"

# I tried to do as much of this as I could, but I definitely had to get hints
# from Wikipedia, Rosetta code, and others.
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
def chinese_remainders(remainders, modulos):
    # For a given equation:
    # x = r mod N
    #
    # The "remainders" are the r's, the "modulos" are the N's.

    total = 0
    N = math.prod(modulos)  # the Modulos are assumed to be co-prime, or this won't work
    for r,n in zip(remainders, modulos):
        p=N//n
        total += r * pow(p, -1, n)*p
    return total % N

def part1(line):
    buses_with_indices = [(i,int(b)) for i,b in enumerate(line.split(',')) if b != 'x']
    buses = [b for i,b in buses_with_indices]

    max_time = earliest_time + max(buses)
    all_times = set()
    bus_times = {}
    for bus_number in buses:
        bus_schedule = range(0, max_time+1, bus_number)
        bus_schedule = [x for x in bus_schedule if x >= earliest_time]
        all_times.update(bus_schedule)
        bus_times[bus_number] = bus_schedule

    next_bus_time = min(all_times)
    wait_time = next_bus_time - earliest_time
    for bus_number in bus_times:
        if next_bus_time in bus_times[bus_number]:
            bus_to_catch = bus_number
            break

    print('Part 1:', wait_time*bus_to_catch)

def part2(line):
    buses_with_indices = [(i,int(b)) for i,b in enumerate(line.split(',')) if b != 'x']

    remainders = []
    modulos = []
    for i,n in buses_with_indices:
        remainders.append(n - i)
        modulos.append(n)
    print('Part 2:', chinese_remainders(remainders, modulos))


if __name__ == '__main__':
    import fileinput

    f = fileinput.input()
    earliest_time = int(next(f))
    lines = [line.strip() for line in f]
    part1(lines[0])


    # Use chinese remainder theorem to calculate the congruence relation, ie solve:
    #  t      % 7  == 0
    # (t + 1) % 13 == 0
    # (t + 4) % 59 == 0
    # (t + 6) % 31 == 0
    # (t + 7) % 19 == 0

    #  t      % 7  == 0
    #  t      % 13 == 12
    #  t      % 59 == 55
    #  t      % 31 == 25
    #  t      % 19 == 12

    #  t == 0  mod 7
    #  t == 12 mod 13
    #  t == 55 mod 59
    #  t == 25 mod 31
    #  t == 12 mod 19

    for line in lines:  # iterates over multiple lines for test data
        part2(line)
