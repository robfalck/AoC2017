from __future__ import print_function, division, absolute_import

import numpy as np


def calc_sum(input):
    """
    Given a string of digits, find all digits that match the subsequent digit in the sequence
    and sum them.

    Parameters
    ----------
    input : str

    Returns
    -------
    int
        The sum of the digits.
    """
    array = np.array([int(i) for i in input + input[0]], dtype=int)
    indices = np.where(array[:-1] == array[1:])[0]
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

    print(calc_sum(my_input))
