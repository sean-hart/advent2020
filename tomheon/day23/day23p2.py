import sys
from collections import deque
from itertools import chain


class Cup:

    def __init__(self, label, next_cup_id):
        self.label = label
        self.next_cup_id = next_cup_id

    def __repr__(self):
        return f'Cup(label={self.label}, next_cup_id={self.next_cup_id})'

    def __str__(self):
        return self.__repr__()


def calc_target_label(start_label, min_label, max_label, disallowed_labels):
    label = start_label - 1
    
    if label < min_label:
        label = max_label

    while label in disallowed_labels:
        label -= 1
        if label < min_label:
            label = max_label

    return label


def find_lifted(ids_to_cups, current_id):
    next_id = ids_to_cups[current_id].next_cup_id
    start_seg = next_id
    for _ in range(2):
        next_id = ids_to_cups[next_id].next_cup_id
    end_seg = next_id
    one_past = ids_to_cups[end_seg].next_cup_id
    return start_seg, end_seg, one_past


def extract_lifted_labels(ids_to_cups, start_lifted_id, one_past_lifted_id):
    lifted_labels = []
    cur = start_lifted_id
    while cur != one_past_lifted_id:
        lifted_labels.append(ids_to_cups[cur].label)
        cur = ids_to_cups[cur].next_cup_id

    return lifted_labels


def do_move(ids_to_cups, labels_to_ids, current_id, min_label, max_label):
    start_lifted_id, end_lifted_id, one_past_lifted_id = find_lifted(ids_to_cups, current_id)
    ids_to_cups[current_id].next_cup_id = one_past_lifted_id

    lifted_labels = extract_lifted_labels(ids_to_cups, start_lifted_id, one_past_lifted_id)
    target_label = calc_target_label(ids_to_cups[current_id].label, min_label, max_label, lifted_labels)

    target_id = labels_to_ids[target_label]
    ids_to_cups[end_lifted_id].next_cup_id = ids_to_cups[target_id].next_cup_id
    ids_to_cups[target_id].next_cup_id = start_lifted_id
    
    return ids_to_cups[current_id].next_cup_id 


def print_cups(ids_to_cups, current_id):
    cups = []
    orig_id = current_id
    while True:
        cups.append(ids_to_cups[current_id].label)
        current_id = ids_to_cups[current_id].next_cup_id
        if current_id == orig_id:
            break

    sc = [str(c) for c in cups]
    sc[0] = f'({sc[0]})'
    print('cups: ', ' '.join(sc))


def render_solution(ids_to_cups, labels_to_ids):
    id_of_one = labels_to_ids[1]
    first_cup = ids_to_cups[ids_to_cups[id_of_one].next_cup_id]
    second_cup = ids_to_cups[first_cup.next_cup_id]
    return first_cup.label * second_cup.label
    


def main():
    # inp = "389125467"
    inp = "463528179"
    
    cup_labels = list([int(d) for d in inp])
    for x in range(max(cup_labels) + 1, 1_000_001):
        cup_labels.append(x)
        
    min_label = min(cup_labels)
    max_label = max(cup_labels)
    ids_to_cups = dict([(i, Cup(l, (i + 1) % len(cup_labels))) for (i, l) in enumerate(cup_labels)])
    labels_to_ids = {c.label: i for (i, c) in ids_to_cups.items()}

    current_id = 0
    
    for m in range(10_000_000):
        if m % 1_000_000 == 0:
            print(f'-- move {m+1} --')
        # print_cups(ids_to_cups, current_id)
        current_id = do_move(ids_to_cups, labels_to_ids, current_id, min_label, max_label)
        # print()

    print(render_solution(ids_to_cups, labels_to_ids))
        
if __name__ == '__main__':
    main()
