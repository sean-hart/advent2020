import sys
from itertools import tee, compress


def upper_half(ls):
    return ls[len(ls)//2:]


def lower_half(ls):
    return ls[:len(ls)//2]


class SeatSearch:

    def __init__(self, num_rows, num_seats):
        self.rows = list(range(num_rows))
        self.seats = list(range(num_seats))

    def search(self, search_str):
        for d in search_str:
            self.narrow(d)
        return self.id()

    def narrow(self, direction):
        if direction == 'F':
            self.rows = lower_half(self.rows)
        elif direction == 'B':
            self.rows = upper_half(self.rows)
        elif direction == 'L':
            self.seats = lower_half(self.seats)
        elif direction == 'R':
            self.seats = upper_half(self.seats)
        else:
            raise Error(f'Bad direction {direction}')

    def resolve(self):
        if len(self.rows) != 1 or len(self.seats) != 1:
            raise Error(f'{len(self.rows)} rows and {len(self.seats)} seats')
        return self.rows[0], self.seats[0]

    def so_far(self):
        return self.rows, self.seats

    def id(self):
        r, s = self.resolve()
        return (r * 8) + s


def main():
    search_strs = [line.strip() for line in sys.stdin if line.strip()]
    seat_ids = sorted([SeatSearch(128, 8).search(s) for s in search_strs])
    a, b = tee(seat_ids)
    next(b)
    diffs = [j - i for (i, j) in zip(a, b)]
    seats_after_gap = list(compress(seat_ids[1:], [d == 2 for d in diffs]))
    missing_seats = [s - 1 for s in seats_after_gap]
    print(' '.join([str(s) for s in missing_seats]))

    


if __name__ == '__main__':
    main()
