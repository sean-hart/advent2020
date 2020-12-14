import sys
from copy import deepcopy
from itertools import chain, product



def parse_seats(instream):
    return [list(iter(l.strip())) for l in instream if l.strip()]


def next_visible(r, c, d, seats):
    nv = None
    while True:
        r = r + d[0]
        c = c + d[1]
        if r < 0 or r >= len(seats):
            break
        if c < 0 or c >= len(seats[r]):
            break
        if seats[r][c] in ('#', 'L'):
            nv = seats[r][c]
            break
        
    return nv


def find_line_of_sight(r, c, seats):
    directions = [(rd, cd) for (rd, cd) in product([-1, 0, 1], [-1, 0, 1]) if (rd, cd) != (0, 0)]
    nv = [next_visible(r, c, direction, seats) for direction in directions]
    return [n for n in nv if n]
    

def is_empty_and_isolated(seat, r, c, seats):
    return seat == 'L' and find_line_of_sight(r, c, seats).count('#') == 0


def is_occupied_and_surrounded(seat, r, c, seats):
    return seat == '#' and find_line_of_sight(r, c, seats).count('#') >= 5


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
