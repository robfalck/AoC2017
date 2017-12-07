from __future__ import print_function, division, absolute_import

import collections
from six import iteritems, itervalues

import networkx as nx

def tier_weight(G, node):
    """
    Return the total weight of the given node and all of its descendants
    Parameters
    ----------
    G : nx.DiGraph
        The directed graph on which we are operating
    node : str
        The node whose tier weight is to be returned

    Returns
    -------
    int
        The total weight of the given node and all of its descendants

    """
    return G.nodes[node]['weight'] + \
           sum([G.nodes[node]['weight'] for node in nx.descendants(G, node)])


def find_faulty_weight(G, base_node, tier=2):
    """
    Traverse each tier of the tower, starting from base_node, and print
    the disk at each tier which has a faulty tier weight.  Also print
    the corrected weight of the disk on that tier that would balance
    the tower.

    Once the child disks of a given disk are found to be balanced, we
    can stop the recursion.

    Parameters
    ----------
    G : nx.DiGraph
        The directed graph on which we are operating.
    base_node : str
        The base disk on which the next tier rests
    tier : int
        The depth of recursion for printing purposes.
        We start at tier 2, the disks resting on the base of the tower.
    """
    # Get the immediate children
    children = [node for node in nx.bfs_successors(G, base_node)][0][1]

    # Get the total weight of the immediate children and all their successors
    children_weights = {}
    for node in children:
        children_weights[node] = tier_weight(G, node)

    # Count the frequency of the weights in the child tiers
    counter = collections.Counter(itervalues(children_weights))

    # Invert the mappings so we can look up nodes by frequency and weight
    inv_counter = {v: k for k, v in iteritems(counter)}
    inv_children_weights = {v: k for k, v in iteritems(children_weights)}

    if 1 in inv_counter:
        children_balanced = False
    else:
        children_balanced = True

    if tier == 2:
        print('tier -  unbalanced disk  -  corrected weight')

    if not children_balanced:
        unbalanced_child = inv_children_weights[inv_counter[1]]
        weight = G.node[unbalanced_child]['weight']
        weight_error = inv_counter[1] - counter.most_common(1)[0][0]
        print('{0:3d}          {1:10s}      {2:15d}'.format(tier,
                                                            unbalanced_child,
                                                            weight-weight_error))
        find_faulty_weight(G, inv_children_weights[inv_counter[1]], tier=tier+1)
    else:
        # end the recursive search, we found the faulty disk
        print('child tiers balanced, problem disk found')
        pass

def solve(input):
    """
    Solve the Day 7 puzzle with the given input.
    """
    G = nx.DiGraph()

    # read input and populate the graph
    for line in input:
        if not line.strip():
            continue
        if '->' in line:
            left, right = line.split('->')
        else:
            left = line
            right = ''
        node_name, node_weight = left.split()
        node_weight = int(node_weight.replace('(', '').replace(')', ''))
        node_children = [s.strip() for s in right.split(',') if len(s) > 0]

        if node_name not in G.nodes:
            # If we havent already added the disk to the tower, add it now
            G.add_node(node_name, weight=node_weight)
        else:
            # If it's already in the tower as a child, set it's weight
            G.node[node_name]['weight'] = node_weight

        for child in node_children:
            # Add each child if it isn't already in the DiGraph, initially with a weight of 0
            if child not in G.nodes:
                G.add_node(child, weight=0)
            # Make a graph edge from the node to the child
            G.add_edge(node_name, child)

    # Find the base disk by using a topological sort of the DiGraph
    base_disk = [item for item in nx.topological_sort(G)][0]

    print('Base disk is', base_disk)

    print('Finding unbalanced disk in each tier:')
    find_faulty_weight(G, base_disk)


if __name__ == '__main__':

    with open('test_input.txt', 'r') as f:
        test_input = f.readlines()
    solve(test_input)

    print()

    with open('input.txt', 'r') as f:
        input = f.readlines()
    solve(input)

