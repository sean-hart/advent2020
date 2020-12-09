import sys
import re
from collections import defaultdict
from functools import reduce
import operator


def unbag(s):
    return ' '.join(s.split()[:-1])


def parse_contained(c):
    num, bag = c.split(' ', 1)
    if num == 'no':
        return None
    return (unbag(bag), int(num))


def parse_rule(rule):
    container, contained = rule.split(' contain ')
    container = unbag(container)
    contained = contained.split(', ')
    contained = [parse_contained(c) for c in contained if parse_contained(c)]
    return (container, contained)


def num_in_bag(holding_to_held, bag):
    direct_in = holding_to_held[bag]
    return sum([n + (n * num_in_bag(holding_to_held, b)) for (b, n) in direct_in])

def main():
    rules = [line.strip() for line in sys.stdin if line.strip()]
    parsed_rules = [parse_rule(rule) for rule in rules]
    holding_to_held = dict(parsed_rules)
    print(num_in_bag(holding_to_held, 'shiny gold'))


if __name__ == '__main__':
    main()
