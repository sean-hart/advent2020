import sys

ints = [int(line.strip()) for line in sys.stdin if line]

i = 0
j = 0

while i < len(ints):
    j = i + 1
    while j < len(ints):
        if i < j:
            if ints[i] + ints[j] == 2020:
                print(ints[i], ints[j], ints[i] * ints[j])
        j += 1
    i += 1

    
