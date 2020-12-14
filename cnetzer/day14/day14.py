from itertools import chain

def flatten1(l):
    return chain(*l)

def mask_address_and_value(lines):
    for line in lines:
        if line.startswith('mask = '):
            mask_line = line
            mask_str = mask_line.split('=')[1].strip()
            assert len(mask_str) == 36, (mask_str, len(mask_str))
            assert set(mask_str).issubset('01X'), mask_str
        else:
            assert line.startswith('mem[')
            line = line[len('mem['):]
            address = int(line.split(']')[0])
            value = int(line.split('=')[1].strip())

            yield (mask_str, address, value)

def part1(lines):
    mem = {}
    # Unoptimized - could check if mask_str actually changed
    for (mask_str, address, unmasked_value) in mask_address_and_value(lines):
        AND_mask_str = mask_str.translate(str.maketrans('X', '1'))
        OR_mask_str = mask_str.translate(str.maketrans('X', '0'))

        AND_mask = int(AND_mask_str, 2)
        OR_mask = int(OR_mask_str, 2)

        masked_value = (unmasked_value & AND_mask) | OR_mask
        mem[address] = masked_value

    return sum(mem.values())

def part2(lines):
    mem = {}
    # Unoptimized - could check if mask_str actually changed
    for (mask_str, unmasked_address, value) in mask_address_and_value(lines):
        # For masking out the 'X' bits
        x_AND_mask_str = mask_str.translate(str.maketrans('0X', '10'))
        x_AND_mask = int(x_AND_mask_str, 2)

        # This is a bit of a wacky technique, even for me.  "Stitch" the X
        # bits into the split-up mask bits.
        x_count = mask_str.count('X')
        mask_chunks = mask_str.split('X')
        all_masks = []
        for b in range(2**x_count):
            bits = list(f'{b:0{x_count}b}')  # binary string w/ proper number of bits
            first,rest = mask_chunks[:1],mask_chunks[1:]
            cur_mask_str = first[0] + ''.join(flatten1(zip(bits,rest)))
            cur_mask = int(cur_mask_str, 2)
            all_masks.append(cur_mask)

        for mask in all_masks:
            masked_address = (unmasked_address & x_AND_mask) | mask
            mem[masked_address] = value

    return sum(mem.values())

if __name__ == '__main__':
    import fileinput

    lines = list(fileinput.input())

    print('Part 1:', part1(lines))
    print('Part 2:', part2(lines))
