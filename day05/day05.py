from __future__ import print_function, division, absolute_import

import itertools


def part1(maze):
    """

    Parameters
    ----------
    maze : list
        A mutable sequence of integers that defines
        the maze to be escaped for part 1 of the test

    Returns
    -------
    int
        The number of steps required to escape the maze

    """
    ptr = 0
    step = 0
    while 0 <= ptr < len(maze):
        offset = maze[ptr]
        maze[ptr] += 1
        ptr += offset
        step += 1
    return step

def part2(maze):
    """

    Parameters
    ----------
    maze : list
        A mutable sequence of integers that defines
        the maze to be escaped for part 2 of the test

    Returns
    -------
    int
        The number of steps required to escape the maze

    """
    ptr = 0
    step = 0
    while 0 <= ptr < len(maze):
        offset = maze[ptr]
        if offset >= 3:
            maze[ptr] -= 1
        else:
            maze[ptr] += 1
        ptr += offset
        step += 1
    return step


if __name__ == '__main__':

    test_maze = [0, 3, 0, 1, -3]

    print(part1(test_maze))

    with open('input.txt', 'r') as f:
        lines = f.readlines()
    maze = [int(s) for s in lines if len(s) > 0]

    print(part1(maze))

    test_maze = [0, 3, 0, 1, -3]
    print(part2(test_maze))

    # reinitialize maze since we changed it
    maze = [int(s) for s in lines if len(s) > 0]

    print(part2(maze))
