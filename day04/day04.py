from __future__ import print_function, division, absolute_import

import itertools

def is_valid_passphrase_part1(passphrase):
    """
    Tests that the given passphrase is valid by making sure it has no duplicate words.

    Parameters
    ----------
    passphrase : str
        The passphrase to be checked.

    Returns
    -------
    bool
        True if the passphrase has no duplicate words, otherwise False.
    """
    words = passphrase.split()
    unique_words = set(words)
    return len(words) == len(unique_words)


def is_valid_passphrase_part2(passphrase):
    """
    Test that the passphase is valid by making sure no two words contain the same
    set of letters.

    Parameters
    ----------
    passphrase : str
        The passphrase to be checked.

    Returns
    -------
    bool
        True if the passphrase is valid, otherwise False.

    """
    words = passphrase.split()
    # Get all possible length-2 combinations of words
    combos = itertools.combinations(words, 2)
    for (word_1, word_2) in combos:
        if set(word_1) == set(word_2):
            return False
    return True


def part1():
    """
    Return solution to part 1
    """
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    return len([line for line in lines if is_valid_passphrase_part1(line)])


def part2():
    """
    Return solution to part 2
    """
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    return len([line for line in lines if is_valid_passphrase_part2(line)])


if __name__ == '__main__':

    # Part 1 tests
    print(is_valid_passphrase_part1('aa bb cc dd ee'))
    print(is_valid_passphrase_part1('aa bb cc dd aa'))

    print(part1())

    # Part 2 tests
    print(is_valid_passphrase_part2('abcde fghij'))
    print(is_valid_passphrase_part2('abcde xyz ecdab'))
    print(is_valid_passphrase_part2('a ab abc abd abf abj'))
    print(is_valid_passphrase_part2('oiii ioii iioi iiio'))

    print(part2())
