#!/usr/local/bin/python3
from functools import reduce

GOLD = 'shiny gold'


def parse_rule(rule):
    bag, raw_contents = rule.split(' contain ')
    contents = {}
    if not raw_contents.startswith('no other bag'):
        for content in raw_contents.rstrip('\n.s').split(', '):
            space = content.index(' ')
            contents[content[space + 1:content.rindex(' ')]] = int(content[:space])

    return bag[:bag.rindex(' ')], contents


def solution(rules):
    def add_bags(bag):
        if not rules[bag]:
            return 0
        return sum(c + c * add_bags(sub_bag) for (sub_bag, c) in rules[bag].items())

    return add_bags(GOLD)


if __name__ == '__main__':
    rules = {}
    with open('input.txt') as f:
        for rule in f.readlines():
            bag, holdables = parse_rule(rule)
            rules[bag] = holdables

    print(solution(rules))


