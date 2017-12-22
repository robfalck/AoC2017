from __future__ import print_function, division, absolute_import

import time
import numpy as np

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)


class Carrier(object):

    def __init__(self, initial_map):
        self.pos = np.array((0, 0), dtype=int)
        self.vel = np.array(NORTH, dtype=int)
        self.infected = set()
        self.infections_caused = 0
        self.initialize_map(initial_map)

    def initialize_map(self, initial_map):
        self.infected.clear()
        n = len(initial_map)
        c = (n - 1) // 2
        for i in range(len(initial_map)):
            for j in range(len(initial_map[i])):
                if initial_map[i][j] == '#':
                    self.infected.add((i-c, j-c))

    def turn_left(self):
        drow, dcol = self.vel
        if (drow, dcol) == NORTH:
            self.vel[:] = WEST
        elif (drow, dcol) == EAST:
            self.vel[:] = NORTH
        elif (drow, dcol) == SOUTH:
            self.vel[:] = EAST
        elif (drow, dcol) == WEST:
            self.vel[:] = SOUTH

    def turn_right(self):
        drow, dcol = self.vel
        if (drow, dcol) == NORTH:
            self.vel[:] = EAST
        elif (drow, dcol) == EAST:
            self.vel[:] = SOUTH
        elif (drow, dcol) == SOUTH:
            self.vel[:] = WEST
        elif (drow, dcol) == WEST:
            self.vel[:] = NORTH

    def burst(self):
        current_infected = False

        print('    Initial pos:', tuple(self.pos.tolist()))
        print('    Initial vel:', tuple(self.vel.tolist()))
        print('    On Infected:', tuple(self.pos.tolist()) in self.infected)

        if tuple(self.pos.tolist()) in self.infected:
            current_infected = True
            self.turn_right()
        else:
            self.turn_left()

        if current_infected:
            # Clean
            self.infected.remove(pos_tup)
            print('    Action:', 'CLEAN')
        else:
            # Infect
            self.infected.add(tuple(self.pos.tolist()))
            print('    Action:', 'INFECT')
            self.infections_caused += 1

        self.pos += self.vel

        print('    Infected population:', len(self.infected))
        print('    Final pos:', tuple(self.pos.tolist()))
        print('    Final vel:', tuple(self.vel.tolist()))
        print()
        #self.print_grid()
        print()

    def print_grid(self):
        max_row = np.max(np.abs([i[0] for i in self.infected]))
        max_col = np.max(np.abs([i[1] for i in self.infected]))

        n = 2 * max((max_row, max_col)) + 1
        c = (n - 1) // 2

        mat = np.empty((n, n), dtype=str)
        mat[:, :] = '.'

        for (i, j) in self.infected:
            mat[i+c, j+c] = '#'

        if tuple(self.pos.tolist()) in self.infected:
            mat[self.pos[0]+c, self.pos[1]+c] = u'\u25CF'
        else:
            mat[self.pos[0]+c, self.pos[1]+c] = u'\u25CB'

        for row in mat:
            print(' '.join(row))


class CarrierPart2(Carrier):

    def __init__(self, initial_map):
        super(CarrierPart2, self).__init__(initial_map)
        self.weakened = set()
        self.flagged = set()

    def burst(self):
        pos_tup = tuple(self.pos.tolist())

        current_infected = pos_tup in self.infected
        current_weakened = pos_tup in self.weakened
        current_flagged = pos_tup in self.flagged

        # print(self.infected)
        #
        # print('    Initial pos:', pos_tup)
        # print('    Initial vel:', tuple(self.vel.tolist()))
        # print('    On Infected:', current_infected)

        if current_infected:
            self.infected.remove(pos_tup)
            self.flagged.add(pos_tup)
            self.turn_right()
        elif current_weakened:
            self.weakened.remove(pos_tup)
            self.infected.add(pos_tup)
            self.infections_caused += 1
        elif current_flagged:
            self.turn_left()
            self.turn_left()
            self.flagged.remove(pos_tup)
        else:
            # Clean
            self.turn_left()
            self.weakened.add(pos_tup)

        self.pos += self.vel

        # print('    Infected population:', len(self.infected))
        # print('    Final pos:', pos_tup)
        # print('    Final vel:', tuple(self.vel.tolist()))
        # print()
        # #self.print_grid()
        # print()


def solve(inp, num_bursts=7):

    # c = Carrier(inp)
    #
    # #c.print_grid()
    #
    # print()
    #
    # for i in range(num_bursts):
    #     print('Burst', i)
    #     c.burst()
    #
    # print('Part 1 Infections caused:', c.infections_caused)

    c2 = CarrierPart2(inp)

    print()

    for i in range(num_bursts):
        print('Burst', i)
        c2.burst()

    print('Part 2 Infections caused:', c2.infections_caused)  # 2510774






if __name__ == '__main__':


    with open('input.txt', 'r') as f:
        puzzle_input = [line.strip() for line in f.readlines() if line]

    t0 = time.time()
    solve(puzzle_input, num_bursts=10000000)
    print('Time to solve part 1:', time.time()-t0, 'sec')
