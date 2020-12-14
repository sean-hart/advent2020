def twosum(numbers, target):
    numbers = set(numbers)
    for n in numbers:
        if (target - n) in numbers:
            return sorted([n, target - n])

def threesum(numbers, target):
    numbers = set(numbers)
    for n in numbers:
        remaining_numbers = numbers - set([n])
        two_target = target - n
        two_nums = twosum(remaining_numbers, two_target)
        if two_nums is not None:
            return sorted([n] + list(two_nums))

def day1(numbers, target=2020):
    pair = twosum(numbers, target)
    x,y = pair
    return x*y

def day1b(numbers, target=2020):
    triplet = threesum(numbers, target)
    x,y,z = triplet
    return x*y*z


if __name__ == '__main__':
    import fileinput

    numbers = [int(x) for x in list(fileinput.input())]
    assert len(numbers) == len(set(numbers))

    print('Part 1:', day1(numbers))
    print('Part 2:', day1b(numbers))

