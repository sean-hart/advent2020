#!/usr/local/bin/python3
from functools import reduce
from itertools import product


EMPTY = 'L'
FLOOR = '.'
OCCUPIED = '#'


class Seating(list):
    @staticmethod
    def from_file(input_file):
        seating = Seating()
        with open(input_file) as f:
            for line in f.readlines():
                seating.append(list(line.rstrip()))
        return seating

    """an append-only seating map that maintains a hash of its contents"""
    def occupied(self):
        return reduce(lambda t, row: t + sum(1 for s in row if s == OCCUPIED), self, 0)

    def shuffle(self):
        """returns a new Seating with seats shfited according to the rules"""
        shuffled = Seating()

        rows = len(self)
        cols = len(self[0])
        for i, row in enumerate(self):
            shuffled_row = []
            for j, spot in enumerate(row):
                if self._empty_area((i, j)):
                    shuffled_row.append(OCCUPIED)
                elif self._busy_area((i, j)):
                    shuffled_row.append(EMPTY)
                else:
                    shuffled_row.append(row[j])
            shuffled.append(shuffled_row)

        return shuffled

    def _look(self, origin, direction):
        """returns the state of the first seat seen by looking in the given direction"""

        # this method is very slow but i am behind on AOC so sadly this will remain as-is
        dx, dy = direction
        x, y = origin[0] + dx, origin[1] + dy
        while  0 <= x < len(self) and 0 <= y < len(self[0]):
            spot = self[x][y]
            if spot != FLOOR:
                return spot
            x += dx
            y += dy

    def _visible_from(self, seat):
        """returns the first seat visible in every direction from the given seat"""
        directions = [d for d in product(range(-1, 2), range(-1, 2)) if d != (0, 0)]
        return filter(None, map(lambda d: self._look(seat, d), directions))

    def _empty_area(self, seat):
        """seat `seat` is empty and there are no adjacent occupied seats"""
        return self[seat[0]][seat[1]] == EMPTY and not any(s == OCCUPIED for s in self._visible_from(seat))

    def _busy_area(self, seat):
        """seat `seat` is occupied and five or more adjacents seats are also occupied"""
        occupied_neighbors = sum(1 for n in self._visible_from(seat) if n == OCCUPIED)
        return self[seat[0]][seat[1]] == OCCUPIED and occupied_neighbors >= 5


def solution(seating):
    shuffled = seating.shuffle()
    while shuffled != seating:
        seating = shuffled
        shuffled = shuffled.shuffle()
    return shuffled.occupied()


if __name__ == '__main__':
    print(solution(Seating.from_file('input.txt')))

