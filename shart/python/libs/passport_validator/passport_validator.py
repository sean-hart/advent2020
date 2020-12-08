def validate_passports(input_string):
    failed = 0
    passports = input_string.split("\n\n")

    required_fields = [
        "byr:",
        "iyr:",
        "eyr:",
        "hgt:",
        "hcl:",
        "ecl:",
        "pid:",
        # "cid",
    ]
    for passport in passports:
        for field in required_fields:
            if field not in passport:
                failed += 1
                break
            

    return len(passports) - failed

def validate_passports2(input_string):
    failed = 0
    passports = input_string.split("\n\n")

    required_fields = [
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
        # "cid",
    ]
    for passport in passports:
        passport_dict = {}
        passport = passport.replace("\n", " ")
        fieldstrings = passport.split(" ")

        for i in fieldstrings:
            if ":" in i:
                key, value = i.split(":")
                passport_dict[key] = value
        for field in required_fields:
            if field not in passport_dict:
                failed += 1
                break
            if not validate(field, passport_dict[field]):
                failed += 1
                break

    return len(passports) - failed

def validate(field, value):
    if field == 'byr':
        return 1920 <= int(value) <= 2002
    elif field == 'iyr':
        return 2010 <= int(value) <= 2020
    elif field == 'eyr':
        return 2020 <= int(value) <= 2030
    elif field == 'hgt':
        if 'cm' in value:
            value = value.rstrip('cm')
            return 150 <= int(value) <= 193
        if 'in' in value:
            value = value.rstrip('in')
            return 59 <= int(value) <= 76
    elif field == 'hcl':
        if len(value) == 7:
            value = value.lstrip('#')
            try:
                int(value)
                return True
            except ValueError:
                return True
    elif field == 'ecl':
        if value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth',]:
            return True
        else:
            return False
    elif field == 'pid':
        if len(value) == 9 and not any(c.isalpha() for c in value):
            return True
        else:
            return False
    else:
        return False
