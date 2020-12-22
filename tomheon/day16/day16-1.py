import sys
from itertools import takewhile, dropwhile


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


def find_invalid_values(tickets, rules):
    for t in tickets:
        for v in t:
            if not any([r.is_valid(v) for r in rules]):
                yield v


def main():
    rules = parse_rules(sys.stdin)
    my_ticket, it = parse_my_ticket(sys.stdin)
    nearby_tickets = parse_nearby_tickets(it)
    invalid_values = find_invalid_values(nearby_tickets, rules)
    print(sum(invalid_values))


if __name__ == '__main__':
    main()
