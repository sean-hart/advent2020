import sys
from itertools import takewhile, dropwhile, filterfalse
from functools import reduce
import operator


class Rule:

    def __init__(self, field, ranges):
        self.field = field
        self.ranges = ranges

    def __repr__(self):
        return f'Rule {self.field} {self.ranges}'

    def is_valid(self, value):
        return any([lower <= value <= upper for (lower, upper) in self.ranges])


def parse_range(r):
    return tuple([int(i) for i in r.split('-')])


def parse_rule(raw_rule):
    field, raw_range_opts = raw_rule.split(':')
    raw_ranges = raw_range_opts.split(' or ')
    ranges = [parse_range(r) for r in raw_ranges]
    return Rule(field, ranges)


def parse_rules(instream):
    raw_rules = [line.strip() for line in takewhile(lambda l: l.strip(), instream)]
    return [parse_rule(raw_rule) for raw_rule in raw_rules]


def parse_ticket(line):
    return [int(i) for i in line.strip().split(',')]


def parse_my_ticket(instream):
    it = dropwhile(lambda l: l.strip() == 'your ticket:', instream)
    line = next(it).strip()
    return parse_ticket(line), it


def parse_nearby_tickets(instream):
    it = dropwhile(lambda l: not l.strip(), instream)
    it2 = dropwhile(lambda l: l.strip() == 'nearby tickets:', it)
    return [parse_ticket(line) for line in it2 if line.strip()]


def is_valid_ticket(ticket, rules):
    return all([any([r.is_valid(v) for r in rules]) for v in ticket])


def find_candidate_fields(i, tickets, rules):
    for r in rules:
        if all([r.is_valid(t[i]) for t in tickets]):
            yield r.field

def prune_candidates_once(candidates):
    uniquely_taken = reduce(operator.or_, [f for (i, f) in candidates if len(f) == 1], set())

    for ut in uniquely_taken:
        for i, fields in candidates:
            if len(fields) > 1:
                fields -= uniquely_taken


def is_dupe_candidates(candidates):
    return any([len(f) > 1 for (_, f) in candidates])
            
            
def prune_candidates(candidates):
    while is_dupe_candidates(candidates):
        prune_candidates_once(candidates)
    return [(i, list(c)[0]) for (i, c) in candidates]


def sum_departure_fields(field_mappings, ticket):
    return reduce(operator.mul, [ticket[i] for (i, f) in field_mappings if f.startswith('departure')])

            
def main():
    rules = parse_rules(sys.stdin)
    my_ticket, it = parse_my_ticket(sys.stdin)
    nearby_tickets = parse_nearby_tickets(it)
    valid_tickets = [t for t in nearby_tickets + [my_ticket] if is_valid_ticket(t, rules)]
    candidates = [(i, set(find_candidate_fields(i, valid_tickets, rules))) for i in range(len(rules))]
    candidates = prune_candidates(candidates)
    print(sum_departure_fields(candidates, my_ticket))
    

if __name__ == '__main__':
    main()
