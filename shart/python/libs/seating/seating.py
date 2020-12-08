def get_seat_id(code):
    row = code[:7]
    col = code[7:]
    row = row.replace('F', '0').replace('B', '1')
    col = col.replace('L', '0').replace('R', '1')
    row = int(row, 2)
    col = int(col, 2)
    seat_id = row * 8 + col
    return seat_id

def get_highest_seat_id(input):
    highest = 0
    for line in input.splitlines():
        seat_id = get_seat_id(line)
        if seat_id > highest:
            highest = seat_id
    return highest

def get_my_seat(input):
    all_seats = list(range(0, 851))
    print(all_seats)
    for line in input.splitlines():
        all_seats.remove(get_seat_id(line))
    print(all_seats)
    # 1-12 are invalid, 1*4+8seats per row
    my_seat = [x for x in all_seats if 12 < x <= 842  ]
    return my_seat[0]
