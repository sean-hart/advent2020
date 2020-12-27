import sys
from collections import deque
from itertools import product, chain, takewhile
from functools import reduce
import operator
import re

import numpy as np


class Tile:

    def __init__(self, tile_id, tile_bits):
        self.tile_id = tile_id
        self.tile_bits = [list(tr) for tr in tile_bits]

    def __eq__(self, other):
        return self.tile_id == other.tile_id and self.tile_bits == other.tile_bits

    def __hash__(self):
        return hash((self.tile_id, tuple([tuple(r) for r in self.tile_bits])))

    def border(self, direction):
        return dict(N=self.north,
                    E=self.east,
                    S=self.south,
                    W=self.west)[direction]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Tile({self.tile_id} {self.tile_bits})'

    @property
    def all_borders(self):
        
        return set([self.north,
                    self.north[::-1],
                    self.south,
                    self.south[::-1],
                    self.east,
                    self.east[::-1],
                    self.west,
                    self.west[::-1]])
    @property
    def rotations(self):
        return [Tile(self.tile_id, np.rot90(self.tile_bits, k)) for k in range(4)]

    @property
    def flips(self):
        return [Tile(self.tile_id, bits)
                for bits
                in [self.tile_bits,
                    np.flipud(self.tile_bits),
                    np.fliplr(self.tile_bits)]]

    @property
    def orientations(self):
        os = set()
        for r in self.rotations:
            for f in r.flips:
                os.add(f)
        return os
    
    @property
    def east(self):
        return ''.join([b[-1] for b in self.tile_bits])

    @property
    def west(self):
        return ''.join([b[0] for b in self.tile_bits])

    @property
    def north(self):
        return ''.join(self.tile_bits[0])

    @property
    def south(self):
        return ''.join(self.tile_bits[-1])

    def has_borders(self, borders):
        """Note that we don't care if the same border, reversed, is used to satisfy two
        incoming borders.  We'll filter it out when we're trying to rotate and
        flip.

        """
        return not bool(set(borders) - self.all_borders)

    


class Position:

    def __init__(self, x, y, tile=None):
        self.x = x
        self.y = y
        self.tile = tile
    
    @property
    def is_filled(self):
        return self.tile is not None

    def shared_edge_direction_with(self, position):
        if self.x == position.x and self.y == position.y + 1:
            return 'N'
        elif self.x == position.x and self.y == position.y - 1:
            return 'S' 
        elif self.x == position.x -1 and self.y == position.y:
            return 'E' 
        elif self.x == position.x + 1 and self.y == position.y:
            return 'W' 
        else:
            raise Exception('No shared edge!')

    def tile_border_at_edge_with(self, position):
        return self.tile.border(self.shared_edge_direction_with(position))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Position({self.x}, {self.y}) = {self.tile}'


class PartialImage:

    def __init__(self, tiles, side, positions=None):
        self.unplaced_tiles = {t.tile_id: t for t in tiles}
        self.side = side 
        if positions is None:
            self.positions = dict()
            for x in range(self.side):
                for y in range(self.side):
                    self.positions[(x, y)] = Position(x, y)
        else:
            self.positions = positions

    def remove_tile(self, tile):
        del self.unplaced_tiles[tile.tile_id]

    def solution_id(self):
        return reduce(operator.mul, [self.positions[c].tile.tile_id
                                     for c in
                                     [(0, 0), (0, self.side - 1), (self.side - 1, 0), (self.side - 1, self.side - 1)]])
        
    def __str__(self):
        return '\n'.join(['PartialImage'] + [str((c, p)) for (c, p) in self.positions.items()] + [str(t) for t in self.unplaced_tiles.values()])

    @property
    def is_complete(self):
        return not [p for p in self.positions.values() if not p.is_filled] 
        
    def extend_one_position(self):
        """Choose a single position and yield a new partial image for each tile
        that fits in it.

        """
        #print('---Extending---')
        coord = self.best_target_coord()
        #print(f'Best target coord {coord}')
        candidate_tiles = self.tiles_fitting_coord(coord)
        for tile in candidate_tiles:
            #print(f'Yielding {tile} for {coord}')
            yield self.with_placed_tile(tile, coord)

    def with_placed_tile(self, tile, coord):
        unplaced_tiles = dict(self.unplaced_tiles)
        positions = dict(self.positions)
        p = positions[coord]
        positions[coord] = Position(p.x, p.y, tile)
        del unplaced_tiles[tile.tile_id]
        return PartialImage(unplaced_tiles.values(), self.side, positions)

    def tiles_fitting_coord(self, coord):
        #print('--Tiles fitting coord--')
        position = self.positions[coord]
        #print(f'Neighbors {self.neighbors(position)}')
        filled_neighbors = [n for n in self.neighbors(position) if n.is_filled]
        # print("FILLED NEIGHBORS")
        # print(position)
        # print(self.neighbors(position))
        # print(filled_neighbors)
        borders_to_match = dict([(position.shared_edge_direction_with(n),
                                  n.tile_border_at_edge_with(position))
                                  for n in filled_neighbors])

        candidate_tiles = [t for t in self.unplaced_tiles.values()
                           if t.has_borders(borders_to_match.values())]
        for ct in candidate_tiles:
            for o in ct.orientations:
               if all([o.border(d) == b for (d, b) in borders_to_match.items()]):
                   yield o
                                
        
    def best_target_coord(self):
        """Find the best target coords to try next, where 'best' means coords of the
        position that:

        1. Is empty
        2. Is manhattan-adjacent to the most filled positions
        3. Is manhattan-adjacent to most unfilled positions (tiebreak for 2)
        4. Has the highest x position (tiebreak for 3)
        5. Has the highest y position (tiebreak for 4)

        """
        targets = sorted([c for c in self.coords if not self.positions[c].is_filled],
                         key=self.grade_coord, reverse=True)
        return targets[0]

    @property
    def coords(self):
        return self.positions.keys()

    def grade_coord(self, coord):
        position = self.positions[coord]
        neighbors = self.neighbors(position)
        return (len([n for n in neighbors if n.is_filled]), len(neighbors), position.x, position.y)

    def neighbors(self, position):
        coord = (position.x, position.y)
        #print(f'Finding neighbors for position {position}')
        #print(f'Coord {coord}')
        #print(f'Neighbors {self.neighbor_coords(coord)}')
        return [self.positions[c] for c in self.neighbor_coords(coord)]

    def neighbor_coords(self, coord):
        coords = [(coord[0] + delta[0], coord[1] + delta[1])
                   for delta
                   in product([-1, 0, 1], [-1, 0, 1])
                   if delta.count(0) == 1]
        #print(f'Gen coords {coords}')
        return [c for c in coords if self.is_coord_in_bounds(c)]
                
    def is_coord_in_bounds(self, coord):
        return 0 <= coord[0] < self.side and 0 <= coord[1] < self.side



def parse_id(line):
    return int(re.match(r'^Tile (\d+):', line).group(1))


def parse_tile(lines):
    tile_id = parse_id(lines[0])
    tile_bits = lines[1:]
    return Tile(tile_id, tile_bits)
    

def parse_tiles(instream):
    while True:
        lines = [l.strip() for l in takewhile(lambda l: l.strip(), instream)]
        if not lines:
            break
        yield parse_tile(lines)


def main():
    tiles = list(parse_tiles(sys.stdin))
    pi = PartialImage(tiles, int(len(tiles) ** 0.5))
    partial_images = deque()
    partial_images.append(pi)
    
    while True:
        if not partial_images:
            print("Empty partial images")
            break
        image = partial_images.pop()
        #print("-Popping image-")
        if image.is_complete:
            # print("Found image")
            # print(image)
            print(image.solution_id())
            break
        for new_image in image.extend_one_position():
            partial_images.append(new_image)
        


if __name__ == '__main__':
    main()



fake_tile_id = 0
    

class FakeTile:

    def __init__(self):
        global fake_tile_id
        fake_tile_id += 1
        self.tile_id = fake_tile_id


def test_construct_partial_image():
    pi = PartialImage([FakeTile() for _ in range(4)], 2)
    assert len(pi.positions) == 4
    assert pi.side == 2
    assert sorted(pi.positions.keys()) == sorted([(0, 0), (0, 1), (1, 0), (1, 1)])
    for p in pi.positions.values():
        assert not p.is_filled


def test_is_coord_in_bounds():
    pi4 = PartialImage([FakeTile() for _ in range(4)], 2)
    assert pi4.is_coord_in_bounds((0, 0))
    assert pi4.is_coord_in_bounds((0, 1))
    assert pi4.is_coord_in_bounds((1, 0))
    assert pi4.is_coord_in_bounds((1, 1))

    assert not pi4.is_coord_in_bounds((-1, 0))
    assert not pi4.is_coord_in_bounds((0, -1))
    assert not pi4.is_coord_in_bounds((2, 0))
    assert not pi4.is_coord_in_bounds((0, 2))
    

def test_neighbor_coords():
    pi4 = PartialImage([FakeTile() for _ in range(4)], 2)
    assert sorted([(0, 1), (1, 0)]) == sorted(pi4.neighbor_coords((0, 0)))
    assert sorted([(0, 1), (1, 0)]) == sorted(pi4.neighbor_coords((1, 1)))
    assert sorted([(0, 0), (1, 1)]) == sorted(pi4.neighbor_coords((1, 0)))

    pi9 = PartialImage([FakeTile() for _ in range(9)], 3)
    assert(sorted([(1, 0), (0, 1), (2, 1), (1, 2)])) == pi9.neighbor_coords((1, 1))

    
def test_grade_coord():
    pi4 = PartialImage([FakeTile() for _ in range(4)], 2)
    # 2 neighbors, neither filled
    assert pi4.grade_coord((0, 0)) == (0, 2, 0, 0)
    assert pi4.grade_coord((1, 0)) == (0, 2, 1, 0)
    pi4.positions[(1, 0)].tile = FakeTile()
    assert pi4.grade_coord((0, 0)) == (1, 2, 0, 0)
    assert pi4.grade_coord((1, 0)) == (0, 2, 1, 0)
    
    pi9 = PartialImage([FakeTile() for _ in range(9)], 3)
    # 4 neighbors, none filled
    assert pi9.grade_coord((1, 1)) == (0, 4, 1, 1)
    pi9.positions[(1, 0)].tile = FakeTile()
    assert pi9.grade_coord((1, 1)) == (1, 4, 1, 1)
    

def test_best_target_coord():
    pi4 = PartialImage([FakeTile() for _ in range(4)], 2)
    assert pi4.best_target_coord() == (1, 1)
    pi4.positions[(1, 1)].tile = FakeTile()
    assert pi4.best_target_coord() == (1, 0)

    pi9 = PartialImage([FakeTile() for _ in range(9)], 3)
    assert pi9.best_target_coord() == (1, 1)
    pi9.positions[(0, 0)].tile = FakeTile()
    pi9.positions[(2, 0)].tile = FakeTile()
    assert pi9.best_target_coord() == (1, 0)

    
def test_is_complete():
    pi4 = PartialImage([FakeTile() for _ in range(4)], 2)
    assert not pi4.is_complete
    pi4.positions[(0, 0)].tile = FakeTile()
    assert not pi4.is_complete
    pi4.positions[(0, 1)].tile = FakeTile()
    pi4.positions[(1, 0)].tile = FakeTile()
    pi4.positions[(1, 1)].tile = FakeTile()
    assert pi4.is_complete


def test_tile_all_borders():
    t = Tile(1, ["ab", "cd"])
    assert set(["ab", "ba", "cd", "dc", "ac", "ca", "bd", "db"]) == t.all_borders

    t2 = Tile(2, ["aa", "cd"])
    assert set(["aa", "cd", "dc", "ac", "ca", "ad", "da"]) == t2.all_borders

    t3 = Tile(3, ["abc", "def", "ghi"])
    assert set(["abc", "cba",
                "ghi", "ihg",
                "adg", "gda",
                "cfi", "ifc"]) == t3.all_borders


def test_tile_borders():
    t = Tile(3, ["abc", "def", "ghi"])
    assert t.north == "abc"
    assert t.west == "adg"
    assert t.south == "ghi"
    assert t.east == "cfi"

    
def test_has_borders():
    t = Tile(1, ["ab", "cd"])
    assert t.has_borders(["ab"])
    assert t.has_borders(["ab", "ac"])
    assert t.has_borders(["ab", "ac", "ba"])
    assert not t.has_borders(["ab", "11"])
    assert not t.has_borders(["11"])
    

def test_tile_border_at_edge_with():
    t = Tile(1, ["abc", "def", "ghi"])
    pos = Position(1, 1, t)
    assert pos.tile_border_at_edge_with(Position(1, 0)) == t.north
    assert pos.tile_border_at_edge_with(Position(1, 2)) == t.south
    assert pos.tile_border_at_edge_with(Position(2, 1)) == t.east
    assert pos.tile_border_at_edge_with(Position(0, 1)) == t.west


def test_rotations():
    t = Tile(1, ["abc", "def", "ghi"])
    for tprime in t.rotations:
        assert tprime.tile_id == t.tile_id
    bits = [[''.join(r) for r in tp.tile_bits] for tp in t.rotations]
    assert sorted(bits) == sorted([["abc", "def", "ghi"],
                                   ["gda", "heb", "ifc"],
                                   ["ihg", "fed", "cba"],
                                   ["cfi", "beh", "adg"]])


def test_flips():
    t = Tile(1, ["ab", "cd"])
    for tprime in t.flips:
        assert tprime.tile_id == t.tile_id
    bits = [[''.join(r) for r in tp.tile_bits] for tp in t.flips]
    assert sorted(bits) == sorted([["ab", "cd"], ["ba", "dc"], ["cd", "ab"]])


def test_tiles_fitting_coord_1():
    t1 = Tile(1, ["ab", "cd"])
    t2 = Tile(2, ["be", "df"])
    t3 = Tile(3, ["cd", "gh"])
    t4 = Tile(4, ["df", "hm"])
    
    pi = PartialImage([t1, t2, t3, t4], 2)
    pi.positions[(0, 0)].tile = t1
    pi.remove_tile(t1)
    assert [t3] == list(pi.tiles_fitting_coord((0, 1)))

    
def test_tiles_fitting_coord_2():
    t1 = Tile(1, ["ab", "cd"])
    t2 = Tile(2, ["be", "df"])
    t3 = Tile(3, ["dc", "gh"])
    t4 = Tile(4, ["df", "hm"])
    
    pi = PartialImage([t1, t2, t3, t4], 2)
    pi.positions[(0, 0)].tile = t1
    pi.remove_tile(t1)
    assert [Tile(3, ["cd", "hg"])] == list(pi.tiles_fitting_coord((0, 1)))


def test_tiles_fitting_coord_3():
    t1 = Tile(1, ["ab", "cd"])
    t2 = Tile(2, ["be", "df"])
    t3 = Tile(3, ["dc", "gh"])
    t4 = Tile(4, ["mc", "md"])
    
    pi = PartialImage([t1, t2, t3, t4], 2)
    pi.positions[(0, 0)].tile = t1
    pi.remove_tile(t1)
    assert set([Tile(3, ["cd", "hg"]), Tile(4, ["cd", "mm"])]) == set(pi.tiles_fitting_coord((0, 1)))

    
def test_with_placed_tile():
    t1 = Tile(1, ["ab", "cd"])
    t2 = Tile(2, ["be", "df"])
    t3 = Tile(3, ["dc", "gh"])
    t4 = Tile(4, ["mc", "md"])
    
    pi = PartialImage([t1, t2, t3, t4], 2)
    new_pi = pi.with_placed_tile(t1, (0, 0))
    assert t1.tile_id not in new_pi.unplaced_tiles
    assert t1.tile_id in pi.unplaced_tiles
    assert not pi.positions[(0, 0)].is_filled
    assert new_pi.positions[(0, 0)].is_filled
    assert new_pi.positions[(0, 0)].tile == t1

    
def test_is_complete():
    t1 = Tile(1, ["ab", "cd"])
    t2 = Tile(2, ["be", "df"])
    t3 = Tile(3, ["dc", "gh"])
    t4 = Tile(4, ["mc", "md"])
    
    pi = PartialImage([t1, t2, t3, t4], 2)
    assert not pi.is_complete
    pi = pi.with_placed_tile(t1, (0, 0))
    assert not pi.is_complete
    pi = pi.with_placed_tile(t2, (1, 0))
    assert not pi.is_complete
    pi = pi.with_placed_tile(t3, (0, 1))
    assert not pi.is_complete
    pi = pi.with_placed_tile(t4, (1, 1))
    assert pi.is_complete


