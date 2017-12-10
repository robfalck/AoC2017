from __future__ import print_function, division, absolute_import

import numpy as np

def perform_iteration(mylist, length, pos):
    """
    Solve the Day 10 puzzle.



    Parameters
    ----------
    input : str
        the string stream

    Returns
    -------
    score : int
        The score of our stream input
    garbage_count : int
        The number of characters in garbage that are not negated nor !
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


def solve(ring, lengths):

    pos = 0
    skip = 0

    for length in lengths:
        ring = perform_iteration(ring, length, pos)
        pos = pos + length + skip
        skip += 1

        while pos >= len(ring):
            pos = pos - len(ring)

    return ring


if __name__ == '__main__':

    # Test

    ring = list(range(5))
    lengths = [3, 4, 1, 5]
    ring = solve(ring, lengths)
    print(ring, np.prod(ring[:2]))

    ring = list(range(256))
    lengths = [225,171,131,2,35,5,0,13,1,246,54,97,255,98,254,110]
    ring = solve(ring, lengths)

    print(ring, '\n', np.prod(ring[:2]))


    with open('input.txt', 'r') as f:
        input = f.read()
