def compile(text):
    lines = text.strip().splitlines()
    tokens = [line.split() for line in lines]
    machine_code = [(opcode,int(arg)) for (opcode,arg) in tokens]
    return machine_code

def execute_loop(program):
    acc = 0
    seen_instructions = set()

    i = 0
    while i not in seen_instructions:
        seen_instructions.add(i)
        opcode,val = program[i]
        if opcode == 'nop':
            i += 1
        elif opcode == 'acc':
            acc += val
            i += 1
        else:
            i += val

    return acc

def toggle_indices(program):
    for i,instruction in enumerate(program):
        opcode,val = instruction
        if opcode == 'nop' and val != 0:
            yield i
        elif opcode == 'jmp':
            yield i

def toggle(program, i):
    opcode,val = program[i]
    if opcode == 'jmp':
        program[i] = ('nop', val)
    elif opcode == 'nop':
        program[i] == ('jmp', val)

    return program

def execute(program):
    acc = 0
    seen_instructions = set()

    i = 0
    while i not in seen_instructions:
        seen_instructions.add(i)
        opcode,val = program[i]
        if opcode == 'nop':
            i += 1
        elif opcode == 'acc':
            acc += val
            i += 1
        else:
            i += val

        if i >= len(program):
            return acc

    return None


if __name__ == '__main__':
    import fileinput

    data = ''.join(fileinput.input())
    print('Part 1:', execute_loop(compile(data)))


    program = compile(data)
    indices = list(toggle_indices(program))

    result = None
    for i in indices:
        new_program = toggle(program.copy(), i)
        result = execute(new_program)
        if result is not None:
            break

    print('Part 2:', result)
