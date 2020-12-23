import sys
from collections import deque
from itertools import product, chain, takewhile
from functools import reduce
import operator
import re
from copy import deepcopy

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

    def strip_borders(self):
        return [tr[1:-1] for tr in self.tile_bits[1:-1]]

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


    def reconstruct(self):
        stripped_tiles = dict()
        for c, p in self.positions.items():
            stripped_tiles[c] = p.tile.strip_borders()

        rows_per_tile = len(stripped_tiles[(0, 0)])
        
        reconstructed = []
        
        for y in range(self.side):
            for r in range(rows_per_tile):
                reconstructed.append(reduce(operator.add, [stripped_tiles[(x, y)][r]
                                                           for x in range(self.side)]))
        return reconstructed
        
    def remove_tile(self, tile):
        del self.unplaced_tiles[tile.tile_id]

    def solution_id(self):
        return reduce(operator.mul, [self.positions[c].tile.tile_id
                                     for c in
                                     [(0, 0), (0, self.side - 1), (self.side - 1, 0),
                                      (self.side - 1, self.side - 1)]])
        
    def __str__(self):
        return '\n'.join(['PartialImage'] + [str((c, p)) for (c, p) in self.positions.items()] +
                         [str(t) for t in self.unplaced_tiles.values()])

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


def reconstruct_image(instream):
    tiles = list(parse_tiles(instream))
    pi = PartialImage(tiles, int(len(tiles) ** 0.5))
    partial_images = deque()
    partial_images.append(pi)
    
    while True:
        if not partial_images:
            raise Exception('Cannot reconstruct image')
        image = partial_images.pop()
        if image.is_complete:
            return image.reconstruct()
        for new_image in image.extend_one_position():
            partial_images.append(new_image)


SEA_MONSTER_PATTERN = \
"""                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.split('\n')


class SeaMonsterSeeker:

    def __init__(self, sea_monster_pattern):
        self.sea_monster_pattern = sea_monster_pattern

    def mark_all_sea_monsters(self, image):
        found = 0
        new_image = deepcopy(image)
        for y in range(len(image)):
            for x in range(len(image[0])):
                if self.is_sea_monster_at(image, x, y):
                    found += 1
                    self.mark_sea_monster_at(new_image, x, y)
        return found, new_image

    def is_sea_monster_at(self, image, x, y):
        for my in range(len(self.sea_monster_pattern)):
            for mx in range(len(self.sea_monster_pattern[0])):
                if (my + y >= len(image) or
                    mx + x >= len(image[0]) or
                    (self.sea_monster_pattern[my][mx] == '#' and
                     image[y + my][x + mx] != '#')):
                    return False
        return True

    def mark_sea_monster_at(self, image, x, y):
        for my in range(len(self.sea_monster_pattern)):
            for mx in range(len(self.sea_monster_pattern[0])):
                if self.sea_monster_pattern[my][mx] == '#':
                    image[y + my][x + mx] = 'O'


def main():
    image = reconstruct_image(sys.stdin)
    all_orientations = list()

    for k in range(4):
        rot = np.rot90(image, k)
        all_orientations.append(rot)
        all_orientations.append(np.flipud(rot))
        all_orientations.append(np.fliplr(rot))

    sms = SeaMonsterSeeker(SEA_MONSTER_PATTERN)

    for i in all_orientations:
        found, new_image = sms.mark_all_sea_monsters(i)
        if found:
            storm = 0
            for y in range(len(new_image)):
                for x in range(len(new_image[y])):
                    if new_image[y][x] == '#':
                        storm += 1
            print(storm)

        

if __name__ == '__main__':
    main()


def test_strip_borders():
    t = Tile(1, ["abcd", "efgh", "ijkl", "mnop"])
    assert [list("fg"), list("jk")] == t.strip_borders()
