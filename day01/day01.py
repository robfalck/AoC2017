from __future__ import print_function, division, absolute_import

import numpy as np


def calc_sum(input, part=1):
    """
    Given a string of digits, find all digits that match the subsequent digit in the sequence
    and sum them.

    Parameters
    ----------
    input : str
        The input to be decoded
    part : int
        The part of the day1 puzzle being solved.

    Returns
    -------
    int
        The sum of the digits.
    """
    n = len(input)
    if part == 1:
        offset = 1
    else:  # part 2
        offset = n // 2

    array = np.array([int(i) for i in input] + [int(i) for i in input[:offset]], dtype=int)
    indices = np.where(array[:n] == array[offset:])[0]

    return array[indices].sum()


if __name__ == '__main__':
    # Tests
    print('1122', calc_sum('1122'))
    print('1111', calc_sum('1111'))
    print('1234', calc_sum('1234'))
    print('91212129', calc_sum('91212129'))

    # Using input
    with open('input.txt', 'r') as f:
        my_input = f.read()

    print('part 1, input', calc_sum(my_input))

    # Tests
    print('1212', calc_sum('1212', part=2))
    print('1221', calc_sum('1221', part=2))
    print('123425', calc_sum('123425', part=2))
    print('123123', calc_sum('123123', part=2))
    print('12131415', calc_sum('12131415', part=2))

    # Using input
    with open('input.txt', 'r') as f:
        my_input = f.read()

    print('part 2, input', calc_sum(my_input, part=2))
