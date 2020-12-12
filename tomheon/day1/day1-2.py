import sys
import itertools

ints = sorted([int(line.strip()) for line in sys.stdin if line.strip()])

for combo in itertools.combinations(ints, 3):
    if sum(combo) == 2020:
        print(combo, combo[0] * combo[1] * combo[2])


