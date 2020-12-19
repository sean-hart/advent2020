import sys


def play_elf_game(numbers, num_turns):
    last_said_at = dict()
    n = None

    for t in range(num_turns):
        n = numbers.pop(0)
        if not numbers:
            new_n = t - last_said_at[n] if n in last_said_at else 0
            numbers.append(new_n)
        last_said_at[n] = t

    return n


def main():
    numbers = [int(i) for i in sys.stdin.read().split(',')]
    print(play_elf_game(numbers, 30000000))


if __name__ == '__main__':
    main()
