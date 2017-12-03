from __future__ import print_function, division, absolute_import

import numpy as np

INPUT = 265149

def part1(number):

    skip = 2
    d = 1
    row = None
    col = None

    for shell_idx in range(1, 10000):
        size = shell_idx * 2 + 1
        a = d + skip
        b = a + skip
        c = b + skip
        d = c + skip
        skip = skip + 2

        if a <= number <= b:
            # top
            col = -(size // 2) + (b - number)
            row = size // 2
        elif b <= number <= c:
            # left
            row = size // 2 - (c - number)
            col = -(size // 2)
        elif c <= number <= d:
            # bottom
            row = -(size // 2)
            col = row + (number - c)
        elif number < a:
            # right
            col = size // 2
            row = col - (a - number)
        if row is not None and col is not None:
            manh_dist = abs(row) + abs(col)
            return manh_dist

def part2(number):
    """
    A brute-force approach to part 2.
    """

    map = np.zeros((11, 11), dtype=int)

    row = 5
    col = 5

    map[row, col] = 1

    heading = 'RIGHT'

    dcol = 1
    drow = 0

    nsteps = 70

    for i in range(nsteps):
        row += drow
        col += dcol
        sum_at_next = map[row-1:row+2, col-1:col+2].sum()

        map[row, col] = sum_at_next

        if sum_at_next > number:
            return sum_at_next

        # Determine if we need to change heading
        if heading == 'RIGHT' and map[row-1, col] == 0:
            heading = 'UP'
            drow = -1
            dcol = 0
        elif heading == 'UP' and map[row, col-1] == 0:
            heading = 'LEFT'
            drow = 0
            dcol = -1
        elif heading == 'LEFT' and map[row+1, col] == 0:
            heading = 'DOWN'
            drow = 1
            dcol = 0
        elif heading == 'DOWN' and map[row, col+1] == 0:
            heading = 'RIGHT'
            drow = 0
            dcol = 1


if __name__ == '__main__':
    print(part1(number=INPUT))

    print(part2(number=INPUT))
