import sys

def is_valid(args):
    char, pos_1, pos_2, password = args
    extracted = [password[p - 1] for p in [pos_1, pos_2]]
    return extracted.count(char) == 1


def parse_line(line):
    char_poses, char_colon, password = line.split()
    pos_1, pos_2 = [int(i) for i in char_poses.split("-")]
    char = char_colon.strip(":")
    return char, pos_1, pos_2, password

lines = [line.strip() for line in sys.stdin if line.strip()]
valid_lines = [line for line in lines if is_valid(parse_line(line))]


print(len(valid_lines))
