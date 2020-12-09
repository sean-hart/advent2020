def find_missing_sum(numbers, N):
    i = N
    while i < len(numbers):
        target = numbers[i]
        window = set(numbers[i-N:i])

        for x in window:
            if target - x in window:
                break
        else: # nobreak
            return numbers[i]

        i += 1

def find_contiguous_sum(numbers, target):
    l,r = 0,1
    while True:
        window = numbers[l:r]
        window_sum = sum(window)
        if window_sum < target:
            r += 1
        elif window_sum > target:
            l += 1
        else:
            return min(window) + max(window)

        if l == r:
            r += 1
        if r >= len(numbers):
            break


if __name__ == '__main__':
    import fileinput

    data = [int(x) for x in fileinput.input()]

    print('Part 1:', find_missing_sum(data, 25))

    print('Part 2:', find_contiguous_sum(data, 138879426))
