import re
import sys


BITS = 36
NOP = 'X'
MASK = "mask"
MEM = "mem"


class Computer:

    def __init__(self):
        self.bitmask = BITS * NOP
        self.memory = dict()

    def update_bitmask(self, bitmask):
        self.bitmask = bitmask

    def update_memory(self, location, value):
        self.memory[location] = self.mask(value)

    def mask(self, value):
        n_bin = self.normalize(value)
        return int(''.join(self.resolve_bit(v, b) for (v, b) in zip(n_bin, self.bitmask)), 2)

    def normalize(self, value):
        return bin(value)[2:].zfill(BITS)

    def sum_memory(self):
        return sum(self.memory.values())

    def resolve_bit(self, value, mask):
        if mask == NOP:
            return value
        else:
            return mask


def run_mask_cmd(c, mask):
    c.update_bitmask(mask.strip())

    
def run_mem_cmd(c, dest, arg):
    loc = int(re.fullmatch(r'^mem\[(\d+)\]', dest).group(1))
    value = int(arg.strip())
    c.update_memory(loc, value)
        

def main():
    c = Computer()
    program = [line.strip() for line in sys.stdin if line.strip()]
    for cmd in program:
        dest, arg = cmd.split(' = ')
        if dest.startswith(MASK):
            run_mask_cmd(c, arg)
        elif dest.startswith(MEM):
            run_mem_cmd(c, dest, arg)
        else:
            raise Error(f'Bad cmd {cmd}')
    print(c.sum_memory())
    

if __name__ == '__main__':
    main()
