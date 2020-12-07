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
    def find_gold(holds_gold, bag, path=set()):
        if bag == GOLD:
            return holds_gold | path
        elif not rules[bag]:
            return holds_gold
        else:
            results = [find_gold(holds_gold, content, path | {bag}) for content in rules[bag]]
            return holds_gold.union(*results)

    return len(reduce(find_gold, rules, set()))


if __name__ == '__main__':
    rules = {}
    with open('input.txt') as f:
        for rule in f.readlines():
            bag, holdables = parse_rule(rule)
            rules[bag] = holdables

    print(solution(rules))


