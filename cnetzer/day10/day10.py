## Too slow. I'd hoped by reducing the number of outgoing edges to just those
## within the distance-3 limit, the number of combinations would be reduced to a
## tractable range.  But it's not even close.  This is essentially traversing
## every possible path, to get a count.
def path_to_target(graph, node_val, target):
    """Count the number of 'True's yielded to get the path count"""
    if node_val == target:
        yield True

    for next_node in graph[node_val]:
        yield from path_to_target(graph, next_node, target)

## Too slow. A variant of the approach above
def count_paths_recursive(graph, node_val, target):
    """A more conventional recursive function (not a recursive generator)"""
    if node_val >= target:
        return 1

    total = 0
    for next_node in graph[node_val]:
        total += count_paths_recursive(graph, next_node, target)

    return total

# Dynamic programming solution (keep track of the number of possible paths for
# each shorter sequence, then use those calculations to generate the solution
# for the current sequence).  I had to get a hint for this from a dynamic
# programming solution (though the graph approach is mine; rather than being
# table-based with nested looping).
def count_paths(path, target):
    """Using a graph of the incoming edges for each node, add each new node and
    count (and store) the number of paths to that node."""
    # Graph of incoming nodes
    incoming_graph = defaultdict(list)
    data_set = set(data)
    for x in reversed(data):
        for y in range(x-3, x):
            if y in data_set:
                incoming_graph[x].append(y)

    G = incoming_graph
    path_counts = { path[0]: 1 }
    for x in path[1:]:
        path_counts[x] = sum(path_counts[y] for y in G[x])

    return max(path_counts.values())


if __name__ == '__main__':
    import fileinput
    from collections import defaultdict, Counter

    data = [int(line) for line in fileinput.input() if line]
    data.sort()
    data.append(data[-1] + 3)
    data = [0] + data

    deltas = [y-x for x,y in zip(data, data[1:])]
    assert max(deltas) == 3, deltas
    assert min(deltas) > 0, deltas

    counts = Counter(deltas)
    ones = counts.get(1, 0)
    threes = counts.get(3, 0)

    print('Part 1:', ones * threes)


    # Graph of outgoing nodes
    graph = defaultdict(list)
    data_set = set(data)
    for x in data:
        for y in range(x+1, x+4):
            if y in data_set:
                graph[x].append(y)

    target = data[-1]
    #print('Part 2:', sum(path_to_target(graph, data[0], target)))
    #print('Part 2:', count_paths_recursive(graph, data[0], target))


    # Following all the outgoing paths was way too slow.
    # Instead, build a graph of the incoming edges for each node, and build up
    # the number of paths from smaller paths (basically a graph-based dynamic
    # programming solution)
    print('Part 2:', count_paths(data, target))
