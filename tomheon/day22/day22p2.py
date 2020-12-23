import sys
from collections import deque
from itertools import takewhile, islice


def parse_deck(instream):
    lines = list(takewhile(lambda l: l.strip(), instream))
    return deque([int(i) for i in lines[1:]])


def gen_deck_sig(deck1, deck2):
    return (tuple(deck1), tuple(deck2))


def should_recurse(c1, deck1, c2, deck2):
    return c1 <= len(deck1) and c2 <= len(deck2)


def play_round(deck1, deck2):
    c1 = deck1.popleft()
    c2 = deck2.popleft()
    round_winner = 1 if c1 > c2 else 2

    if should_recurse(c1, deck1, c2, deck2):
        round_winner = play_game(deque(islice(deck1, 0, c1)), deque(islice(deck2, 0, c2)))

    if round_winner == 1:
        deck1.append(c1)
        deck1.append(c2)
    else:
        deck2.append(c2)
        deck2.append(c1)


def play_game(deck1, deck2):
    game_winner = 0
    seen_decks = set()
    
    while not game_winner:
        deck_sig = gen_deck_sig(deck1, deck2)
        if deck_sig in seen_decks:
            game_winner = 1
        else:
            seen_decks.add(deck_sig)
            play_round(deck1, deck2)
            if not deck1:
                game_winner = 2
            if not deck2:
                game_winner = 1

    return game_winner


def score(deck):
    factors = zip(reversed(deck), range(1, len(deck) + 1))
    return sum([t[0] * t[1] for t in factors])


def main():
    deck1 = parse_deck(sys.stdin)
    deck2 = parse_deck(sys.stdin)
            
    if play_game(deck1, deck2) == 1:
        print(score(deck1))
    else:
        print(score(deck2))

if __name__ == '__main__':
    main()
