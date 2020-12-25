import sys


def do_loop(subject_number, value):
    return (value * subject_number) % 20201227


def guess_loop_size(subject_number, public_keys):
    value = 1 
    loop_size = 0

    while value not in public_keys:
        value = do_loop(subject_number, value)
        loop_size += 1
    return loop_size, value


def transform(subject_number, loop_size):
    value = 1 
    for _ in range(loop_size):
        value = do_loop(subject_number, value)
    return value


def main():
    public_keys = [int(line.strip()) for line in sys.stdin if line.strip()]
    loop_size, value = guess_loop_size(7, public_keys)
    public_keys.remove(value)
    print(transform(public_keys[0], loop_size))
    

if __name__ == '__main__':
    main()
