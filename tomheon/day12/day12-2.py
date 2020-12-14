import sys


class Waypoint:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotate_right(self, degrees):
        steps = degrees // 90
        for _ in range(steps):
            self._swap_coords()
            self.y = -self.y

    def rotate_left(self, degrees):
        steps = degrees // 90
        for _ in range(steps):
            self._swap_coords()
            self.x = -self.x

    def move_north(self, units):
        self.y += units

    def move_south(self, units):
        self.y -= units

    def move_east(self, units):
        self.x += units

    def move_west(self, units):
        self.x -= units

    def _swap_coords(self):
        t = self.x
        self.x = self.y
        self.y = t


class Ship:

    def __init__(self, waypoint):
        self.waypoint = waypoint
        self.x = 0
        self.y = 0
        self.instruction_map = dict(F=self.move_forward,
                                    R=self.waypoint.rotate_right,
                                    L=self.waypoint.rotate_left,
                                    N=self.waypoint.move_north,
                                    S=self.waypoint.move_south,
                                    E=self.waypoint.move_east,
                                    W=self.waypoint.move_west)

    def follow_instruction(self, instruction, arg):
        self.instruction_map[instruction](arg)

    def move_forward(self, units):
        self.x += (self.waypoint.x * units)
        self.y += (self.waypoint.y * units)

    def manhattan(self):
        return int(abs(self.x)) + int(abs(self.y))


def parse_instr(instr):
    return instr[0], int(instr[1:])


def main():
    waypoint = Waypoint(10, 1)
    ship = Ship(waypoint)
    instrs = [line.strip() for line in sys.stdin if line.strip()]

    for instr in instrs:
        i, arg = parse_instr(instr)
        ship.follow_instruction(i, arg)

    print(ship.manhattan())



if __name__ == '__main__':
    main()
