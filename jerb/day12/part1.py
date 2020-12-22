#!/usr/local/bin/python3


ORDERS = {
    'N': lambda f, d, a: ((f[0] + a, f[1]), d),
    'S': lambda f, d, a: ((f[0] - a, f[1]), d),
    'E': lambda f, d, a: ((f[0], f[1] + a), d),
    'W': lambda f, d, a: ((f[0], f[1] - a), d),
    'W': lambda f, d, a: ((f[0], f[1] - a), d),
    'F': lambda f, d, a: ((f[0] + d[0] * a, f[1] + d[1] * a), d),
    'L': lambda f, d, a: (f, rotate(d, -a)),
    'R': lambda f, d, a: (f, rotate(d, a))
}


def parse_orders(lines):
    for line in lines:
        yield line[0], int(line[1:])


def rotate(direction, degree):
    for _ in range((degree % 360) // 90):
        direction = -direction[1], direction[0]
    return direction


def sail(orders):
    ship = (0, 0)
    direction = (0, 1)
    for order in orders:
        ship, direction = ORDERS[order[0]](ship, direction, order[1])
    return abs(ship[0]) + abs(ship[1])


if __name__ == '__main__':
    with open('input.txt') as f:
        print(sail(parse_orders(f)))
