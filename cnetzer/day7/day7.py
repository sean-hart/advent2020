from itertools import islice

def chunkify(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(islice(it, n))
        if not chunk:
            return
        yield chunk

def parse_rules(f):
    bag_map = {}
    for line in f:
        line = line.strip()
        if not line:
            continue
        if 'no other bags' in line:
            outer_bag = ' '.join(line.split()[:2])
            bag_map[outer_bag] = []
        else:
            line = line.replace(',', '').replace('.', '')
            cols = line.split()
            outer_bag = ' '.join(cols[:2])
            bag_map[outer_bag] = []
            for quad in chunkify(4, cols[4:]):
                    count,adj,color,_ = quad
                    inner_bag = ' '.join([adj, color])
                    bag_map[outer_bag].append((int(count),inner_bag))
    return bag_map

def walk_path(bag_map, bag, target):
    if not bag_map[bag]:
        return

    for (count, inner_bag) in bag_map[bag]:
        if inner_bag == target:
            yield True
            return
        else:
            yield from walk_path(bag_map, inner_bag, target)

def walk_path2(bag_map, bag):
    if not bag_map[bag]:
        return

    for (count, inner_bag) in bag_map[bag]:
        inner_count = count + count*sum(walk_path2(bag_map, inner_bag))
        yield inner_count


if __name__ == '__main__':
    import fileinput

    bags = parse_rules(fileinput.input())
    count = 0
    for bag in bags:
        if list(walk_path(bags, bag, 'shiny gold')):
            count += 1
    print('Part 1:', count)


    count = sum(walk_path2(bags, 'shiny gold'))
    print('Part 2:', count)
