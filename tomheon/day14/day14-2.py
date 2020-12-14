import re
import sys
from itertools import product


BITS = 36
FLOATING = 'X'
MASK = "mask"
MEM = "mem"


class Computer:

    def __init__(self):
        self.bitmask = BITS * FLOATING
        self.memory = dict()

    def update_bitmask(self, bitmask):
        self.bitmask = bitmask

    def update_memory(self, location, value):
        for masked_loc in self.mask(location):
            self.memory[masked_loc] = value

    def mask(self, location):
        n_bin = self.normalize(location)
        gen = [self.resolve_bit(l, b) for (l, b) in zip(n_bin, self.bitmask)]
        for gend in product(*gen):
            yield int(''.join(gend), 2)

    def normalize(self, value):
        return bin(value)[2:].zfill(BITS)

    def sum_memory(self):
        return sum(self.memory.values())

    def resolve_bit(self, value, mask):
        if mask == FLOATING:
            return ['0', '1']
        elif mask == '1':
            return ['1']
        else:
            return [value]


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
