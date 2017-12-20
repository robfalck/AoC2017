from __future__ import print_function, division, absolute_import

import re
import time
import numpy as np

re_pos = re.compile('p=<(.+?)>')
re_vel = re.compile('v=<(.+?)>')
re_acc = re.compile('a=<(.+?)>')

np.set_printoptions(linewidth=1024, edgeitems=9)

def solve(inp, part=2):

    pmat = np.zeros([len(inp), 9], dtype=int)

    for id, line in enumerate(inp):
        pmatch = re_pos.search(line)
        vmatch = re_vel.search(line)
        amatch = re_acc.search(line)

        pos = np.array([int(s) for s in pmatch.groups()[0].split(',')], dtype=int)
        vel = np.array([int(s) for s in vmatch.groups()[0].split(',')], dtype=int)
        acc = np.array([int(s) for s in amatch.groups()[0].split(',')], dtype=int)

        pmat[id,:3] = pos
        pmat[id,3:6] = vel
        pmat[id,6:9] = acc

    # Simulate
    collided = set()
    for i in range(200):
        pmat[:, 3:6] += pmat[:, 6:9]  # update velocity
        pmat[:, :3] += pmat[:, 3:6]   # update position

        if part == 2:
            for row in range(pmat.shape[0]):
                if row in collided:
                    continue
                colliding_rows = np.where((pmat[:, :3] == pmat[row, :3]).all(axis=1))[0]
                if len(colliding_rows) > 1:
                    # Kill the collided rows
                    pmat[colliding_rows, :3] = 1000000000
                    pmat[colliding_rows, 3:] = 0
                    collided |= set(colliding_rows.tolist())

    # manhattan distance
    result = np.argmin(np.abs(pmat[:, :3]).sum(axis=1))

    if part == 1:
        print('min manhattan distance is particle #:', result)

    if part == 2:
        print('surviving particles:', pmat.shape[0] - len(collided))


if __name__ == '__main__':


    with open('input.txt', 'r') as f:
        puzzle_input = [line.strip() for line in f.readlines() if line]

    t0 = time.time()
    solve(puzzle_input, part=1)
    print('Time to solve part 1:', time.time()-t0, 'sec')

    t0 = time.time()
    solve(puzzle_input, part=2)
    print('Time to solve part 2:', time.time()-t0, 'sec')
