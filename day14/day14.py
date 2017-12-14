from __future__ import print_function, division, absolute_import

import numpy as np

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

def knot_hash(input_str, rounds=64):
    """
    Return the Knot hash corresponding to the input string.
    """
    ring = list(range(256))
    input_str = [ord(c) for c in input_str]
    input_str += [17, 31, 73, 47, 23]

    pos = 0
    skip = 0

    for round in range(rounds):
        for length in input_str:
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

    return hash


def hash_to_binary(hash):
    """ Convert a hexidecimal hash string to a 4-bit string of 0's and 1's """
    return ''.join([bin(int(char, 16))[2:].zfill(4) for char in hash])


def check_neighboring_blocks(block, grid):
    """
    Given a block, return the immediate neighbors of the block.

    Parameters
    ----------
    block : tuple
        The row and column of a block (row, col)
    grid : ndarray
        The numpy 2D array of containing blocks (1) and empty space (0)

    Returns
    -------
    neighbors : list of tuple (row, col)
        A list of the immediate neighbors of the given block.

    """
    neighbors = []
    i, j = block
    if i >= 1 and grid[i-1, j] == 1:
        neighbors.append((i-1, j))
    if j >= 1 and grid[i, j-1] == 1:
        neighbors.append((i, j-1))
    if i < 127 and grid[i+1, j] == 1:
        neighbors.append((i+1, j))
    if j < 127 and grid[i, j+1] == 1:
        neighbors.append((i, j+1))
    return neighbors


def make_block_group(block, grid, group=None):
    """
    Recursively search for neighbors of the given block, and
    their neighbors, and their neighbors, etc.

    Parameters
    ----------
    block : tuple
        The block whose group is to be determined.
    grid : ndarray
        The 2D numpy array representing blocks (1) and empty space (0)
    group : list or None
        The group to which we are adding the neighbors of the current block.
        On recursive calls, group is passed.  When called externally, group
        should be left as None.

    Returns
    -------
    group : list
        A list of all (row, col) tuples (blocks) that are directly or
        indirectly adjacent to block.

    """
    if group is None:
        group = []

    neighbors = check_neighboring_blocks(block, grid)

    for neighbor in neighbors:
        if neighbor not in group:
            group.append(neighbor)
            make_block_group(neighbor, grid, group)

    return group


def solve(puzzle_input):

    grid_str = ''

    for row in range(128):
        hash_input = '{0}-{1}'.format(puzzle_input, row)
        hash = knot_hash(hash_input)
        grid_str += hash_to_binary(hash) + '\n'

    print('squares in grid', grid_str.count('1'))

    # Convert our string grid to a numpy 2D array
    grid = np.zeros((128, 128), dtype=int)
    for i, row in enumerate(grid_str.split('\n')):
        for j, char in enumerate(row):
            grid[i, j] = int(char)

    np.set_printoptions(linewidth=1024, edgeitems=1024)

    # Keep track of all blocks that have been grouped
    grouped_blocks = set()

    # Keep a dictionary of groups
    groups = {}

    # Get the row and column indices of the blocks
    rows, cols = np.where(grid == 1)

    group_id = 0
    # For each block we have, find all blocks in it's group
    for i in range(len(rows)):
        block = rows[i], cols[i]
        # Skip this block if it's already been grouped
        if block not in grouped_blocks:
            # Find all blocks in the group
            group = make_block_group(block, grid)
            # Add the group to the groups dict
            groups[group_id] = group
            group_id += 1
            # Add the blocks in the newest group to
            # the set of grouped blocks
            grouped_blocks |= set(group)

    print('Number of groups', len(groups))




if __name__ == '__main__':

    test_input = 'flqrgnkx'

    solve(test_input)

    print()

    puzzle_input = 'vbqugkhl'

    solve(puzzle_input)

    # 8148, 1180
