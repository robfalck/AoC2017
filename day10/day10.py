from __future__ import print_function, division, absolute_import

import numpy as np


def perform_iteration(mylist, length, pos):
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


def solve_part1(ring, lengths, rounds=1):

    pos = 0
    skip = 0

    for round in range(rounds):
        for length in lengths:
            ring = perform_iteration(ring, length, pos)
            pos = pos + length + skip
            skip += 1
            while pos >= len(ring):
                pos = pos - len(ring)
    return ring


def solve_part2(ring, lengths, rounds=64):
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


if __name__ == '__main__':

    # Test

    ring = list(range(5))
    lengths = [3, 4, 1, 5]
    ring = solve_part1(ring, lengths)
    print(ring, np.prod(ring[:2]))

    ring = list(range(256))
    lengths = [225,171,131,2,35,5,0,13,1,246,54,97,255,98,254,110]
    ring = solve_part1(ring, lengths)

    print('solution part 1:', np.prod(ring[:2]))

    # Part 2

    ring = list(range(256))
    lengths = ''
    ring, hash = solve_part2(ring, lengths, rounds=64)

    print()
    print('Tests:')
    print('a2582a3a0e66e6e86e3812dcb672a272')
    print(hash)
    print()

    ring = list(range(256))
    print('3efbe78a8d82f29979031a4aa0b16a9d')
    lengths = '1,2,3'
    ring, hash = solve_part2(ring, lengths, rounds=64)
    print(hash)
    print()

    ring = list(range(256))
    lengths = '225,171,131,2,35,5,0,13,1,246,54,97,255,98,254,110'
    ring, hash = solve_part2(ring, lengths, rounds=64)
    print('solution part 2:', hash)
