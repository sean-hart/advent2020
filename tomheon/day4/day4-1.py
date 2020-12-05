import sys
import re


REQUIRED_FIELDS = set('byr iyr eyr hgt hcl ecl pid'.split())


def read_passports(instream):
    sofar = dict()
    for line in instream:
        line = line.strip()
        if not line:
            if sofar:
                yield sofar
            sofar = dict()
        else:
            recs = line.split()
            for rec in recs:
                key, val = rec.split(':')
                sofar[key] = val
    if sofar:
        yield sofar


def has_req_fields(passport):
    return not (REQUIRED_FIELDS - passport.keys())


def is_valid(passport):
    if not has_req_fields(passport):
        return False


def main():
    print(len([p for p in read_passports(sys.stdin) if is_valid(p)]))

    
if __name__ == '__main__':
    main()
            
    
