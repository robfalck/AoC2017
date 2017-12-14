from __future__ import print_function, division, absolute_import

import time
import numpy as np

import networkx as nx

def perform_iteration(ring, length, pos):
    """
    Solve the Day 10 puzzle.
    """
    if pos + length < len(ring):
        ring[pos: pos+length] = ring[pos: pos+length][::-1]
    else:
        seq = ring[pos:] + ring[:pos + length - len(ring)]
        len_new_left = pos + length - len(ring)
        len_new_right =  len(ring) - pos
        new_left = seq[:len_new_left][::-1]
        new_right = seq[-len_new_right:][::-1]
        ring[:len(new_left)] = new_left
        ring[-len(new_right):] = new_right
    return ring

def knot_hash(ring, lengths, rounds=64):
    lengths = [ord(c) for c in lengths]
    lengths += [17, 31, 73, 47, 23]

    pos = 0
    skip = 0

    for round in range(rounds):
        for length in lengths:
            ring = perform_iteration(ring, length, pos)
            pos = pos + length + skip
            skip += 1

            while pos >= len(ring):
                pos = pos - len(ring)

    im1 = 0
    hash = ''
    for i in range(16, 256+1, 16):
        seq = ring[im1: i]
        result = seq[0]
        for j in range(1, len(seq)):
            result = result ^ seq[j]
        hash += '{0:02x}'.format(result)
        im1 = i

    return ring, hash


def hash_to_binary(hash):
    return ''.join([bin(int(char, 16))[2:].zfill(4) for char in hash])

def solve(puzzle_input):

    grid_str = ''

    for row in range(128):
        ring = list(range(256))
        hash_input = '{0}-{1}'.format(puzzle_input, row)
        ring, hash = knot_hash(ring, hash_input, rounds=64)
        grid_str += hash_to_binary(hash) + '\n'

    print('squares in grid', grid_str.count('1'))

    grid = np.zeros((128, 128), dtype=int)
    for i, row in enumerate(grid_str.split('\n')):
        for j, char in enumerate(row):
            grid[i, j] = int(char)

    np.set_printoptions(linewidth=1024, edgeitems=1024)
    #print(grid)

    group = 1
    for i in range(128):
        for j in range(1,128):
            # Check if block to left
            if grid[i, j] == 1:
                if grid[i, j-1] != 0:
                    grid[i, j] = grid[i, j-1]
                else:
                    grid[i, j] = group
            else:
                group += 1
        break

    print(grid)



if __name__ == '__main__':

    test_input = 'flqrgnkx'

    solve(test_input)

    puzzle_input = 'vbqugkhl'

    solve(puzzle_input)

    # print()
    #
    # with open('input.txt', 'r') as f:
    #     puzzle_input = f.readlines()
    #
    # t0 = time.time()
    # solve(puzzle_input)
    # print('Time for solution:', time.time()-t0)
    #
