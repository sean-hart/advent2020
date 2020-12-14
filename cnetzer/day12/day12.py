from math import sin,cos,radians

def compass_to_degrees(compass):
    d = { 'E': 90, 'N': 0, 'S': 180, 'W': 270 }
    return d[compass]

def compass_offsets(compass_dir):
    d = {
         'E': ( 1, 0),
         'N': ( 0, 1),
         'W': (-1, 0),
         'S': ( 0,-1),
        }
    return d[compass_dir]

class Ship:
    def __init__(self, pos_x = 0, pos_y = 0, direction = 'E'):
        self.x = pos_x
        self.y = pos_y
        self.course = compass_to_degrees(direction)

        self._command_map = {
                'E': self.compass_move,
                'N': self.compass_move,
                'W': self.compass_move,
                'S': self.compass_move,
                'L': self.compass_turn,
                'R': self.compass_turn,
                'F': self.move_forward,
                }

    def input(self, s):
        command = s[:1]
        num = int(s[1:])
        self._command_map[command](command, num)

    def compass_move(self, compass_dir, num):
        assert compass_dir in set('NSEW')
        self.x += compass_offsets(compass_dir)[0]*num
        self.y += compass_offsets(compass_dir)[1]*num

    def compass_turn(self, turn_dir, num):
        assert turn_dir in ['L', 'R']
        assert 0 <= num <= 360
        if turn_dir == 'L':
            self.course = (self.course + 360 - num) % 360
        else:
            self.course = (self.course + 360 + num) % 360

    def move_forward(self, _, num):
        self.x += sin(radians(self.course)) * num
        self.y += cos(radians(self.course)) * num

    def manhattan_distance(self):
        return round(abs(self.x) + abs(self.y))

class WaypointShip:
    def __init__(self):
        self.ship_pos = (0,0)
        self.waypoint = (10, 1)

        self._command_map = {
                'E': self.waypoint_move,
                'N': self.waypoint_move,
                'W': self.waypoint_move,
                'S': self.waypoint_move,
                'L': self.waypoint_swivel,
                'R': self.waypoint_swivel,
                'F': self.move_forward,
                }

    def input(self, s):
        command = s[:1]
        num = int(s[1:])
        self._command_map[command](command, num)

    def waypoint_move(self, compass_dir, num):
        assert compass_dir in set('NSEW')
        x_off = compass_offsets(compass_dir)[0]*num
        y_off = compass_offsets(compass_dir)[1]*num
        x, y = self.waypoint
        self.waypoint = (x + x_off, y + y_off)

    def waypoint_swivel(self, turn_dir, num):
        assert turn_dir in ['L', 'R']
        assert 0 <= num <= 360

        x = self.waypoint[0] - self.ship_pos[0]
        y = self.waypoint[1] - self.ship_pos[1]

        if turn_dir == 'L':
            num = -num

        r = radians(num)
        new_x = x*cos(r) + y*sin(r)
        new_y = y*cos(r) - x*sin(r)

        self.waypoint = (self.ship_pos[0] + new_x, self.ship_pos[1] + new_y)

    def move_forward(self, _, num):
        x_off = self.waypoint[0] - self.ship_pos[0]
        y_off = self.waypoint[1] - self.ship_pos[1]
        x,y = self.ship_pos
        for _ in range(num):
            x += x_off
            y += y_off

        self.ship_pos = (x,y)
        self.waypoint = (x + x_off, y + y_off)

    def manhattan_distance(self):
        x,y = self.ship_pos
        return round(abs(x) + abs(y))


if __name__ == '__main__':
    import fileinput

    ship = Ship()
    for line in fileinput.input():
        ship.input(line)

    print('Part 1:', ship.manhattan_distance())


    ship = WaypointShip()
    for line in fileinput.input():
        ship.input(line)

    print('Part 2:', ship.manhattan_distance())
