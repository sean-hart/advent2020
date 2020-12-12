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



