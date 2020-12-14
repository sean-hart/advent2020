import sys
from copy import deepcopy
from itertools import chain, product



def parse_seats(instream):
    return [list(iter(l.strip())) for l in instream if l.strip()]


def find_adjacent(r, c, seats):
    candidates = [(r + rd, c + cd) for (rd, cd) in product([-1, 0, 1], [-1, 0, 1]) if (rd, cd) != (0, 0)]
    return [seats[r][c] for (r, c) in candidates if (0 <= r < len(seats)) and (0 <= c < len(seats[r]))]
    


def is_empty_and_isolated(seat, r, c, seats):
    return seat == 'L' and find_adjacent(r, c, seats).count('#') == 0


def is_occupied_and_surrounded(seat, r, c, seats):
    return seat == '#' and find_adjacent(r, c, seats).count('#') >= 4


def advance_seats(seats):
    new_seats = deepcopy(seats)

    for r, row in enumerate(seats):
        for c, seat in enumerate(row):
            if is_empty_and_isolated(seat, r, c, seats):
                new_seats[r][c] = '#'
            elif is_occupied_and_surrounded(seat, r, c, seats):
                new_seats[r][c] = 'L'

    return new_seats
    


def main():
    seats = parse_seats(sys.stdin)
    old_seats = []
    
    while old_seats != seats:
        old_seats = seats
        seats = advance_seats(seats)

    print(list(chain.from_iterable(seats)).count('#'))



if __name__ == '__main__':
    main()
