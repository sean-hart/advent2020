def validate_password_for_count(input_string):
    rng_string, letter, password = input_string.split(' ')
    letter = letter[:-1]
    least, most = rng_string.split('-')
    count = password.count(letter)
    if int(least) <= count <= int(most):
        return True
    else:
        return False

def validate_passwords_for_count(input_string):
    valid_count = 0
    for line in input_string.splitlines():
        if validate_password_for_count(line):
            valid_count +=1
    return valid_count

def validate_password_for_position(input_string):
    rng_string, letter, password = input_string.split(' ')
    letter = letter[:-1]
    first, second = rng_string.split('-')

    # rng_string = rng_string.zfill(int(second))
    if password[int(first) - 1] == password[int(second) - 1]:
        return False
    if (letter == password[int(first) - 1] or letter == password[int(second) - 1]):
        return True
    else:
        return False

def validate_passwords_for_position(input_string):
    valid_count = 0
    for line in input_string.splitlines():
        if validate_password_for_position(line):
            valid_count += 1
    return valid_count
        
