import itertools

def check(count, input):
    for checksum in itertools.combinations(input, count):
        checksum_sum = sum(checksum)
        if checksum_sum == 2020:
            total = 1
            for i in checksum:
                total = total * i
            return total
