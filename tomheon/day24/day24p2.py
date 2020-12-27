import sys

from lark import Lark, Transformer, v_args

WHITE = 1
BLACK = -1
TOGGLE = -1


# FLIP_DIRECTIONS = dict(nw="se", ne="sw", e="w",
#                        se="nw", sw="ne", w="e")


def debug(m):
    print(m)

grammar = """
start: direction+ -> finish

?direction: "nw"
          | "ne"
          | "sw"
          | "se"
          | "e"
          | "w"
"""

@v_args(inline=True)    
class DirectionLexer(Transformer):

    def finish(self, *args):
        return [str(t) for t in args]

    
class Floor:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.deltas = dict(e=(1, -1, 0),
                           se=(0, -1, 1),
                           sw=(-1, 0, 1),
                           w=(-1, 1, 0),
                           nw=(0, 1, -1),
                           ne=(1, 0, -1))
        self.tile_colors = dict()

    def warp_to_origin(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def step_in_direction(self, direction):
        d = self.deltas[direction]
        self.x += d[0]
        self.y += d[1]
        self.z += d[2]

    def flip_current_tile(self):
        p = (self.x, self.y, self.z)
        if p not in self.tile_colors:
            self.tile_colors[p] = BLACK
        else:
            self.tile_colors[p] *= TOGGLE

    def count_black_tiles(self):
        return list(self.tile_colors.values()).count(BLACK)

    def generate_all_neighbors(self):
        existing = list(self.tile_colors.keys())
        for p in existing:
            for d in self.deltas.values():
                n = tuple([p[i] + d[i] for i in range(3)])
                if n not in self.tile_colors:
                    self.tile_colors[n] = WHITE

    def count_black_neighbors(self, p):
        black_ct = 0
        
        for d in self.deltas.values():
            n = tuple([p[i] + d[i] for i in range(3)])
            if n in self.tile_colors and self.tile_colors[n] == BLACK:
                black_ct += 1

        return black_ct

    def conway(self):
        flip = []
        self.generate_all_neighbors()
        for p in self.tile_colors:
            black_neighbors = self.count_black_neighbors(p)
            if self.tile_colors[p] == BLACK and black_neighbors == 0 or black_neighbors > 2:
                flip.append((p, WHITE))
            elif self.tile_colors[p] == WHITE and black_neighbors == 2:
                flip.append((p, BLACK))
        for p, c in flip:
            self.tile_colors[p] = c
            
                

    
def main():
    parser = Lark(grammar, parser='lalr', transformer=DirectionLexer(), keep_all_tokens=True)
    walks = [parser.parse(line.strip()) for line in sys.stdin if line.strip()]
    floor = Floor()
    for walk in walks:
        floor.warp_to_origin()
        for step in walk:
            floor.step_in_direction(step)
        floor.flip_current_tile()
    for d in range(100):
        floor.conway()
    print(floor.count_black_tiles())

if __name__ == '__main__':
    main()
