def parse_passports(data):
    passports = []
    passport = {}
    for line in data:
        line = line.rstrip()

        if not line:
            if passport:
                passports.append(passport)
            passport = {}
            continue

        fields = line.split()
        for field in fields:
            k,v = field.split(':')
            passport[k] = v

    if passport:
        passports.append(passport)

    return passports

def is_valid(passport):
    valid_passport_keys = [
            { 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid' },
            { 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid' },
            ]
    keys = set(passport)

    for keys in valid_passport_keys:
        if keys == set(passport):
            return True

    return False

def valid_hcl(hcl):
    if not hcl.startswith('#'):
        return False
    if len(hcl[1:]) != 6:
        return False
    if not set(hcl[1:]).issubset('0123456789abcdef'):
        return False
    return True

def four_digit_range(s, lo, hi):
    """Return True if s is a 4 digit number string in range of lo-hi (inclusive)"""
    if len(s) != 4:
        return False
    return int(s) in range(lo, hi + 1)

def is_really_valid(passport):
    d = passport

    if not (d['hgt'].endswith('cm') or d['hgt'].endswith('in')):
        return False
    hgt_units = d['hgt'][-2:]
    hgt = int(d['hgt'][:-2])

    if (
        four_digit_range(d['byr'], 1920, 2002) and
        four_digit_range(d['iyr'], 2010, 2020) and
        four_digit_range(d['eyr'], 2020, 2030) and
       ((hgt_units == 'cm' and (193 >= hgt >= 150)) or
        (hgt_units == 'in' and (76 >= hgt >= 59))) and
        (valid_hcl(d['hcl'])) and
        (d['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}) and
        (len(d['pid']) == 9 and set(d['pid']).issubset('0123456789'))
        ):
        return True
    return False


if __name__ == '__main__':
    import fileinput

    data = list(fileinput.input())

    count = 0
    passports = parse_passports(data)
    for passport in passports:
        count += is_valid(passport)

    print('Part 1:', count)

    count = 0
    passports = parse_passports(data)
    for passport in passports:
        count += (is_valid(passport) and is_really_valid(passport))

    print('Part 2:', count)
