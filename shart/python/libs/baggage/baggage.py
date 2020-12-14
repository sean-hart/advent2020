import string

def parse_rules(raw_rules):
    # clear plum bags contain 2 vibrant gray bags, 4 striped tan bags.
    rule_lines = raw_rules.splitlines()
    bag_rules = {}
    for line in rule_lines:
        line = line.replace('bags', 'bag')
        line = line.replace(' ','')
        line = line.rstrip('.')
        outer, inner = line.split('contain')
        if inner == 'nootherbag':
            inner_list = []
        else:
            inner_list = []
            inner_list_raw = inner.split(',')
            for i in inner_list_raw:
                # print(i)
                if i[0] in string.digits:
                    count = int(i[0])
                    inner_list.append((count, i[1:]))
                else:
                    inner_list.append((1, i[1:]))

        if outer in bag_rules:    
            bag_rules[outer]['children'] = inner_list
        else:
            bag_rules[outer] = {'children': inner_list, 'parents': []}
        for child in inner_list:
            if child[1] in bag_rules:
                bag_rules[child[1]]['parents'].append(outer)
            else:
                bag_rules[child[1]] = {'parents': [outer], 'children': []}
    return bag_rules
        # bagmap[outer] = inner_list


def parent_bags(rules, my_bag):
    parsed_rules = parse_rules(rules)
    possible_parents = walk_parent_relationship(parsed_rules, my_bag, set())
    return len(set(possible_parents))


def walk_parent_relationship(rules, bag, collected):
    collected.update(rules[bag]['parents'])
    if rules[bag]['parents'] == []:
        return collected
    for bag in rules[bag]['parents']:
        collected.update(walk_parent_relationship(rules, bag, collected))
    return collected

def child_bags(rules, my_bag):
    parsed_rules = parse_rules(rules)
    total_children = count_walk_child_relationship(parsed_rules, my_bag, 0)
    return total_children

def count_walk_child_relationship(rules, bag, total):
    print(total)
    if len(rules[bag]['children']) == 0:
        return 0
    for child in rules[bag]['children']:
        print(child)
        total += child[0]
        total += count_walk_child_relationship(rules, child[1], total)
    print(total)
    return total


1
- 1
- - 3
- - 4
- 2
- - 5
- - 6
