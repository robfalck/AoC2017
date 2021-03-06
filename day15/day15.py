from __future__ import print_function, division, absolute_import

from time import time

try:
    # Python 2
    from itertools import izip
except ImportError:
    # Python 3
    izip = zip


# Puzzle input
start = {'a': 618,
         'b': 814}

multiple = {'a': 4,
            'b': 8}

factor = {'a': 16807,
          'b': 48271}

bit_mask = 0b1111111111111111


def gen(n, name='a', use_mult=False):
    """
    This method implements the generators
    defined for day15 of AoC2017.

    Parameters
    ----------
    n : int
        The number of iterations to perform.
    name : str
        The name of the generator, either 'a' or 'b'.  Defining it
        as either generator 'a' or generator 'b' sets the appropriate
        start value, factor, and multiple.  Default is 'a'
    use_mult : bool
        If True, use the given multiple.  If False, assume the multiple
        is 1 (for part 1 of the problem).  Default is False/

    Yields
    ------
    value : int
        The next value in the sequence such that
        value = previous * factor % 2147483647  *and* value % multiple = 0
    """
    prev = start[name]
    mult = multiple[name] if use_mult else 1
    fac = factor[name]

    count = 0
    while count < n:
        cur = (prev * fac) % 2147483647
        prev = cur
        if cur % mult == 0:
            count += 1
            yield cur


def solve(n=40000000, use_mult=False):
    """
    Iterate through generators A and B, incrementing score by 1 when
    the 16 least significant bits are the same.

    Parameters
    ----------
    n : int
        The number of iterations to perform for the generators
    use_mult : bool
        True if the multiplier should be used in the generator (part 2), otherwise False (part 1)

    Returns
    -------
    score : int
        The score obtained for the given number of iterations.

    """
    A = gen(n, name='a', use_mult=use_mult)
    B = gen(n, name='b', use_mult=use_mult)

    score = 0

    for a, b in izip(A, B):
        # Extract 16 least significant bits and compare
        if a & bit_mask == b & bit_mask:
            score += 1

    return score


if __name__ == '__main__':

    t0 = time()
    score = solve(40000000, use_mult=False)
    print('Part 1 Score:', score)  # 577
    print('Time to solve part 1:', time()-t0)

    print()

    t0 = time()
    score = solve(5000000, use_mult=True)
    print('Part 2 Score:', score)  # 316
    print('Time to solve part 2:', time()-t0)
