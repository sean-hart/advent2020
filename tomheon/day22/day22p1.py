import sys
from collections import deque
from itertools import takewhile


def parse_deck(instream):
    lines = list(takewhile(lambda l: l.strip(), instream))
    return deque(reversed([int(i) for i in lines[1:]]))


def play_round(deck1, deck2):
    c1 = deck1.pop()
    c2 = deck2.pop()
    if c1 > c2:
        deck1.appendleft(c1)
        deck1.appendleft(c2)
    else:
        deck2.appendleft(c2)
        deck2.appendleft(c1)
    if not deck1:
        return deck2
    if not deck2:
        return deck1
    return None


def score(deck):
    factors = zip(deck, range(1, len(deck) + 1))
    return sum([t[0] * t[1] for t in factors])


def main():
    deck1 = parse_deck(sys.stdin)
    deck2 = parse_deck(sys.stdin)
    winner = None
    while not winner: 
        winner = play_round(deck1, deck2)
    print(score(winner))

if __name__ == '__main__':
    main()
