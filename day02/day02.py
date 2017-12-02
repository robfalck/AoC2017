from __future__ import print_function, division, absolute_import

import numpy as np

def checksum(file):
    with open(file, 'rb') as f:
        lines = f.readlines()

    diffs = np.zeros(len(lines))

    for i, line in enumerate(lines):
        line_array = np.array([int(s) for s in line.split()])
        diffs[i] = line_array.max() - line_array.min()

    return diffs.sum()


def evenly_divisible_checksum(file):
    with open(file, 'rb') as f:
        lines = f.readlines()

    sum = 0

    for i, line in enumerate(lines):
        line_array = np.array([int(s) for s in line.split()])

        for val in line_array:
            quotient = line_array/float(val)

            for item in quotient:
                # Triple-nested loops :scream:
                if item % 1.0 == 0 and item != 1.0:
                    sum += item

    return sum

if __name__ == '__main__':

    print(checksum('test_input.txt'))

    print(checksum('input.txt'))

    print(evenly_divisible_checksum('test_input2.txt'))

    print(evenly_divisible_checksum('input.txt'))