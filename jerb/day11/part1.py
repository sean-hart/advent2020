#!/usr/local/bin/python3
from functools import reduce
from itertools import product

EMPTY = 'L'
FLOOR = '.'
OCCUPIED = '#'


class Seating(list):
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
                if self._empty_area(i, j):
                    shuffled_row.append(OCCUPIED)
                elif self._busy_area(i, j):
                    shuffled_row.append(EMPTY)
                else:
                    shuffled_row.append(row[j])
            shuffled.append(shuffled_row)

        return shuffled

    def _neighbors(self, row, col):
        possible_neighbors = ((row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                              (row, col - 1), (row, col + 1),
                              (row + 1, col - 1), (row + 1, col), (row + 1, col + 1))
        for i, j in possible_neighbors:
            if 0 <= i < len(self) and 0 <= j < len(self[0]) and self[i][j] != FLOOR:
                yield self[i][j]

    def _empty_area(self, i, j):
        """seat (i, j) is empty and there are no adjacent occupied seats"""
        return self[i][j] == EMPTY and not any(s == OCCUPIED for s in self._neighbors(i, j))

    def _busy_area(self, i, j):
        """seat (i, j) is occupied and four or more adjacents seats are also occupied"""
        occupied_neighbors = sum(1 for n in self._neighbors(i, j) if n == OCCUPIED)
        return self[i][j] == OCCUPIED and occupied_neighbors >= 4


def solution(seating):
    shuffled = seating.shuffle()
    while shuffled != seating:
        seating = shuffled
        shuffled = shuffled.shuffle()
    return shuffled.occupied()



if __name__ == '__main__':
    seating = Seating()
    with open('input.txt') as f:
        for line in f.readlines():
            seating.append(list(line.rstrip()))
    print(solution(seating))

