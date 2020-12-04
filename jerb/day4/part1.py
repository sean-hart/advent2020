#!/usr/local/bin/python3

PASSPORT_FILE = 'input.txt'

REQUIRED_FIELDS = 'byr iyr eyr hgt hcl ecl pid'.split()


def parse_passport(raw_passport):
    fields = raw_passport.rstrip().replace('\n', ' ').split(' ')
    return dict([f.split(':') for f in fields])


def is_valid_passport(passport):
    return all(f in passport for f in REQUIRED_FIELDS)


if __name__ == '__main__':
    with open(PASSPORT_FILE) as f:
        raw_passports = f.read().split('\n\n')

    print(len([p for p in raw_passports
               if is_valid_passport(parse_passport(p))]))
