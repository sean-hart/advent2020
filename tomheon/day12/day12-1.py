import sys


DIRECTIONS = 'N E S W'.split()


class Ship:

    def __init__(self, facing_dir):
        self.facing_dir = facing_dir
        self.x = 0
        self.y = 0
        self.forward_map = dict(E=self.move_east,
                                W=self.move_west,
                                N=self.move_north,
                                S=self.move_south)
        self.instruction_map = dict(F=self.move_forward,
                                    R=self.turn_right,
                                    L=self.turn_left,
                                    N=self.move_north,
                                    S=self.move_south,
                                    E=self.move_east,
                                    W=self.move_west)

    def follow_instruction(self, instruction, arg):
        self.instruction_map[instruction](arg)

    def move_forward(self, units):
        self.forward_map[self.facing_dir](units)

    def turn_right(self, degrees):
        self._turn(degrees // 90)
        
    def turn_left(self, degrees):
        self._turn(-(degrees // 90))

    def move_north(self, units):
        self.y += units

    def move_south(self, units):
        self.y -= units

    def move_east(self, units):
        self.x += units

    def move_west(self, units):
        self.x -= units

    def manhattan(self):
        return int(abs(self.x)) + int(abs(self.y))

    def _turn(self, steps):
        cur_ind = DIRECTIONS.index(self.facing_dir)
        new_ind = (cur_ind + steps) % len(DIRECTIONS)
        self.facing_dir = DIRECTIONS[new_ind]


def parse_instr(instr):
    return instr[0], int(instr[1:])


def main():
    ship = Ship('E')
    instrs = [line.strip() for line in sys.stdin if line.strip()]

    for instr in instrs:
        i, arg = parse_instr(instr)
        ship.follow_instruction(i, arg)

    print(ship.manhattan())



if __name__ == '__main__':
    main()
