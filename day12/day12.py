from __future__ import print_function, division, absolute_import

import networkx as nx


def solve(puzzle_input):
    G = nx.Graph()

    nodes = range(len(puzzle_input))

    G.add_nodes_from(nodes)

    for line in puzzle_input:
        source, targets = line.strip().split('<->')
        targets = [int(target.strip()) for target in targets.split(',') if target.strip() != '']
        G.add_edges_from([(int(source), target) for target in targets])

    # Part 1
    nodes_connected_to_zero = [i for i in nodes if nx.has_path(G, 0, i)]
    print('Number of nodes connected to 0:', len(nodes_connected_to_zero))

    # Part 2
    groups = {0: nodes_connected_to_zero}
    grouped_nodes = set(nodes_connected_to_zero)
    ungrouped_nodes = set(nodes) - grouped_nodes

    while ungrouped_nodes:
        node_i = next(iter(ungrouped_nodes))
        nodes_connected_to_i = [node for node in ungrouped_nodes if nx.has_path(G, node, node_i)]
        groups[node_i] = [node_i] + nodes_connected_to_i
        ungrouped_nodes = ungrouped_nodes - set(nodes_connected_to_i)

    print('Number of groups', len(groups))



if __name__ == '__main__':

    with open('test_input.txt', 'r') as f:
        puzzle_input = f.readlines()

    solve(puzzle_input)

    print()
    with open('input.txt', 'r') as f:
        puzzle_input = f.readlines()

    from time import time
    t0 = time()
    solve(puzzle_input)
    print('time:', time() - t0)
