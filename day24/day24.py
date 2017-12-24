from __future__ import print_function, division, absolute_import

import copy
import time
import numpy as np
import sys


class Bridge(object):

    def __init__(self, initial_components, available_components):
        self.components = list(initial_components)
        self.score = sum([sum(tup) for tup in self.components])
        self.available_components = available_components

    def next_required_number(self):
        if len(self.components) == 1:
            c = self.components[0]
            nrn = c[0] if c.index(0) == 1 else c[1]
        else:
            c1 = self.components[-1]
            c2 = self.components[-2]
            nrn = c1[0] if c1[1] in c2 else c1[1]
        return nrn

    def add_component(self, c):
        nrn = self.next_required_number()
        if nrn not in c:
            raise ValueError('Invalid connection, wrong port.  Needed: {0}  Got: {1}'.format(nrn, str(c)))
        if c not in self.available_components:
            raise ValueError('Component unavailable:', c)
        self.components.append(c)
        self.score += sum(c)
        self.available_components.remove(c)

    # def score(self):
    #     return sum([sum(tup) for tup in self.components])

    def length(self):
        return len(self.components)

    def assemble_next(self):
        """
        Find the next required number in the bridge.  Return
        a *new* list of bridges each with a different valid
        component on the end, depending on the available components.

        Returns
        -------

        """
        nrn = self.next_required_number()
        next_components = [c for c in self.available_components if nrn in c]
        new_bridges = []

        for nx in next_components:
            b = Bridge(initial_components=tuple(self.components),
                       available_components=self.available_components.copy())
            b.add_component(nx)
            new_bridges.append(b)
        return new_bridges

    def __str__(self):
        s = '--'.join(['{0}/{1}'.format(*c) for c in self.components])
        return s


def solve(inp):

    components = [(int(line.split('/')[0]), int(line.split('/')[1])) for line in inp]

    starting_comps = [c for c in components if 0 in c]

    bridges = []

    for sc in starting_comps:
        bridges.append(Bridge((sc,), set(components)-set((sc,))))

    complete_bridges = []
    complete_bridges.extend(bridges)

    for i in range(1000):
        print('.', end='')
        sys.stdout.flush()

        new_bridges = []
        for b in bridges:
            new_bridges.extend(b.assemble_next())

        if not new_bridges:
            # Terminate once no new bridges can be built
            break

        bridges = new_bridges
        complete_bridges.extend(new_bridges)
    strongest_bridge = complete_bridges[np.argmax([b.score for b in complete_bridges])]

    print()
    print('Strongest bridge:')
    print('   ', str(strongest_bridge))
    print('    strength = ', strongest_bridge.score, 'length =', strongest_bridge.length())

    longest_length = np.max([b.length() for b in complete_bridges])

    longest_bridges = [b for b in bridges if b.length() == longest_length]

    strongest_longest_bridge = longest_bridges[np.argmax([b.score for b in longest_bridges])]

    print('Strongest longest bridge:')
    print('   ', str(strongest_longest_bridge))
    print('    strength = ', strongest_longest_bridge.score, 'length =', strongest_longest_bridge.length())





if __name__ == '__main__':


    with open('test_input.txt', 'r') as f:
        puzzle_input = [line.strip() for line in f.readlines() if line]

    t0 = time.time()
    solve(puzzle_input)
    print('Time to solve test:', time.time()-t0, 'sec')

    with open('input.txt', 'r') as f:
        puzzle_input = [line.strip() for line in f.readlines() if line]

    t0 = time.time()
    solve(puzzle_input)
    print('Time to solve:', time.time()-t0, 'sec')
