import sys
from itertools import chain


class Instruction:

    def next_instruction_addr(self):
        return 1

    def adjust_accumulator(self, accumulator):
        return accumulator

    def execute(self, accumulator):
        accum_incr, addr_incr = self.adjust_accumulator(accumulator), self.next_instruction_addr()
        return accum_incr, addr_incr


class NopInstruction(Instruction):

    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        return f"Nop {self.arg}"


class AccumInstruction(Instruction):

    def __init__(self, increment):
        self.increment = increment

    def adjust_accumulator(self, accumulator):
        return accumulator + self.increment

    def __repr__(self):
        return f"Accum {self.increment}" 

    
class JumpInstruction(Instruction):

    def __init__(self, jump):
        self.jump = jump

    def next_instruction_addr(self):
        return self.jump

    def __repr__(self):
        return f"Jump {self.jump}"



def parse_instruction(instr_s):
    class_dict = dict(acc=AccumInstruction, nop=NopInstruction, jmp=JumpInstruction)
    instr, arg = instr_s.split()
    return class_dict[instr](int(arg))
    

class Computer:

    def __init__(self, instructions):
        self.instructions = [[i, False] for i in instructions]

    def run(self):
        accum = 0
        addr = 0
        normal_exit = False

        while True:
            if addr == (len(self.instructions) - 1):
                normal_exit = True
                break
            instr, executed = self.instructions[addr]
            if executed:
                break
            accum, addr_incr = instr.execute(accum)
            self.instructions[addr][1] = True
            addr += addr_incr

        return accum, normal_exit


def mutate_at(instructions, index, instr):
    new_instructions = list(instructions)
    new_instructions[index] = instr
    return new_instructions


def try_repair_jmp(instructions):
    for index, instr in enumerate(instructions):
        if type(instr) == JumpInstruction:
            yield mutate_at(instructions, index, NopInstruction(instr.jump))


def try_repair_nop(instructions):
    for index, instr in enumerate(instructions):
        if type(instr) == NopInstruction:
            yield mutate_at(instructions, index, JumpInstruction(instr.arg))


def try_repair_instructions(instructions):
    return chain(try_repair_jmp(instructions), try_repair_nop(instructions))


def main():
    instrs_s = [line.strip() for line in sys.stdin if line.strip()]
    instructions = [parse_instruction(i) for i in instrs_s]
    for mutated in try_repair_instructions(instructions):
        c = Computer(mutated)
        accum, stopped = c.run()
        if stopped:
            print(accum)
            

if __name__ == '__main__':
    main()
        
