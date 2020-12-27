import sys
from collections import deque


def lift_cups(cups):
    cups = list(cups)
    return deque(cups[0:1] + cups[4:]), deque(cups[1:4])


def calc_destination_cup(left_cups, lifted_cups):
    min_cup_label = min(left_cups + lifted_cups)
    max_cup_label = max(left_cups + lifted_cups)
    label = left_cups[0] - 1
    while label not in left_cups:
        if label < min_cup_label:
            label = max_cup_label
        else:
            label -= 1
    return left_cups.index(label)


def insert_cups(left_cups, lifted_cups, destination_cup):
    for c in reversed(lifted_cups):
        left_cups.insert(destination_cup + 1, c)
    return left_cups


def do_move(cups):
    left_cups, lifted_cups = lift_cups(cups)
    # print('pick up: ', ', '.join([str(c) for c in lifted_cups]))
    destination_cup = calc_destination_cup(left_cups, lifted_cups)
    new_cups = insert_cups(left_cups, lifted_cups, destination_cup)
    new_cups.rotate(-1)
    return new_cups


def print_cups(cups):
    sc = [str(c) for c in cups]
    sc[0] = f'({sc[0]})'
    print('cups: ', ' '.join(sc))


def render_solution(cups):
    while cups[0] != 1:
        cups.rotate(1)
    return ''.join([str(i) for i in list(cups)[1:]]) 
    

def main():
    cups = deque([int(d) for d in "463528179"])
    for m in range(100):
        # print(f'-- move {m + 1} --')
        # print_cups(cups)
        cups = do_move(cups)
        # print()
    print(render_solution(cups))
        
if __name__ == '__main__':
    main()
