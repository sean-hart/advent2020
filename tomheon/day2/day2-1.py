import sys

def is_valid(args):
    char, min_occs, max_occs, password = args
    return min_occs <= password.count(char) <= max_occs


def parse_line(line):
    ocs_range, char_colon, password = line.split()
    min_occs, max_occs = [int(i) for i in ocs_range.split("-")]
    char = char_colon.strip(":")
    return char, min_occs, max_occs, password

lines = [line.strip() for line in sys.stdin if line.strip()]
valid_lines = [line for line in lines if is_valid(parse_line(line))]


print(len(valid_lines))
