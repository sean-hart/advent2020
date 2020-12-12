#!/usr/local/bin/python3
from string import hexdigits

PASSPORT_FILE = 'input.txt'

FIELDS = {
    'byr': lambda y: 1920 <= int(y) <= 2002,
    'iyr': lambda y: 2010 <= int(y) <= 2020,
    'eyr': lambda y: 2020 <= int(y) <= 2030,
    'hgt': lambda h: h[-2:] == 'cm' and 150 <= int(h[:-2]) <= 193 or h[-2:] == 'in' and 59 <= int(h[:-2]) <= 76,
    'hcl': lambda h: h.startswith('#') and all(c in hexdigits.lower() for c in h[1:]),
    'ecl': lambda e: e in 'amb blu brn gry grn hzl oth'.split(),
    'pid': lambda p: len(p) == 9 and all(c.isdigit() for c in p)
}


def parse_passport(raw_passport):
    fields = raw_passport.rstrip().replace('\n', ' ').split(' ')
    return dict([f.split(':') for f in fields])


def is_valid_field(passport, field):
    return field in passport and FIELDS[field](passport[field])


def is_valid_passport(passport):
    return all(is_valid_field(passport, f) for f in FIELDS)


if __name__ == '__main__':
    with open(PASSPORT_FILE) as f:
        raw_passports = f.read().split('\n\n')

    print(len([p for p in raw_passports if is_valid_passport(parse_passport(p))]))
