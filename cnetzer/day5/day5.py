def find_row(seq):
    rows = range(128)  # Rows 0 - 127
    while seq:
        direction = seq[:1]
        mid = len(rows) // 2
        if direction.upper() == 'F':
            rows = rows[:mid]
        else:
            rows = rows[mid:]
        seq = seq[1:]

    assert len(rows) == 1, rows
    return list(rows)[0]

def find_col(seq):
    cols = range(8)  # Rows 0 - 7
    while seq:
        direction = seq[:1]
        if direction.upper() == 'L':
            cols = cols[:len(cols)//2]
        else:
            cols = cols[len(cols)//2:]
        seq = seq[1:]

    assert len(cols) == 1, cols
    return list(cols)[0]


def seat_ids(seat_seqs):
    all_seat_ids = []
    for seq in seat_seqs:
        assert len(seq) == 10, seq
        row = find_row(seq[:7])
        col = find_col(seq[7:])
        all_seat_ids.append(row*8 + col)
    return(all_seat_ids)


if __name__ == '__main__':
    import fileinput

    data = [line.strip() for line in list(fileinput.input()) if line]

    passes = []
    for boarding_pass in data:
        passes.append(boarding_pass)

    print('Part 1:', max(seat_ids(passes)))


    all_seat_ids = seat_ids(data)
    assert len(set(all_seat_ids)) == len(all_seat_ids), len(all_seat_ids)

    all_seat_ids = set(all_seat_ids)

    possible_seat_ids = []
    for seat in range(max(all_seat_ids)):
        if (seat not in all_seat_ids) and ((seat + 1) in all_seat_ids) and ((seat - 1) in all_seat_ids):
            possible_seat_ids.append(seat)

    assert len(possible_seat_ids) == 1, possible_seat_ids
    print("Part 2:", possible_seat_ids[0])
