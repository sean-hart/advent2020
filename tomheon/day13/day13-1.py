import sys


def wait_time(ts, bus):
    return bus - (ts % bus)



def main():
    ts, buses = sys.stdin.read().split()
    ts = int(ts)
    buses = [int(b) for b in buses.split(',') if b != 'x']
    with_wait_times = [(wait_time(ts, b), b) for b in buses]
    with_wait_times.sort()
    print(with_wait_times[0][0] * with_wait_times[0][1])


if __name__ == '__main__':
    main()
