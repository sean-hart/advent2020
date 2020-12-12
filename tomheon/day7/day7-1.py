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


def find_all_containers(held_to_holding, bag):
    direct_containers = held_to_holding[bag]
    return direct_containers | reduce(operator.or_, [find_all_containers(held_to_holding, c) for c in direct_containers], set())


def main():
    rules = [line.strip() for line in sys.stdin if line.strip()]
    parsed_rules = [parse_rule(rule) for rule in rules]
    held_to_holding = defaultdict(set)
    for container, contained in parsed_rules:
        for c, _ in contained:
            held_to_holding[c].add(container)

    print(len(find_all_containers(held_to_holding, 'shiny gold')))


if __name__ == '__main__':
    main()
