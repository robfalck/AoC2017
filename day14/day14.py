from __future__ import print_function, division, absolute_import

import sys
import os

import numpy as np

# Import functions from day10 (since this isn't a package do it the hard way)
dir_, _ = os.path.split(__file__)
sys.path.append(os.path.join(dir_, 'day10'))

from day10.day10 import knot_hash


def hash_to_binary(hash):
    """
    Convert a hexidecimal hash string to
    a 4-bit string of 0's and 1's
    """
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
    grid = np.zeros((128, 128), dtype=int)

    for row in range(128):
        hash_input = '{0}-{1}'.format(puzzle_input, row)
        hash = knot_hash(hash_input)
        grid[row, :] = [int(char) for char in hash_to_binary(hash)]

    print('squares in grid', np.count_nonzero(grid))

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
