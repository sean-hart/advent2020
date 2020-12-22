#!/usr/local/bin/python3
from collections import defaultdict, deque
import sys


def setup_history(starting):
    history = defaultdict(lambda: deque(maxlen=2))
    for i, n in enumerate(starting):
        history[n].append(i + 1)
    return history


def speak(turn, spoken, history):
    if spoken in history:
        return turn - 1 - history[spoken][0]
    else:
        return 0


def solution(starting, target):
    history = setup_history(starting)
    turn = len(starting) + 1
    spoken = starting[-1]

    while True:
        spoken = speak(turn, spoken, history)
        history[spoken].append(turn)

        if turn == target:
            return spoken

        turn += 1


if __name__ == '__main__':
    starting = [int(n) for n in sys.stdin.read().rstrip().split(',')]
    print(solution(starting, 30000000)) # 2020 for part1
