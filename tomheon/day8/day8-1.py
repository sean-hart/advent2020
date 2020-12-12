import sys


class Instruction:

    def next_instruction_addr(self):
        return 1

    def adjust_accumulator(self, accumulator):
        return accumulator

    def execute(self, accumulator):
        accum_incr, addr_incr = self.adjust_accumulator(accumulator), self.next_instruction_addr()
        return accum_incr, addr_incr


class NopInstruction(Instruction):

    def __init__(self, _ignored):
        pass

    def __repr__(self):
        return "Nop"


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

        while True:
            instr, executed = self.instructions[addr]
            if executed:
                break
            accum, addr_incr = instr.execute(accum)
            self.instructions[addr][1] = True
            addr += addr_incr

        return accum


def main():
    instrs_s = [line.strip() for line in sys.stdin if line.strip()]
    instructions = [parse_instruction(i) for i in instrs_s]
    c = Computer(instructions)
    print(c.run())
    

if __name__ == '__main__':
    main()
        
