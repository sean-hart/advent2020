def find_bootloop(input_string):
    lines = input_string.splitlines()
    line_no, output = process_lines(lines)
    return output

def fix_bootloop(input_string):
    lines = input_string.splitlines()
    output = fix_bootloop_list(lines, 0)
    return output

def fix_bootloop_list(lines, current_line):
    flipped_lines = []
    line_no = 0
    output = 0
    for i in range(0, len(lines)):
        lines_copy = lines.copy()
        if "jmp" in lines_copy[i]:
            lines_copy[i] = lines_copy[i].replace("jmp", "nop")
        elif "nop" in lines_copy[i]:
            lines_copy[i] = lines_copy[i].replace("nop", "jmp")
        processed_lines, output = process_lines(lines_copy)
        if processed_lines[-1] == len(lines):
            break
    return output

def process_lines(lines):
    processed_lines = []
    line_no = 0
    output = 0
    while line_no not in processed_lines:
        processed_lines.append(line_no)
        line_no, output = process_line(lines, output, line_no)
    return processed_lines, output

def process_line(lines, output, line_no):
    if len(lines) <= line_no:
        return line_no, output
    line = lines[line_no]
    command, arg = line.split(' ')
    if command == 'acc':
        output += int(arg)
        line_no += 1
    if command == 'nop':
        line_no += 1
    if command == 'jmp':
        if line_no == line_no + int(arg):
            print("here")
            return line_no, output
        line_no += int(arg)
    return line_no, output


