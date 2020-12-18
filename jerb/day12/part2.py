#!/usr/local/bin/python3

ORDERS = {
    'N': lambda s, w, a: (s, (w[0] + a, w[1])),
    'S': lambda s, w, a: (s, (w[0] - a, w[1])),
    'E': lambda s, w, a: (s, (w[0], w[1] + a)),
    'W': lambda s, w, a: (s, (w[0], w[1] - a)),
    'F': lambda s, w, a: ((s[0] + a * w[0], s[1] + a * w[1]), w),
    'L': lambda s, w, a: (s, rotate(w, -a)),
    'R': lambda s, w, a: (s, rotate(w, a))
}


def parse_orders(lines):
    for line in lines:
        yield line[0], int(line[1:])


def rotate(waypoint, degree):
    for _ in range((degree % 360) // 90):
        waypoint = -waypoint[1], waypoint[0]
    return waypoint


def sail(orders):
    ship = (0, 0)
    waypoint = (1, 10)
    for order in orders:
        ship, waypoint = ORDERS[order[0]](ship, waypoint, order[1])
    return abs(ship[0]) + abs(ship[1])

if __name__ == '__main__':
    with open('input.txt') as f:
        print(sail(parse_orders(f)))

