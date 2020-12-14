from collections import Counter

def parse_policy(policy):
    range_str, c = policy.split()
    lo,hi = range_str.split('-')
    lo,hi = int(lo),int(hi)
    return lo,hi,c

def pwcheck(pw, policy):
    counts = Counter(pw)

    lo,hi,char = parse_policy(policy)
    if char not in counts:
        return False

    return lo <= counts[char] <= hi

def pwcheck2(pw, policy):
    lo,hi,char = parse_policy(policy)
    lo,hi = (lo-1),(hi-1)  # Adjust to 0-index

    return sum(pw[i] == char for i in [lo,hi]) == 1


if __name__ == '__main__':
    import fileinput

    lines = list(fileinput.input())

    valid_count = 0
    for line in lines:
        policy,pw = line.split(':')
        if pwcheck(pw.strip(), policy):
            valid_count += 1

    print('Part 1:', valid_count)

    valid_count = 0
    for line in lines:
        policy,pw = line.split(':')
        if pwcheck2(pw.strip(), policy):
            valid_count += 1

    print('Part 2:', valid_count)
