import itertools
import string

from collections import Counter 

lower_letters = string.ascii_lowercase

def check(count, input):
    for checksum in itertools.combinations(input, count):
        checksum_sum = sum(checksum)
        if checksum_sum == 2020:
            total = 1
            for i in checksum:
                total = total * i
            return total

def check_survey(input):
    grand_total = 0
    for group in input.split("\n\n"):
        raw_answers = group.replace("\n", "")
        group_total = len(set(raw_answers))
        grand_total += group_total
    return grand_total

def check_survey_all(input):
    grand_total = 0
    groups_list = input.split("\n\n")
    for group in groups_list:
        group_list = group.split("\n")
        group = group.replace("\n", "")
        counts = Counter(group)
        all_yes = [k for k in counts if counts[k] == len(group_list)]
        grand_total += len(all_yes)
    return grand_total

def check_cipher(input, preamble_length):
    lines = input.splitlines()
    lines = [int(x) for x in lines]
    line_no = preamble_length
    for i in lines[line_no:]:
        pre = line_no - preamble_length
        preamble = lines[(line_no - preamble_length):line_no]
        found = False
        for j in preamble:
            if i - j in preamble: 
                found = True
                break
        if not found:
            return i, line_no
        line_no += 1

def find_weakness(input, preamble_length):
    seq = []
    lines = input.splitlines()
    lines = [int(x) for x in lines]
    invalid_number, end_line = check_cipher(input, preamble_length)
    for i in range(0, end_line):
        seq = find_sequence(lines, invalid_number, i)       
        if sum(seq) == invalid_number:
            seq.sort()
            return (seq[0] + seq[-1])
    return 0

def find_sequence(number_list, total, index):
    return_list = []
    while sum(return_list) < total:
        return_list.append(number_list[index])
        index += 1
    return return_list
