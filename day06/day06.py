from __future__ import print_function, division, absolute_import

import itertools


def _redistribute_part1(banks, start_idx):
    """
    Redistribute the memory per part 1.

    Parameters
    ----------
    banks : list
        The memory banks to be reconfigured
    start_idx : int
        The starting index for the reconfiguraiton
    """
    n = len(banks)

    blocks = banks[start_idx]
    banks[start_idx] = 0
    ptr = start_idx + 1
    for i in range(blocks):
        if ptr >= n:
            ptr = 0
        banks[ptr] += 1
        ptr += 1


def part1(banks, max_steps=1E6):
    """

    Parameters
    ----------
    banks : list
        The initial configuration of memory banks.
    max_steps
        The maximum allowable number of steps for the algorithm

    Returns
    -------
    int
        The number of reallocation steps before a
        repeating configuration is encountered.

    """
    previous_configs = {tuple(banks)}

    for step_i in range(int(max_steps)):
        # Determine the maximum index in the banks
        start_idx = banks.index(max(banks))

        print('Step ', step_i)
        print('Max index:', start_idx)
        print('Starting banks', banks)

        _redistribute_part1(banks, start_idx)

        print('Ending banks', banks)

        tup = tuple(banks)

        print(tup)
        print()

        if tup in previous_configs:
            break
        previous_configs.add(tup)

    return step_i + 1


def part2(banks, max_steps=1E6):
    """

    Parameters
    ----------
    banks : list
        The initial configuration of memory banks.
    max_steps
        The maximum allowable number of steps for the algorithm

    Returns
    -------
    int
        The number of steps since the previous configuration.

    """
    previous_configs = {tuple(banks) : 0}

    for step_i in range(int(max_steps)):
        # Determine the maximum index in the banks
        start_idx = banks.index(max(banks))

        print('Step ', step_i)
        print('Max index:', start_idx)
        print('Starting banks', banks)

        _redistribute_part1(banks, start_idx)

        print('Ending banks', banks)

        tup = tuple(banks)

        print(tup)
        print()

        if tup in previous_configs:
            break
        previous_configs[tup] = step_i

    return step_i - previous_configs[tup]


if __name__ == '__main__':

    test_banks = [0, 2, 7, 0]

    print(part1(test_banks, max_steps=10))
    
    input_banks = [int(s) for s in '5 1 10 0 1 7 13 14 3 12 8 10 7 12 0 6'.split()]

    print(part1(input_banks, max_steps=100000))

    ### Part 2 ###

    test_banks = [0, 2, 7, 0]

    print(part2(test_banks, max_steps=10))

    input_banks = [int(s) for s in '5 1 10 0 1 7 13 14 3 12 8 10 7 12 0 6'.split()]

    print(part2(input_banks, max_steps=100000))