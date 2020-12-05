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


def year_between(yr, lower, upper):
    return lower <= yr <= upper
    
        
def has_req_fields(passport):
    return not (REQUIRED_FIELDS - passport.keys())


def is_valid_yr(yr, lower, upper):
    return re.fullmatch('\d{4}', yr) and year_between(int(yr), lower, upper)


def has_valid_byr(passport):
    return is_valid_yr(passport['byr'], 1920, 2002)


def has_valid_iyr(passport):
    return is_valid_yr(passport['iyr'], 2010, 2020)


def has_valid_eyr(passport):
    return is_valid_yr(passport['eyr'], 2020, 2030)


def has_valid_hgt(passport):
    hgt = passport['hgt']
    m = re.fullmatch('(\d+)(cm|in)', hgt)
    if not m:
        return False
    unit = m.group(2)
    quant = int(m.group(1))
    if unit == 'cm':
        return 150 <= quant <= 193
    elif unit == 'in':
        return 59 <= quant <= 76
    else:
        raise Error('wut')

def has_valid_hcl(passport):
    hcl = passport['hcl']
    return re.fullmatch('#[0-9a-f]{6}', hcl)
    

def has_valid_ecl(passport):
    ecl = passport['ecl']
    return ecl in 'amb blu brn gry grn hzl oth'.split()


def has_valid_pid(passport):
    return re.fullmatch('\d{9}', passport['pid'])

def is_valid(passport):
    if not has_req_fields(passport):
        return False
    return all([
                has_valid_byr(passport),
                has_valid_iyr(passport),
                has_valid_eyr(passport),
                has_valid_hgt(passport),
                has_valid_hcl(passport),
                has_valid_ecl(passport),
                has_valid_pid(passport)])


def main():
    print(len([p for p in read_passports(sys.stdin) if is_valid(p)]))

    
if __name__ == '__main__':
    main()
            
    
